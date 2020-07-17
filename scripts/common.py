import numpy as np
import aglfn
import fontforge
import subprocess

params = {'template': 'template-256.png',
  'sample_file': 'sample.png',
  'name_list': 'aglfn.txt',
  'new_font_file': 'sachacHand.sfd',
  'new_otf': 'sachacHand.otf',
  'new_font_name': 'sachacHand',
  'new_family_name': 'sachacHand',
  'new_full_name': 'sachacHand',
  'text_color': 'lightgray',
  'glyph_dir': 'glyphs/',
  'letters': 'HOnodpagscebhklftijmnruwvxyzCGABRDLEFIJKMNPQSTUVWXYZ0123456789?:;-–—=!\'’"“”@/\\~_#$%&()*+,.<>[]^`{|}q',
  'direction': 'vertical',
 
  'em': 1000, 
  'em_width': 1000, 
  'x_height': 368,
  'caps': 650,
  'ascent': 800, 
  'descent': 200, 

  'rows': 10, 
  'columns': 10, 
  'row_padding': 0,
  'width': 500,
  'height': 500,
  'line_width': 3,

  'text': "Python+FontForge+Org: I made a font based on my handwriting!"
}
fontforge.loadNamelist(params['name_list'])
params['font_size'] = int(params['em'])
params['baseline'] = params['em'] - params['descent']

def transpose_letters(letters, width, height):
  return ''.join(np.reshape(list(letters.ljust(width * height)), (height, width)).transpose().reshape(-1))

# Return glyph name of s, or s if none (possibly variant)
def glyph_name(s):
  return aglfn.name(s) or s

def get_glyph(font, g):
  pos = font.findEncodingSlot(g)
  if pos == -1:
    return font.createChar(pos, g)
  else:
    return font[pos]

def glyph_matrix(font=None, matrix=None, letters=None, rows=0, columns=0, direction='horizontal', **kwargs):
  if matrix:
    if isinstance(matrix[0], str):
      # Split each
      matrix = [x.split(',') for x in matrix]
    else:
      matrix = matrix[:]  # copy the list
  else:
    matrix = np.reshape(list(letters.ljust(rows * columns)), (rows, columns))
    if direction == 'vertical':
      matrix = matrix.transpose()
  matrix = [[glyph_name(x) if x != 'None' else None for x in row] for row in matrix]
  if font:
    for r, row in enumerate(matrix):
      for c, col in enumerate(row):
        if col is None: continue
        matrix[r][c] = get_glyph(font, col)
  return matrix

def glyph_filename_base(glyph_name):
  try:
    return 'uni%s-%s' % (hex(ord(aglfn.to_glyph(glyph_name))).replace('0x', '').zfill(4), glyph_name)
  except:
    return glyph_name

def load_font(params):
  if type(params) == str:
    return fontforge.open(params)
  else:
    return fontforge.open(params['new_font_file'])

def save_font(font, font_filename=None, **kwargs):
  if font_filename is None:
    font_filename = font.fontname + '.sfd'
  font.save(font_filename)
  font.generate(font_filename.replace('.sfd', '.otf'))
  subprocess.call(['sfnt2woff', font_filename.replace('.sfd', '.otf')])
