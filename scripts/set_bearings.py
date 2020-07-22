import re

# Return glyph name without .suffix
def glyph_base_name(x):
  m = re.match(r"([^.]+)\..+", x)
  return m.group(1) if m else x

def set_bearings(font, bearings, **kwargs):
  bearing_dict = {}
  for row in bearings: #[1:]:
    bearing_dict[row[0]] = row
  for g in font:
    key = font[g].glyphname
    m = glyph_base_name(key)
    if not key in bearing_dict:
      if m and m in bearing_dict:
        key = m
      else:
        key = 'Default'
    if bearing_dict[key][1] != '':
      font[g].left_side_bearing = bearing_dict[key][1]
    else:
      font[g].left_side_bearing = bearing_dict['Default'][1]
    if bearing_dict[key][2] != '':
      font[g].right_side_bearing = bearing_dict[key][2]
    else:
      font[g].right_side_bearing = bearing_dict['Default'][2]
  if 'space' not in bearing_dict:
    space = font.createMappedChar('space')
    space.width = int(font.em / 5)
  return font
