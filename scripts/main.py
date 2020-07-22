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
parser_template.add_argument('input', type=str)
parser_template.add_argument('output', type=str)

parser_generate = subparser.add_parser('generate', help="Generate font from (modified) template")
parser_generate.add_argument('--state', type=str, required=True, help="Saved state filename")
parser_generate.add_argument('input', type=str)
parser_generate.add_argument('output', type=str)


options = vars(parser.parse_args())
command = options['command']
del options['command']

if command == None:
  parser.print_help()
  exit(0)

if command == 'template':
  options['size'] = tuple([ int(x) for x in options['size'].split(',') ])
  
  from template import generate_template
  state = generate_template(**options)
  with open('state.json', 'w') as f:
    json.dump(state, f)

elif command == 'generate':
  with open(options['state']) as f:
    state = json.load(f)

  from process import generate_font
  font = generate_font(options['input'], state)
  save_font(font, options['output'])
