import json
import fontforge
from common import glyph_matrix
from cut_glyphs import cut_glyphs
from import_glyphs import import_glyphs
from set_bearings import set_bearings

with open('state.json', 'r') as f:
  state = json.load(f)

font = fontforge.open(state['sample'])
matrix = glyph_matrix(
  font=font,
  letters=state['letters'],
  direction=state['direction'],
  columns=state['columns'],
  rows=state['rows']
)

bearings = list(map(lambda g: [g.glyphname, g.left_side_bearing, g.right_side_bearing], font.glyphs()))

# Step 1: cut glyphs from modified template
cut_glyphs(
  matrix=matrix,
  height=state['height'],
  width=state['width'],
  scale=state['scale'],

  glyph_dir='glyphs',
  # sample_file='Roboto.png',
  sample_file='sachac.png',
  force=True,
)

# Step 2: Import cut glyphs
import_glyphs(
  font=font,
  matrix=matrix,
  height=state['height']
)

# Step 3: Set back bearings
font = set_bearings(font, bearings)

# TODO: Kern
# print(font.getKerningClass('kern-1'))

# Final step: produce font
save_font(font, 'output.sfd')
