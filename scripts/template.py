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
  vert(dx, dy, 'lightgray')
  vert(dx + em, dy, 'lightgray')
  horz(dx, dy, 'gray')
  horz(dx, dy + em, 'gray')

  # baseline, cap height, x-height
  horz(dx, dy + ascent, 'red')
  horz(dx, dy + ascent - xHeight, 'lightblue')
  horz(dx, dy + ascent - capHeight, 'lightgreen')


def make_template(sample, size, scale, letters):
  rows, columns = size

  font = fontforge.open(sample)
  draw_font = ImageFont.truetype(sample, int(font.em * scale))
  matrix = glyph_matrix(letters=letters, font=font, rows=columns, columns=columns)
  
  ascent, descent = draw_font.getmetrics()
  em = ascent + descent
  xHeight = descent * (font.xHeight / font.descent)
  capHeight = descent * (font.capHeight / font.descent)

  img = Image.new('RGB', (em * columns, em * rows), 'white')
  draw = ImageDraw.Draw(img)

  for r, row in enumerate(matrix):
    for c, letter in enumerate(row):
      dx = em * c
      dy = em * r
      # Draw grid
      draw_grid(draw, dx, dy, line_width=3, em=em, ascent=ascent, capHeight=capHeight, xHeight=xHeight)

      text = chr(letter.unicode)
      x = dx + (em - draw_font.getsize(text)[0]) / 2
      y = dy
      draw.text((x, y), text, font=draw_font, fill='lightgray')
  
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
