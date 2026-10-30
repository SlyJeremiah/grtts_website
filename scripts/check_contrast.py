"""Verify the GRTTS palette meets WCAG AA contrast requirements.

Reads the colour tokens straight out of static/css/grtts.css so the check can
never drift from the stylesheet, then tests the pairs the design system
actually puts on screen.

Usage:
    python scripts/check_contrast.py

Exits non-zero if any pair fails, so it can be wired into CI.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

CSS_PATH = Path(__file__).resolve().parent.parent / 'static' / 'css' / 'grtts.css'

WHITE = '#FFFFFF'

# (description, foreground token, background token, is_large_text)
PAIRS = [
    ('body text on white',                      'ink',          WHITE, False),
    ('muted text on white',                     'ink-muted',    WHITE, False),
    ('subtle text on white',                    'ink-subtle',   WHITE, False),
    ('link on white',                           'green-700',    WHITE, False),
    ('heading on white',                        'green-900',    WHITE, False),
    ('white on primary button',                 WHITE,  'green-700',   False),
    ('white on green-800',                      WHITE,  'green-800',   False),
    ('white on green-900',                      WHITE,  'green-900',   False),
    ('accent button text on gold',              'green-950', 'gold-500', False),
    ('eyebrow on white',                        'gold-700',     WHITE, False),
    ('eyebrow on inverse section',              'gold-300', 'green-900', False),
    ('stat value on inverse section',           'gold-400', 'green-900', True),
    ('stat note on inverse section',            'green-200', 'green-900', False),
    ('badge text on green tint',                'green-800', 'green-100', False),
    ('badge text on gold tint',                 'gold-800', 'gold-100',  False),
    ('danger text on white',                    'danger',       WHITE, False),
]


def parse_tokens(css: str) -> dict[str, str]:
    """Pull `--grtts-<name>: #RRGGBB;` declarations out of the stylesheet."""
    tokens: dict[str, str] = {}
    for name, value in re.findall(r'--grtts-([\w-]+):\s*(#[0-9A-Fa-f]{6})\s*;', css):
        tokens[name] = value
    return tokens


def relative_luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip('#')
    channels = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    r, g, b = linear
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg: str, bg: str) -> float:
    lighter, darker = sorted((relative_luminance(fg), relative_luminance(bg)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def resolve(token: str, tokens: dict[str, str]) -> str:
    if token.startswith('#'):
        return token
    try:
        return tokens[token]
    except KeyError:
        raise SystemExit(f'Token --grtts-{token} not found in {CSS_PATH.name}')


def main() -> int:
    css = CSS_PATH.read_text(encoding='utf-8')
    tokens = parse_tokens(css)

    print(f'{"pair":44} {"ratio":>7}  {"required":>8}  result')
    print('-' * 76)

    failures = 0
    for description, fg_token, bg_token, is_large in PAIRS:
        fg = resolve(fg_token, tokens)
        bg = resolve(bg_token, tokens)
        ratio = contrast_ratio(fg, bg)
        required = 3.0 if is_large else 4.5
        passed = ratio >= required
        failures += 0 if passed else 1
        print(f'{description:44} {ratio:6.2f}:1  {required:7.1f}:1  '
              f'{"PASS" if passed else "FAIL"}')

    print('-' * 76)
    if failures:
        print(f'{failures} pair(s) below the WCAG AA threshold.')
        return 1
    print(f'All {len(PAIRS)} pairs meet WCAG AA.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
