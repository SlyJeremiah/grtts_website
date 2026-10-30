"""Generate the optimised icon and social-image set from the master logo.

The master artwork (static/images/logo.png) is a 523x442 circular emblem with
curved text around it. Shipping it unmodified costs ~180KB to render a 50px
navbar mark, which is the single heaviest asset on the site and matters on the
mobile connections much of this audience browses from.

Run after replacing the master logo:

    .venv/Scripts/python.exe scripts/build_assets.py

Outputs into static/images/:
    favicon.ico          16/32/48 multi-resolution
    logo-mark-96.png     navbar, 1x
    logo-mark-192.png    navbar, 2x
    apple-touch-icon.png 180x180, home-screen bookmark
    og-image.png         1200x630, social sharing card
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / 'static' / 'images'
MASTER = IMAGES / 'logo.png'

# Brand background for the social card — --grtts-green-900.
OG_BACKGROUND = (12, 43, 26, 255)
OG_SIZE = (1200, 630)


def square_crop(image: Image.Image) -> Image.Image:
    """Centre-crop to a square so the circular emblem is not clipped.

    `object-fit: cover` on a 523x442 source crops the left and right edges,
    which cuts through the curved wordmark. Cropping to a square here means
    the browser never has to.
    """
    width, height = image.size
    side = min(width, height)
    left = (width - side) // 2
    top = (height - side) // 2
    return image.crop((left, top, left + side, top + side))


def save_png(image: Image.Image, name: str) -> None:
    path = IMAGES / name
    image.save(path, 'PNG', optimize=True)
    print(f'  {name:24} {image.size[0]:>4}x{image.size[1]:<4} {path.stat().st_size / 1024:6.1f} KB')


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Best available sans font, falling back to PIL's bitmap default."""
    candidates = [
        'C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf',
        'C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold
        else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/System/Library/Fonts/Supplemental/Arial Bold.ttf' if bold
        else '/System/Library/Fonts/Supplemental/Arial.ttf',
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def build_social_card(mark: Image.Image) -> Image.Image:
    """1200x630 card: emblem in a white disc beside the wordmark.

    The master artwork has an opaque white background, so pasting it straight
    onto brand green leaves a white rectangle. Masking it to a circle keeps
    the dark curved wordmark on the light ground it needs while sitting
    cleanly on the green.
    """
    card = Image.new('RGBA', OG_SIZE, OG_BACKGROUND)

    disc_size = 430
    emblem = mark.resize((disc_size, disc_size), Image.LANCZOS)

    mask = Image.new('L', (disc_size * 4, disc_size * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, disc_size * 4 - 1, disc_size * 4 - 1), fill=255)
    mask = mask.resize((disc_size, disc_size), Image.LANCZOS)  # anti-aliased edge

    disc_x, disc_y = 70, (OG_SIZE[1] - disc_size) // 2
    card.paste(emblem, (disc_x, disc_y), mask)

    draw = ImageDraw.Draw(card)
    text_x = disc_x + disc_size + 60

    gold = (217, 180, 63, 255)
    white = (255, 255, 255, 255)
    pale = (169, 216, 187, 255)

    draw.text((text_x, 212), 'GRTTS', font=load_font(104, bold=True), fill=white)
    draw.text((text_x, 330), 'Game Ranger and Tracker', font=load_font(34), fill=pale)
    draw.text((text_x, 374), 'Training Specialist', font=load_font(34), fill=pale)
    draw.text((text_x, 436), 'TRAINING THAT SAVES LIVES',
              font=load_font(26, bold=True), fill=gold)

    return card


def main() -> int:
    if not MASTER.exists():
        print(f'Master logo not found: {MASTER}', file=sys.stderr)
        return 1

    master = Image.open(MASTER).convert('RGBA')
    print(f'master: {master.size[0]}x{master.size[1]}  '
          f'{MASTER.stat().st_size / 1024:.1f} KB\n')

    mark = square_crop(master)

    print('icons:')
    # Multi-resolution .ico. The previous favicon.ico was a single 256px frame
    # at 121KB; browsers only ever render it at 16-48px.
    ico_sizes = [(16, 16), (32, 32), (48, 48)]
    ico_path = IMAGES / 'favicon.ico'
    mark.resize((48, 48), Image.LANCZOS).save(ico_path, format='ICO', sizes=ico_sizes)
    print(f'  {"favicon.ico":24} {"16/32/48":>9}  {ico_path.stat().st_size / 1024:6.1f} KB')

    save_png(mark.resize((96, 96), Image.LANCZOS), 'logo-mark-96.png')
    save_png(mark.resize((192, 192), Image.LANCZOS), 'logo-mark-192.png')
    save_png(mark.resize((180, 180), Image.LANCZOS), 'apple-touch-icon.png')

    print('\nsocial:')
    save_png(build_social_card(mark), 'og-image.png')

    print('\nDone.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
