# GRTTS Design System

Defined in `static/css/grtts.css`. Load order is
`bootstrap.min.css` → `grtts.css` → `style.css`.

The primary reader of this site is a landowner, NGO or conservancy deciding
whether GRTTS can be trusted with an armed deployment contract. The system
favours clarity, contrast and restraint over decoration.

## How it works today

`grtts.css` does two jobs:

1. **Defines the tokens and components** (`grtts-` prefixed classes) that
   templates will be rewritten against.
2. **Bridges those tokens onto Bootstrap 5.3's own CSS custom properties**
   (`--bs-primary`, `--bs-body-color`, `--bs-font-sans-serif` and friends), so
   the existing Bootstrap markup picks up the brand immediately rather than
   waiting for every template to be rewritten.

Section 2 of the stylesheet — the Bootstrap bridge — is deliberately
temporary. Delete it once no template depends on Bootstrap components.

## Colour

Green is the brand. Gold is an accent and is **never** a surface for body
text; on white, use `--grtts-gold-700` or darker for anything that must be
read.

### Verified contrast ratios

Measured with the WCAG 2.1 relative luminance formula. AA requires 4.5:1 for
normal text and 3:1 for large text (18.66px bold or 24px regular).

| Pair | Ratio | AA normal | AA large |
|---|---:|---|---|
| `--grtts-ink` on white | 16.8:1 | PASS | PASS |
| `--grtts-ink-muted` on white | 7.3:1 | PASS | PASS |
| `--grtts-ink-subtle` on white | 4.8:1 | PASS | PASS |
| `--grtts-green-700` link on white | 8.6:1 | PASS | PASS |
| `--grtts-green-900` heading on white | 15.3:1 | PASS | PASS |
| White on `--grtts-green-700` (primary button) | 8.6:1 | PASS | PASS |
| White on `--grtts-green-800` | 11.8:1 | PASS | PASS |
| White on `--grtts-green-900` | 15.3:1 | PASS | PASS |
| `--grtts-green-950` on `--grtts-gold-500` (accent button) | 7.2:1 | PASS | PASS |
| `--grtts-gold-700` eyebrow on white | 5.1:1 | PASS | PASS |
| `--grtts-gold-300` eyebrow on `--grtts-green-900` | 9.7:1 | PASS | PASS |
| `--grtts-gold-400` stat on `--grtts-green-900` | 7.7:1 | PASS | PASS |
| `--grtts-green-200` note on `--grtts-green-900` | 9.6:1 | PASS | PASS |
| `--grtts-green-800` on `--grtts-green-100` (badge) | 9.6:1 | PASS | PASS |
| `--grtts-gold-800` on `--grtts-gold-100` (badge) | 6.6:1 | PASS | PASS |
| `--grtts-danger` on white | 7.9:1 | PASS | PASS |

Re-run the check after changing any colour token:

```bash
.venv/Scripts/python.exe scripts/check_contrast.py
```

### Rules

- Every green at 500 and darker is a safe background for white text.
- Gold 500 and lighter needs dark text (`--grtts-green-950`), never white.
- Text over photography must sit inside `.grtts-overlay`, which applies a
  gradient scrim so legibility does not depend on the image.

## Typography

System font stack — no webfont request. Much of this audience browses on
mobile connections where a 200KB font blocks the first paint.

Modular scale at 1.250 (major third) from a 16px base. Headings use
`clamp()` so they scale with the viewport without breakpoint jumps.

**Body copy is never set in uppercase.** The previous site set whole
paragraphs in capitals, which measurably slows reading. Uppercase is confined
to `.grtts-eyebrow`, `.grtts-badge` and `.grtts-stat__label` — short labels
only, always with `--grtts-tracking-caps` letter-spacing.

Long-form text goes in `.grtts-prose`, capped at `--grtts-measure` (68ch).

## Spacing

4px base. Use the `--grtts-space-*` tokens rather than arbitrary values:

| Token | Value | Typical use |
|---|---|---|
| `--grtts-space-1` … `-3` | 4–12px | Inside controls, gaps between label and field |
| `--grtts-space-4` … `-5` | 16–24px | Card padding, stack rhythm |
| `--grtts-space-6` … `-7` | 32–48px | Between content blocks |
| `--grtts-space-8` … `-10` | 64–128px | Section padding |

## Components

| Class | Purpose |
|---|---|
| `.grtts-container` | Page width, 1200px max, 16px side gutter |
| `.grtts-section` | Vertical rhythm; `--sunken` and `--inverse` variants |
| `.grtts-grid` | Auto-fitting responsive grid, no breakpoint classes needed |
| `.grtts-stack` | Consistent vertical spacing between children |
| `.grtts-eyebrow` | Small uppercase section label |
| `.grtts-btn` | `--primary`, `--accent`, `--outline`, `--on-dark`, `--lg`, `--sm` |
| `.grtts-card` | Content card; `--interactive` adds hover lift |
| `.grtts-stat` | Headline figure; adapts automatically on inverse sections |
| `.grtts-badge` | Status pill; `--accent`, `--neutral` |
| `.grtts-field` / `.grtts-input` | Form controls, 44px min target, 16px text |
| `.grtts-alert` | `--success`, `--warning`, `--danger`, `--info` |
| `.grtts-overlay` | Gradient scrim for text over photography |

## Accessibility commitments

- All interactive targets are at least 44×44px.
- Inputs are 16px, which stops iOS zooming the viewport on focus.
- Focus is always visible: a 3px gold outline with 2px offset, applied via
  `:focus-visible` so it does not appear on mouse clicks.
- `prefers-reduced-motion: reduce` disables animation and transitions.
- The viewport meta no longer sets `maximum-scale`, so pinch-zoom works.
- `.grtts-skip-link` is available for skip-to-content.

## Not yet done

- **Dark mode.** Tokens are structured for it, but no dark theme is defined.
  This is a light marketing site; adding one is a decision, not an oversight.
- **Template rewrite.** Phase 1 ships the system and the Bootstrap bridge.
  Templates still use Bootstrap markup and ~1,000 lines of inline `<style>`
  in `base.html` and `home.html` remain to be removed.
