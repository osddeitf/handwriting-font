import os
import subprocess
import numpy
import math
import fontforge
import libxml2
from PIL import Image
from common import glyph_filename_base, glyph_matrix

from svgpathtools import svg2paths2, wsvg

def compact(source, dest, px):
  paths, attributes, svg_attributes = svg2paths2(source)

  if len(paths) == 0:
    return

  # Get global bbox
  bboxes = numpy.array([
      # min_x, max_x, min_y, max_y
      path.bbox() for path in paths
  ])

  min_x, _____, min_y, _____ = numpy.min(bboxes, 0)
  _____, max_x, _____, max_y = numpy.max(bboxes, 0)

  min_x = math.floor(min_x)
  max_x = math.ceil(max_x)
  min_y = math.floor(min_y)
  max_y = math.ceil(max_y)

  # Bulk translate
  translated = [
      path.translated(complex(-min_x + px, 0))
      for path in paths
  ]

  wsvg(
    paths=translated,
    attributes=attributes,
    svg_attributes=svg_attributes,
    filename=dest
  )

def cut_glyphs(scale=None, matrix=None, sample_file="", height=0, width=0, glyph_dir='glyphs', force=False, **kwargs):
  # print(columns, rows, width, height)
  im = Image.open(sample_file).convert('1')
  if not os.path.exists(glyph_dir):
    os.makedirs(glyph_dir)

  for r, row in enumerate(matrix):
    top = r * height
    bottom = top + height
    for c, ch in enumerate(row):
      if ch is None: continue
      filename = os.path.join(glyph_dir, glyph_filename_base(ch.glyphname) + '.pbm')
      if os.path.exists(filename) and not force: continue
      
      left = c * width
      right = left + width
      small = im.crop((left, top, right, bottom))
      small.save(filename)
      # print(left, top, right, bottom)
      
      png = filename.replace('.pbm', '.png')
      small.save(png)

      svg = filename.replace('.pbm', '.svg')
      subprocess.call(['autotrace',
        # '-background-color', 'FFFFFF',
        '-output-file', svg, filename])
      
      doc = libxml2.parseFile(svg)
      root = doc.children
      child = root.children
      child.next.unlinkNode()
      doc.saveFile(svg)

      compact(svg, svg, ch.left_side_bearing * scale)
