from typing import List
import yaml
import os

class Row:
  __slots__ = ('header_name', 'rows', 'character_length')

  def __init__(self, header_name: str):
    self.header_name = header_name
    self.character_length = len(header_name)
    self.rows = []
  
  def append(self, row_contents: str):
    self.character_length = max(self.character_length, max(map(lambda content: len(list(content)), row_contents.splitlines())))
    self.rows.append(row_contents)
  
  def render(self, text: str):
    return f'{text}{" " * (self.character_length - len(text))}'

CHANGE_EMOJIS = {
  'add': chr(129001),
  'fix': chr(128998),
  'rem': chr(128997)
}

def render_lines(rows: List[Row], character: str = '-'):
  output = f'+{character}'
  last_idx = len(rows) - 1
  
  for idx, row in enumerate(rows):
    output += f'{character * (row.character_length + 1)}+'
    
    if idx != last_idx:
      output += character
  
  return output

def render_contents(rows: List[Row], idx: int):
  max_row_lines = max(*map(lambda row: len(row.rows[idx].splitlines()), rows))
  output = ''

  for current_idx in range(0, max_row_lines):
    last_row_idx = len(rows) - 1
  
    for row_idx, row in enumerate(rows):
      lines = row.rows[idx].splitlines()
      output += f'| {row.render(lines[current_idx] if lines[current_idx:] else "")}'
      
      if row_idx != last_row_idx:
        output += ' '
    
    output += '|\n'
  
  return output[:-1]

def render(rows: List[Row]):
  output = f'{render_lines(rows)}\n'

  for row in rows:
    output += f'| {row.render(row.header_name)} '
  
  output += f'|\n{render_lines(rows, "=")}\n'
  
  # All rows have the same length of rows, get it?
  last_row_idx = len(rows[0].rows) - 1
  
  for row_idx in range(0, last_row_idx + 1):
    output += f'{render_contents(rows, row_idx)}\n{render_lines(rows)}'
    
    if row_idx != last_row_idx:
      output += '\n'
  
  return output

versions = Row('Version')
release_dates = Row('Release date')
changes = Row('Changes')

with open(os.path.join(os.path.abspath('..'), 'changelog.yml')) as yml_stream:
  parsed_yml = yaml.safe_load(yml_stream)
  
  for stream in parsed_yml['changelog']:
    versions.append(stream['version'])
    release_dates.append(stream['release-date'])
 
    change_strings = []
    
    for change in stream['changes']:
      key = list(change.keys())[0]
      value = list(change.values())[0]
      
      change_strings.append(f'- {CHANGE_EMOJIS[key]} {value}')
    
    changes.append('\n'.join(change_strings))
  
  with open('changelog.rst', 'w', encoding='utf-8') as output:
    output.write(f'Changelog\n=========\n\n{render([versions, release_dates, changes])}')