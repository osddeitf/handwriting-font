import numpy as np
from PIL import Image, ImageFont, ImageDraw
from common import glyph_matrix

def draw_letter(draw, dx, dy, letter, font, params):

  def horz(x, y, color):
    draw.line((x, y, x + params['em_width'], y), fill=color, width=params['line_width'])

  def vert(x, y, color):
    draw.line((x, y, x, y + params['em']), fill=color, width=params['line_width'])

  # Gray box: top (ascent), bottom (descent), left, right
  horz(dx, dy, 'lightgray')
  horz(dx, dy + params['em'], 'lightgray')
  vert(dx, dy, 'lightgray')
  vert(dx + params['em_width'], dy, 'lightgray')
  
  # baseline, cap height, x-height
  horz(dx, dy + params['ascent'], 'red')
  horz(dx, dy + params['ascent'] - params['caps'], 'lightgreen')
  horz(dx, dy + params['ascent'] - params['x_height'], 'lightgray')

  # width, height = draw.textsize(letter, font=params['font'])
  width, height = letter.width, letter.vwidth
  draw.text((dx + (params['em_width'] - width) / 2, dy), chr(letter.unicode), font=font, fill=params['text_color'])


def make_template(sample, matrix, padding, params):
  px, py = padding
  rows, columns = np.array(matrix).shape

  img = Image.new('RGB', (columns * (px + params['em_width']), rows * (py + params['em'])), 'white')
  draw = ImageDraw.Draw(img)
  font = ImageFont.truetype(sample, params['em'])

  for r, row in enumerate(matrix):
    for c, ch in enumerate(row):
      # Top-left corner
      dx = c * (px + params['em_width'])
      dy = r * (py + params['em'])
      draw_letter(draw, dx, dy, ch, font, params)
  
  return img


params = {
  'em': 1000,
  'em_width': 1000,
  'x_height': 368,
  'caps': 650,
  'ascent': 800,
  #descent

  # Draw props
  'font_size': 1000, # = em
  'line_width': 3,
  'text_color': 'lightgray'
}


def gen(input, output, letters, size):
  rows, columns = size
  matrix = glyph_matrix(letters=letters, font=fontforge.open(input), rows=columns, columns=columns)
  img = make_template(input, matrix, (0, 0), params)
  ratio = 2
  width, height = img.size
  img.thumbnail((width / ratio, height / ratio))
  img.save(output)

# letters = 'HOnodpagscebhklftijmnruwvxyzCGABRDLEFIJKMNPQSTUVWXYZ0123456789?:;-–—=!\'’"“”@/\\~_#$%&()*+,.<>[]^`{|}q'
letters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ?:;-–—=!\'’"“”@/\\~_#$%&()*+,.<>[]^`{|}'
gen('assets/sachacHand.otf', 'template-sachacHand.png', letters, (10, 10))
print("Success")
