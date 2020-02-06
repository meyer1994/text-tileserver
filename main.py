import string
from io import BytesIO
from collections import defaultdict

from PIL import Image, ImageFont, ImageDraw
from fastapi import FastAPI
from starlette.responses import StreamingResponse

app = FastAPI()

# Fake db
db = defaultdict(lambda: ' ')
for i in range(-1000, 1000):
    db[(0, i)] = string.ascii_lowercase[i % 26]
    db[(i, 0)] = string.ascii_lowercase[i % 26]
    db[(i, i)] = string.ascii_lowercase[i % 26]
    db[(-i, i)] = string.ascii_lowercase[i % 26]


# Some font
font = ImageFont.truetype('/usr/share/fonts/noto/NotoSansMono-Medium.ttf', 26)
mx, my = font.getsize('A')
mx = 256 // mx
my = (256 // my) - 1


@app.get('/{x}/{y}/{z}')
async def test(x: int, y: int, z: int):
    x *= mx
    y *= my

    size = (256, 256)
    img = Image.new('L', size, 0)
    draw = ImageDraw.Draw(img)

    lines = []
    for i in range(y, y + 8):
        line = ''.join(db[(j, i)] for j in range(x, x + 256 // mx))
        lines.append(line)

    text = '\n'.join(lines)
    draw.text((0, 0), text, 255, font=font)

    buff = BytesIO()
    img.save(buff, format='PNG')
    buff.seek(0)

    return StreamingResponse(buff, media_type='image/png')
