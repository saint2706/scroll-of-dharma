"""
Font downloader for the Scroll of Dharma project.

This script fetches specified font families from the Google Fonts API,
downloads the WOFF2 font files, and saves them to the `assets/fonts` directory.
It is designed to be run from the command line, typically via `setup.py`.

The process is as follows:
1.  **Build a CSS API URL**: Constructs a single, optimized URL to request all
    font variants defined in the `FAMILIES` dictionary.
2.  **Fetch the CSS**: Downloads the CSS file from the Google Fonts API. This
    CSS contains `@font-face` rules with URLs pointing to the actual font files.
3.  **Parse the CSS**: Extracts the font family, style, weight, and file URL
    from each `@font-face` rule using regular expressions.
4.  **Select Variants**: Matches the parsed font faces against the requested
    variants in `FAMILIES` to get the precise URLs for the fonts we need.
5.  **Download Font Files**: Downloads each font file, skipping any that
    already exist, and saves it with a standardized, friendly filename
    (e.g., `CormorantGaramond-Regular-400.woff2`).
6.  **Generate Manifests**: Creates a debug CSS file and a manifest text file
    for troubleshooting.
"""
from __future__ import annotations

import time
import ssl
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import re

# The directory where fonts will be stored.
BASE_DIR = Path(__file__).resolve().parent
FONTS_DIR = BASE_DIR / "assets" / "fonts"
FONTS_DIR.mkdir(parents=True, exist_ok=True)

# Configuration for all font families to be fetched from the Google Fonts CSS API.
# The structure is a dictionary where each key is the font family name.
# - "axes": Specifies the axes for variable fonts (e.g., 'wght', 'ital,wght').
# - "variants": A list of tuples defining the specific styles to download.
#   For 'wght', each tuple is (weight,).
#   For 'ital,wght', each tuple is (italic_flag, weight), where italic is 0 or 1.
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
    "Cinzel": {"axes": "wght", "variants": [(400,), (700,)]},
    "Spectral": {
        "axes": "ital,wght",
        "variants": [(0, 400), (0, 700), (1, 400)],
    },
    # Weapon Quest
    "Cormorant Unicase": {"axes": "wght", "variants": [(400,), (700,)]},
    "Alegreya": {
        "axes": "ital,wght",
        "variants": [(0, 400), (0, 700), (1, 400)],
    },
    # Devanagari fallback for script rendering
    "Noto Serif Devanagari": {"axes": "wght", "variants": [(400,), (700,)]},
    "Tiro Devanagari Sanskrit": {"axes": "wght", "variants": [(400,)]},
}

# A standard desktop User-Agent header to send with requests.
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0 Safari/537.36"
)

# A minimal file size in bytes to consider a downloaded font valid. This
# helps prevent saving empty or corrupted files from failed downloads.
MIN_BYTES = 2 * 1024


def _with_static_fallback(url: str) -> str | None:
    """
    A fallback mechanism for font URLs (currently unused in the CSS API flow).

    This function was designed for older font fetching methods and is retained
    for potential future use or safety. It transforms a font URL to its '/static/'
    equivalent if it matches a specific GitHub raw content pattern.
    """
    # This function is not actively used in the current CSS API download flow
    # but is kept for robustness in case of future changes.
    m = re.match(
        r"^(https://github.com/google/fonts/raw/main/ofl/[^/]+/)([^/]+\.ttf)$", url
    )
    if m:
        return m.group(1) + "static/" + m.group(2)
    return None


def fetch(url: str, retries: int = 3, timeout: int = 30) -> bytes:
    """
    Downloads a resource from a URL with basic retries and a standard User-Agent.

    Args:
        url: The URL to fetch.
        retries: The number of times to retry on failure.
        timeout: The timeout in seconds for the request.

    Returns:
        The downloaded content as bytes.

    Raises:
        RuntimeError: If all retries fail.
    """
    ctx = ssl.create_default_context()
    backoff = 1.0
    last_err: Exception | None = None
    for _ in range(retries):
        try:
            req = Request(url, headers={"User-Agent": UA})
            with urlopen(req, context=ctx, timeout=timeout) as resp:
                return resp.read()
        except (URLError, HTTPError, ssl.SSLError) as e:
            # On a 404 error, try the static fallback URL once.
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
    """
    Downloads a single file to a destination path.

    It checks if the file already exists and is valid. If not, it downloads
    the file to a temporary location before moving it to the final destination
    to ensure atomicity.

    Args:
        url: The URL to download.
        dest: The destination Path object.

    Returns:
        A tuple of (skipped, error_or_none). `skipped` is True if the
        destination file already existed. `error_or_none` is a string
        containing an error message on failure, otherwise None.
    """
    if dest.exists():
        try:
            if dest.stat().st_size >= MIN_BYTES:
                return True, None  # File exists and is large enough, skip.
        except OSError:
            pass  # File exists but can't be stat'd, proceed to download.
    try:
        data = fetch(url)
        if len(data) < MIN_BYTES:
            return False, f"Downloaded size too small: {len(data)} bytes"
        # Download to a temporary file first to avoid partial files.
        tmp = dest.with_suffix(dest.suffix + ".part")
        tmp.write_bytes(data)
        tmp.replace(dest)
        return False, None
    except Exception as e:
        return False, str(e)


def _css_family_param(name: str, axes: str, variants: list[tuple]) -> str:
    """
    Formats a single family's parameters for the Google Fonts CSS API URL.

    Args:
        name: The font family name (e.g., "Cormorant Garamond").
        axes: The axes string (e.g., "ital,wght").
        variants: The list of variant tuples (e.g., [(0, 400), (1, 700)]).

    Returns:
        A formatted string like "family=Cormorant+Garamond:ital,wght@0,400;0,700;1,400".
    """
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
        # Fallback for a basic request without specific axes.
        return f"family={fam}"


def build_css_url() -> tuple[str, list[str]]:
    """
    Builds a single, optimized Google Fonts CSS API v2 request URL for all families.

    Returns:
        A tuple containing the full CSS URL and a list of the family names requested.
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


# --- CSS Parsing Regular Expressions ---

# Regex to find `url(...)` declarations for .woff2 files in CSS.
CSS_WOFF2_RE = re.compile(
    r"url\((['\"]?)(?:(https?):)?//([^)'\"]+\.woff2)(?:\?[^)'\"]*)?\1\)"
)
# Regex to find `url(...)` declarations for .woff files (as a fallback).
CSS_WOFF_RE = re.compile(
    r"url\(((['\"]?)(?:(https?):)?//([^)'\"]+\.woff)(?:\?[^)'\"]*)?)\1\)"
)

# Regex to extract a full @font-face { ... } block.
FONTFACE_BLOCK_RE = re.compile(r"@font-face\s*\{(.*?)\}", re.DOTALL | re.IGNORECASE)
# Regex to extract the font-family property.
FAMILY_RE = re.compile(r"font-family:\s*(['\"])(.+?)\1\s*;", re.IGNORECASE)
# Regex to extract the font-style property.
STYLE_RE = re.compile(r"font-style:\s*(normal|italic)\s*;", re.IGNORECASE)
# Regex to extract the font-weight property.
WEIGHT_RE = re.compile(r"font-weight:\s*(\d+)\s*;", re.IGNORECASE)
# Regex to extract the unicode-range property.
UNICODE_RE = re.compile(r"unicode-range:\s*([^;]+);", re.IGNORECASE)


def _extract_url(block: str) -> tuple[str | None, str | None]:
    """
    Extracts a font file URL from a @font-face CSS block, preferring .woff2.

    Args:
        block: The text content of a single `@font-face` rule.

    Returns:
        A tuple of (url, extension) or (None, None) if no URL is found.
    """
    # Prefer WOFF2 as it's more modern and smaller.
    m2 = CSS_WOFF2_RE.search(block)
    if m2:
        scheme = m2.group(2) or "https"
        path = m2.group(3)
        return f"{scheme}://{path}", "woff2"
    # Fallback to WOFF if WOFF2 is not available.
    m1 = CSS_WOFF_RE.search(block)
    if m1:
        full = m1.group(1)
        # Re-run a simpler regex on the matched group for robustness.
        m = re.match(r"(['\"]?)(?:(https?):)?//([^?'\"]+\.woff)", full)
        if m:
            scheme = m.group(2) or "https"
            path = m.group(3)
            return f"{scheme}://{path}", "woff"
    return None, None


def parse_font_faces(css_text: str) -> list[dict]:
    """
    Parses a Google Fonts CSS string and extracts details for each @font-face rule.

    Args:
        css_text: The full CSS content from the Google Fonts API.

    Returns:
        A list of dictionaries, where each dictionary represents a parsed
        `@font-face` rule with its properties (family, style, weight, url, etc.).
    """
    faces: list[dict] = []
    for m in FONTFACE_BLOCK_RE.finditer(css_text):
        block = m.group(1)
        fam_m = FAMILY_RE.search(block)
        sty_m = STYLE_RE.search(block)
        w_m = WEIGHT_RE.search(block)
        if not (fam_m and sty_m and w_m):
            continue  # Skip blocks missing essential properties.

        url, ext = _extract_url(block)
        if not url:
            continue  # Skip blocks without a valid font URL.

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
                # Heuristic to prefer the Latin subset if available.
                "pref_latin": ("latin" in url.lower())
                or ("U+0000-00FF" in unicode_range.upper()),
            }
        )
    return faces


def _fam_key(name: str) -> str:
    """Generates a filesystem-friendly key from a font family name."""
    return re.sub(r"\s+", "", name)


def _friendly_name(family: str, italic: bool, weight: int, ext: str) -> str:
    """Creates a standardized, descriptive filename for a font variant."""
    fam = _fam_key(family)
    style_str = "-Italic" if italic else ""
    return f"{fam}{style_str}-{weight}.{ext}"


def _select_variants(faces: list[dict]) -> list[dict]:
    """
    Filters and selects the specific font variants needed by the application.

    It takes the list of all available font faces parsed from the CSS and
    matches them against the variants defined in the `FAMILIES` config.

    Args:
        faces: A list of all parsed font faces from `parse_font_faces`.

    Returns:
        A filtered list of dictionaries, where each dictionary represents a
        font to be downloaded and includes its destination filename.
    """
    wanted: list[dict] = []
    # Build a lookup table for quick access to font faces by their properties.
    by_key: dict[tuple[str, bool, int], list[dict]] = {}
    for fc in faces:
        fam = fc["family"]
        if fam not in FAMILIES:
            continue
        italic = fc["style"].lower() == "italic"
        key = (fam, italic, fc["weight"])
        by_key.setdefault(key, []).append(fc)

    # Iterate through the required families and variants.
    for fam, cfg in FAMILIES.items():
        axes = cfg.get("axes", "wght")
        variants = cfg.get("variants", [])
        for v in variants:
            if axes == "ital,wght":
                ital, w = v
                key = (fam, bool(ital), int(w))
            else:
                w = v[0]
                key = (fam, False, int(w))

            candidates = by_key.get(key, [])
            if not candidates:
                continue

            # From the candidates, prefer .woff2 and the Latin subset.
            candidates.sort(
                key=lambda x: (
                    0 if x["ext"] == "woff2" else 1,
                    0 if x["pref_latin"] else 1,
                )
            )
            picked = candidates[0]
            picked = dict(picked)  # Create a copy to modify.
            picked["dest_name"] = _friendly_name(fam, key[1], key[2], picked["ext"])
            wanted.append(picked)
    return wanted


def main() -> int:
    """The main execution function for the script."""
    print(f"Saving fonts to: {FONTS_DIR}")
    ok = 0
    skipped = 0
    errors: list[tuple[str, str]] = []

    css_url, _ = build_css_url()
    print(f"Requesting CSS: {css_url}")
    try:
        css = fetch(css_url).decode("utf-8", errors="replace")
    except Exception as e:
        print(f"Failed to fetch CSS: {e}")
        return 1

    # Write a debug copy of the CSS for troubleshooting.
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

    # Write a simple manifest for reference and debugging.
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
