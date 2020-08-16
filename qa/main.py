"""
Sample implementation of a CLI wrapper with QA-Board.
"""
import sys
import subprocess
from pathlib import Path

import click



def run(context):
  """
  Runs you code, creates files under context.output_dir, and returns metrics.
  """
  command = ' && '.join([
    "sysbench fileio prepare",
    "sysbench fileio --file-test-mode=rndrw run",
  ])
  click.secho(command, fg='cyan')
  if context.dryrun:
    return {"is_failed": False}
  process = subprocess.run(
    command,
    shell=True,
    cwd=context.input_path,
    encoding='utf-8',
  )
  if process.returncode != 0:
    return {"is_failed": True, "returncode": process.returncode}
  return {"is_failed": False}
