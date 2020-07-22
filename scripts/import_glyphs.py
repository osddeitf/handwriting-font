import os
from common import glyph_filename_base

def set_up_font_info(font, new_family_name="", new_font_name="", new_full_name="", em=1000, descent=200, ascent=800, **kwargs):
  font.encoding = 'UnicodeFull'
  font.fontname = new_font_name
  font.familyname = new_family_name
  font.fullname = new_full_name
  font.em = em
  font.descent = descent
  font.ascent = ascent
  return font

def import_glyphs(font=None, glyph_dir='glyphs', matrix=None, height=0, **kwargs):
  old_em = font.em
  font.em = height

  for row in matrix:
    for g in row:
      if g is None: continue
      try:
        base = glyph_filename_base(g.glyphname)
        svg_filename = os.path.join(glyph_dir, base + '.svg')
        png_filename = os.path.join(glyph_dir, base + '.png')
        g.clear()
        g.importOutlines(png_filename, scale=True)
        g.importOutlines(svg_filename, scale=True)
      except Exception as e:
        print("Error with ", g, e)
  font.em = old_em
  return font
