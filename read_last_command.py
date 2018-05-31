#!/usr/bin/env python
# from io import StringIO
# import sys
import os
import re
import subprocess
from jinja2 import Environment, FileSystemLoader
import logging

from flask.logging import default_handler
BASE = os.path.dirname(os.path.abspath(__file__))

log = logging.getLogger()
log.addHandler(default_handler)

save_filename = os.path.join(BASE, 'saves', 'mysave2.qzl')

env = Environment(
    loader=FileSystemLoader('./')
)
template = env.get_template('templates/commands.txt')


def restart_game():
  # Delete any saved game files, etc
  if os.path.exists(save_filename):
    os.remove(save_filename)
  return send_command(None, restore=False)


top_line_pat = re.compile('^(?P<location>.+?) {3,}(?P<right_side>.*)$')
score_pat = re.compile('^Score: (?P<score>\d*)')


def parse_output(output, overwritten=True):
  back_pedal = -3
  if not overwritten:
    back_pedal = -3

  #print(output.decode('cp1252'))
  game_output = output.decode('cp1252').split('> >')
  #print(len(game_output))
  output = game_output[back_pedal].replace('\n. \n', '\r\n').strip()
  lines = output.splitlines()
  mm = top_line_pat.match(lines[0])
  matches = mm.groupdict()
  
  # Get first line which is he location on the left and
  # the score on the right. These pieces should be displayed differently in
  # chat than in Frotz

  score = 0
  score_match = score_pat.match(matches['right_side'])
  if score_match:
    score = score_match.groupdict().get('score')

  data = dict(
      location=matches['location'], 
      right_side=matches['right_side'], 
      text = '\r\n'.join(lines[1:]),
      score=score)
  return data


def send_command(command, restore=True):

  if command: 
      command = command.strip()

  overwrite = os.path.exists(save_filename)

  tout = template.render(command=command, save_filename=save_filename, restore=restore, overwrite=overwrite)

  log.debug('tout %s', tout)

  args = ['dfrotz','-x','-p','-S','0', './games/LostPig.z8']
  p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

  stdout, stderr = p.communicate(tout.encode('cp1252'))

  return parse_output(stdout, overwritten=overwrite)
