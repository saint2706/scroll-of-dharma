from __future__ import annotations

import types
from pathlib import Path

import pytest  # type: ignore

import app
from narrative import NARRATIVES

# Added: top-level guarded import to satisfy style rule
try:
    import streamlit.runtime as runtime_module  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - streamlit is an install requirement
    runtime_module = None


@pytest.fixture(autouse=True)
def stub_streamlit_runtime(monkeypatch: pytest.MonkeyPatch):
    """Provide a lightweight media manager so `register_audio` stays pure."""
    if runtime_module is None:
        pytest.skip("streamlit runtime is unavailable")

    media_manager = types.SimpleNamespace(
        add=lambda path, *_args, **_kwargs: f"streamlit-media://{Path(path).name}"
    )
    monkeypatch.setattr(runtime_module, "exists", lambda: True)
    monkeypatch.setattr(
        runtime_module,
        "get_instance",
        lambda: types.SimpleNamespace(media_file_mgr=media_manager),
    )

    return media_manager


def _assert_asset_exists(path: Path, message: str) -> None:
    assert path.exists(), message


def test_narrative_assets_are_present(stub_streamlit_runtime):
    for chapter_key, stories in NARRATIVES.items():
        chapter_backgrounds = getattr(app, "CHAPTER_BACKGROUNDS", None)
        assert chapter_backgrounds is not None, "app.CHAPTER_BACKGROUNDS is missing"
        background_name = chapter_backgrounds.get(chapter_key)
        assert (
            background_name
        ), f"Missing background mapping for chapter '{chapter_key}'"
        background_path = app.get_asset_path("textures", background_name)
        _assert_asset_exists(
            background_path,
            f"Background texture '{background_name}' for '{chapter_key}' is missing",
        )

        artwork_map = getattr(app, "SOUNDSCAPE_ARTWORK", None)
        assert artwork_map is not None, "app.SOUNDSCAPE_ARTWORK is missing"
        chapter_artwork = artwork_map.get(chapter_key)
        assert chapter_artwork, f"Missing soundscape artwork for chapter '{chapter_key}'"

        default_artwork = chapter_artwork.get("default")
        assert (
            default_artwork
        ), f"Chapter '{chapter_key}' is missing default soundscape artwork"
        default_subfolder = default_artwork.get("subfolder")
        default_filename = default_artwork.get("filename")
        assert (
            default_subfolder and default_filename
        ), f"Default artwork for '{chapter_key}' must define subfolder and filename"
        default_path = app.get_asset_path(default_subfolder, default_filename)
        _assert_asset_exists(
            default_path,
            f"Default soundscape artwork '{default_filename}' for '{chapter_key}' is missing",
        )

        # Resolve chant mapping attribute robustly (supports multiple possible names)
        chant_mapping = None
        for attr_name in ("CHANT_LINES", "CHAPTER_CHANTS", "CHAPTER_CHANT_LINES"):
            if hasattr(app, attr_name):
                chant_mapping = getattr(app, attr_name)
                break
        assert chant_mapping is not None, (
            "No chant lines mapping found "
            "(looked for app.CHANT_LINES / app.CHAPTER_CHANTS / "
            "app.CHAPTER_CHANT_LINES)"
        )
        chapter_chants = chant_mapping.get(chapter_key, {})
        assert chapter_chants, f"Missing chant lines for chapter '{chapter_key}'"

        for story_key in stories:
            asset_info = app.scene_assets.get(story_key)
            assert asset_info, f"No scene asset mapping for story '{story_key}'"

            svg_filename = asset_info["svg"]
            svg_path = app.get_asset_path("svg", svg_filename)
            _assert_asset_exists(
                svg_path, f"SVG '{svg_filename}' for story '{story_key}' is missing"
            )

            svg_html = app.load_animated_svg(
                asset_info["svg"], asset_info["anim_class"], asset_info["alt"]
            )
            assert svg_html, f"SVG loader returned empty content for '{story_key}'"

            chant_lines = chapter_chants.get(story_key)
            assert (
                chant_lines
            ), f"Missing chant lines for story '{chapter_key}/{story_key}'"
            assert all(
                line.strip() for line in chant_lines
            ), f"Blank chant line detected for story '{chapter_key}/{story_key}'"

            has_override = story_key in chapter_artwork
            artwork_details = chapter_artwork.get(story_key, default_artwork)
            story_subfolder = artwork_details.get("subfolder", default_subfolder)
            story_filename = artwork_details.get("filename", default_filename)
            if has_override:
                assert artwork_details.get(
                    "subfolder"
                ), f"Override artwork for '{chapter_key}/{story_key}' missing subfolder"
                assert artwork_details.get(
                    "filename"
                ), f"Override artwork for '{chapter_key}/{story_key}' missing filename"
            assert story_subfolder, f"Artwork subfolder missing for '{chapter_key}/{story_key}'"
            assert story_filename, f"Artwork filename missing for '{chapter_key}/{story_key}'"
            artwork_path = app.get_asset_path(story_subfolder, story_filename)
            path_label = (
                f"Soundscape artwork '{story_filename}' for '{chapter_key}/{story_key}'"
                if has_override
                else (
                    f"Soundscape artwork '{default_filename}' for "
                    f"'{chapter_key}/{story_key}' (default)"
                )
            )
            _assert_asset_exists(
                artwork_path,
                path_label,
            )

            primary_audio, ambient_audio = app.get_audio_for_story(
                chapter_key, story_key
            )
            for label, audio_path in {
                "primary": primary_audio,
                "ambient": ambient_audio,
            }.items():
                if audio_path is None:
                    continue
                _assert_asset_exists(
                    audio_path,
                    (
                        f"{label.title()} audio '{audio_path.name}' "
                        f"for '{chapter_key}/{story_key}' is missing"
                    ),
                )
                register_fn = getattr(
                    app.register_audio,
                    "__wrapped__",
                    app.register_audio,
                )
                url = register_fn(audio_path)
                assert url, (
                    f"register_audio returned no URL for {label} asset "
                    f"'{audio_path.name}' ({chapter_key}/{story_key})"
                )
                url = register_fn(audio_path)
                assert url, (
                    f"register_audio returned no URL for {label} asset "
                    f"'{audio_path.name}' ({chapter_key}/{story_key})"
                )
