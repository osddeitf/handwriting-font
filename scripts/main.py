import json
import argparse
from common import save_font

ASCII="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"


parser = argparse.ArgumentParser(argument_default='-h')
subparser = parser.add_subparsers(dest='command')

parser_template = subparser.add_parser('template', help="Generate template from existing font")
parser_template.add_argument('--letters', type=str, help="Selected letters", default=ASCII)
parser_template.add_argument('--size', type=str, required=True)
parser_template.add_argument('--scale', type=float, required=True)
parser_template.add_argument('--save-state', type=str)
parser_template.add_argument('input', type=str)
parser_template.add_argument('output', type=str)

parser_generate = subparser.add_parser('generate', help="Generate font from (modified) template")
parser_generate.add_argument('--state-file', type=str, help="Saved state filename")
parser_generate.add_argument('--sample-file', type=str, help="Sample file")
parser_generate.add_argument('--letters', type=str, help="Letters")
parser_generate.add_argument('--direction', type=str, default="horizontal")
parser_generate.add_argument('--size', type=str, help="(rows, columns)")
parser_generate.add_argument('--dimension', type=str, help="(width, height)")
parser_generate.add_argument('--scale', type=float)
parser_generate.add_argument('input', type=str)
parser_generate.add_argument('output', type=str)


options = vars(parser.parse_args())
command = options.pop('command')

if command == None:
  parser.print_help()
  exit(0)


def parse_tuple(s):
  return tuple([ int(x) for x in s.split(',') ])

if command == 'template':
  save_state = options.pop('save_state')
  options['size'] = parse_tuple(options['size'])
  
  from template import generate_template
  state = generate_template(**options)

  if save_state:
    with open(save_state, 'w') as f:
      json.dump(state, f)
  else:
    print(state)

elif command == 'generate':
  state = {}
  if options['state_file'] != None:
    with open(options['state_file']) as f:
      state = json.load(f)

  if options['sample_file']:
    state['sample'] = options['sample_file']
  if options['letters']:
    state['letters'] = options['letters']
  if options['direction']:
    state['direction'] = options['direction']
  if options['size']:
    state['rows'], state['columns'] = parse_tuple(options['size'])
  if options['dimension']:
    state['width'], state['height'] = parse_tuple(options['dimension'])
  if options['scale']:
    state['scale'] = options['scale']

  from process import generate_font
  font = generate_font(options['input'], state)
  save_font(font, options['output'])
