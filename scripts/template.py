import fontforge
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from common import glyph_matrix

def draw_grid(draw, dx, dy, *, line_width, em, ascent, capHeight, xHeight):

  def horz(x, y, color):
    xy = np.array((x, y, x + em, y))
    draw.line(tuple(xy), fill=color, width=line_width)

  def vert(x, y, color):
    xy = np.array((x, y, x, y + em))
    draw.line(tuple(xy), fill=color, width=line_width)

  # Gray box: left, right, top (ascent), bottom (descent)
  vert(dx, dy, '#f2f2f2')
  vert(dx + em, dy, '#f2f2f2')
  horz(dx, dy, '#f2f2f2')
  horz(dx, dy + em, '#f2f2f2')

  # baseline, cap height, x-height
  horz(dx, dy + ascent, '#f2f2f2')
  horz(dx, dy + ascent - xHeight, '#f2f2f2')
  horz(dx, dy + ascent - capHeight, '#f2f2f2')


def make_template(sample, size, scale, letters):
  padding = 100
  rows, columns = size

  font = fontforge.open(sample)
  draw_font = ImageFont.truetype(sample, int(font.em * scale))
  matrix = glyph_matrix(letters=letters, font=font, rows=columns, columns=columns)
  
  ascent, descent = draw_font.getmetrics()
  em = ascent + descent
  xHeight = descent * (font.xHeight / font.descent)
  capHeight = descent * (font.capHeight / font.descent)

  img = Image.new('RGB', (em * columns + columns * padding * 2, em * rows + rows * padding * 2), 'white')
  draw = ImageDraw.Draw(img)

  for r in range(rows):
    y = r * (em + padding * 2)
    draw.line((0, y, img.width, y), width=3, fill="#aaaaaa")

  for c in range(columns):
    x = c * (em + padding * 2)
    draw.line((x, 0, x, img.height), width=3, fill="#aaaaaa")

  for r, row in enumerate(matrix):
    for c, letter in enumerate(row):
      dx = em * c + c * padding * 2 + padding
      dy = em * r + r * padding * 2 + padding
      # Draw grid
      draw_grid(draw, dx, dy, line_width=3, em=em, ascent=ascent, capHeight=capHeight, xHeight=xHeight)

      text = chr(letter.unicode)
      x = dx + (em - draw_font.getsize(text)[0]) / 2
      y = dy
      draw.text((x, y), text, font=draw_font, fill='#f2f2f2')
  
  return img


def generate_template(input, output, letters, size, scale):
  rows, columns = size
  img = make_template(input, size, scale, letters)
  img.save(output)

  # Save state
  return {
    'sample': input,
    'letters': letters,
    'direction': 'horizontal',
    'rows': rows,
    'columns': columns,
    'height': img.size[0] // rows,
    'width': img.size[1] // columns,
    'scale': scale
  }
