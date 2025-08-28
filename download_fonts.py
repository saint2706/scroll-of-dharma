from __future__ import annotations

import time
import ssl
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import re

# Where to store fonts
BASE_DIR = Path(__file__).resolve().parent
FONTS_DIR = BASE_DIR / "assets" / "fonts"
FONTS_DIR.mkdir(parents=True, exist_ok=True)

# Families to fetch via Google Fonts CSS API (woff2)
# For ital-enabled families, we request 0 (roman) and 1 (italic) where needed.
FAMILIES: dict[str, dict] = {
    # Gita Scroll
    "Cormorant Garamond": {
        "axes": "ital,wght",
        "variants": [(0, 400), (0, 700), (1, 400)],  # Regular, Bold, Italic
    },
    "EB Garamond": {
        "axes": "ital,wght",
        "variants": [(0, 400), (0, 700), (1, 400)],
    },
    # Fall of Dharma
    "Cinzel": {
        "axes": "wght",
        "variants": [(400,), (700,)],
    },
    "Spectral": {
        "axes": "ital,wght",
        "variants": [(0, 400), (0, 700), (1, 400)],
    },
    # Weapon Quest
    "Cormorant Unicase": {
        "axes": "wght",
        "variants": [(400,), (700,)],
    },
    "Alegreya": {
        "axes": "ital,wght",
        "variants": [(0, 400), (0, 700), (1, 400)],
    },
    # Devanagari fallback
    "Noto Serif Devanagari": {
        "axes": "wght",
        "variants": [(400,), (700,)],
    },
    "Tiro Devanagari Sanskrit": {
        "axes": "wght",
        "variants": [(400,)],
    },
}

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0 Safari/537.36"
)

# Minimal sanity size (bytes) to consider a font valid (prevents empty files)
MIN_BYTES = 2 * 1024


def _with_static_fallback(url: str) -> str | None:
    # Not used in CSS API flow, retained for safety.
    m = re.match(
        r"^(https://github.com/google/fonts/raw/main/ofl/[^/]+/)([^/]+\.ttf)$", url
    )
    if m:
        return m.group(1) + "static/" + m.group(2)
    return None


def fetch(url: str, retries: int = 3, timeout: int = 30) -> bytes:
    """Download the resource with basic retries and a desktop UA."""
    ctx = ssl.create_default_context()
    backoff = 1.0
    last_err: Exception | None = None
    for _ in range(retries):
        try:
            req = Request(url, headers={"User-Agent": UA})
            with urlopen(req, context=ctx, timeout=timeout) as resp:
                return resp.read()
        except (URLError, HTTPError, ssl.SSLError) as e:
            # On 404, try a /static/ URL variant once
            if isinstance(e, HTTPError) and e.code == 404:
                alt = _with_static_fallback(url)
                if alt and alt != url:
                    url = alt
                    continue
            last_err = e
            time.sleep(backoff)
            backoff *= 2
    if last_err:
        raise last_err
    raise RuntimeError("Unknown error during fetch")


def download_file(url: str, dest: Path) -> tuple[bool, str | None]:
    """Download a single URL into dest. Returns (skipped, error_or_none)."""
    if dest.exists():
        try:
            if dest.stat().st_size >= MIN_BYTES:
                return True, None
        except OSError:
            pass
    try:
        data = fetch(url)
        if len(data) < MIN_BYTES:
            return False, f"Downloaded size too small: {len(data)} bytes"
        tmp = dest.with_suffix(dest.suffix + ".part")
        tmp.write_bytes(data)
        tmp.replace(dest)
        return False, None
    except Exception as e:  # noqa: BLE001
        return False, str(e)


def _css_family_param(name: str, axes: str, variants: list[tuple]) -> str:
    fam = name.replace(" ", "+")
    if axes == "wght":
        weights = ";".join(str(v[0]) for v in variants)
        return f"family={fam}:{axes}@{weights}"
    elif axes == "ital,wght":
        parts = []
        for v in variants:
            if len(v) != 2:
                continue
            ital, w = v
            parts.append(f"{ital},{w}")
        return f"family={fam}:{axes}@{';'.join(parts)}"
    else:
        # Fallback basic request
        return f"family={fam}"


def build_css_url() -> tuple[str, list[str]]:
    """Build a single CSS2 request URL covering all families.

    Returns (css_url, family_names_list)
    """
    params = []
    fam_order: list[str] = []
    for name, cfg in FAMILIES.items():
        params.append(
            _css_family_param(name, cfg.get("axes", "wght"), cfg.get("variants", []))
        )
        fam_order.append(name)
    query = "&".join(params) + "&display=swap"
    return f"https://fonts.googleapis.com/css2?{query}", fam_order


CSS_WOFF2_RE = re.compile(
    r"url\((['\"]?)(?:(https?):)?//([^)'\"]+\.woff2)(?:\?[^)'\"]*)?\1\)"
)
CSS_WOFF_RE = re.compile(
    r"url\(((['\"]?)(?:(https?):)?//([^)'\"]+\.woff)(?:\?[^)'\"]*)?)\1\)"
)


FONTFACE_BLOCK_RE = re.compile(r"@font-face\s*\{(.*?)\}", re.DOTALL | re.IGNORECASE)
FAMILY_RE = re.compile(r"font-family:\s*(['\"])(.+?)\1\s*;", re.IGNORECASE)
STYLE_RE = re.compile(r"font-style:\s*(normal|italic)\s*;", re.IGNORECASE)
WEIGHT_RE = re.compile(r"font-weight:\s*(\d+)\s*;", re.IGNORECASE)
UNICODE_RE = re.compile(r"unicode-range:\s*([^;]+);", re.IGNORECASE)


def _extract_url(block: str) -> tuple[str | None, str | None]:
    """Return (url, ext) prefer woff2 then woff."""
    m2 = CSS_WOFF2_RE.search(block)
    if m2:
        scheme = m2.group(2) or "https"
        path = m2.group(3)
        return f"{scheme}://{path}", "woff2"
    m1 = CSS_WOFF_RE.search(block)
    if m1:
        full = m1.group(1)
        # m1 groups: 1 full match (maybe with quotes), 2 quote, 3 scheme, 4 path
        # Re-run simpler groups
        m = re.match(r"(['\"]?)(?:(https?):)?//([^?'\"]+\.woff)", full)
        if m:
            scheme = m.group(2) or "https"
            path = m.group(3)
            return f"{scheme}://{path}", "woff"
    return None, None


def parse_font_faces(css_text: str) -> list[dict]:
    faces: list[dict] = []
    for m in FONTFACE_BLOCK_RE.finditer(css_text):
        block = m.group(1)
        fam_m = FAMILY_RE.search(block)
        sty_m = STYLE_RE.search(block)
        w_m = WEIGHT_RE.search(block)
        if not (fam_m and sty_m and w_m):
            continue
        url, ext = _extract_url(block)
        if not url:
            continue
        u_m = UNICODE_RE.search(block)
        unicode_range = u_m.group(1).strip() if u_m else ""
        family = fam_m.group(2)
        style = sty_m.group(1)
        weight = int(w_m.group(1))
        faces.append(
            {
                "family": family,
                "style": style,
                "weight": weight,
                "url": url,
                "ext": ext or "woff2",
                "unicode_range": unicode_range,
                "pref_latin": ("latin" in url.lower())
                or ("U+0000-00FF" in unicode_range.upper()),
            }
        )
    return faces


def _fam_key(name: str) -> str:
    return re.sub(r"\s+", "", name)


def _friendly_name(family: str, italic: bool, weight: int, ext: str) -> str:
    fam = _fam_key(family)
    if italic:
        return f"{fam}-Italic-{weight}.{ext}"
    return f"{fam}-{weight}.{ext}"


def _select_variants(faces: list[dict]) -> list[dict]:
    wanted: list[dict] = []
    # Build lookup by (family, italic, weight)
    by_key: dict[tuple[str, bool, int], list[dict]] = {}
    for fc in faces:
        fam = fc["family"]
        if fam not in FAMILIES:
            continue
        italic = fc["style"].lower() == "italic"
        key = (fam, italic, fc["weight"])
        by_key.setdefault(key, []).append(fc)

    for fam, cfg in FAMILIES.items():
        axes = cfg.get("axes", "wght")
        variants = cfg.get("variants", [])
        for v in variants:
            if axes == "ital,wght":
                ital, w = v
                italic = bool(ital)
                key = (fam, italic, int(w))
            else:
                w = v[0]
                italic = False
                key = (fam, italic, int(w))
            cands = by_key.get(key, [])
            if not cands:
                continue
            # Prefer woff2, prefer latin subset
            cands.sort(
                key=lambda x: (
                    0 if x["ext"] == "woff2" else 1,
                    0 if x["pref_latin"] else 1,
                )
            )
            picked = cands[0]
            picked = dict(picked)  # shallow copy
            picked["dest_name"] = _friendly_name(fam, italic, int(w), picked["ext"])
            wanted.append(picked)
    return wanted


def main() -> int:
    print(f"Saving fonts to: {FONTS_DIR}")
    ok = 0
    skipped = 0
    errors: list[tuple[str, str]] = []

    css_url, fams = build_css_url()
    print(f"Requesting CSS: {css_url}")
    try:
        css = fetch(css_url).decode("utf-8", errors="replace")
    except Exception as e:  # noqa: BLE001
        print(f"Failed to fetch CSS: {e}")
        return 1

    # Write debug copy of CSS for troubleshooting
    (FONTS_DIR / "fonts_css_debug.css").write_text(css, encoding="utf-8")

    faces = parse_font_faces(css)
    selected = _select_variants(faces)
    if not selected:
        print("No matching font variants found in CSS. Aborting.")
        return 1

    manifest_lines = [f"CSS: {css_url}"]
    for item in selected:
        url = item["url"]
        filename = item["dest_name"]
        dest = FONTS_DIR / filename
        was_skipped, err = download_file(url, dest)
        if err is None:
            if was_skipped:
                skipped += 1
                print(f"SKIP  {filename}")
            else:
                ok += 1
                print(f"OK    {filename}")
            manifest_lines.append(f"{filename} <- {url}")
        else:
            errors.append((filename, err))
            print(f"FAIL  {filename} -> {err}")

    # Write a simple manifest for reference
    (FONTS_DIR / "fonts_manifest.txt").write_text(
        "\n".join(manifest_lines), encoding="utf-8"
    )

    print("\nSummary:")
    print(f"  Downloaded: {ok}")
    print(f"  Skipped:    {skipped}")
    print(f"  Failed:     {len(errors)}")
    if errors:
        print("\nFailures:")
        for fn, err in errors:
            print(f"  - {fn}: {err}")

    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
