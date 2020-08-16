"""
Sample implementation of a CLI wrapper with QA-Board.
"""
import re
import sys
import json
import subprocess
from pathlib import Path

import click


def get_histogram_data(logs, cutoff=None):
  # https://plotly.com/javascript/bar-charts/
  x = []
  y = []
  for line in logs.splitlines():
    if '|' not in line:
      continue
    value_str, bar, count = line.split()
    value = float(value_str)
    if cutoff and value > cutoff: # ignore outliers
      continue
    x.append(float(value))
    y.append(float(count))
  return {
    "data": [{
      "type": "bar",
      "x": x,
      "y": y,
    }],
    "layout": {
      "xaxis": {
        "title": 'Latency (ms)',
        "type": "log",
        "range": [-2, 2],
      },
      "yaxis": {
        "type": "log",
      },
    }
  }



def run(context):
  """
  Runs you code, creates files under context.output_dir, and returns metrics.
  """
  command = ' && '.join([
    "sysbench fileio prepare",
    "sysbench fileio --file-test-mode=rndrw run --histogram",
  ])
  click.secho(command, fg='cyan')
  if context.dryrun:
    return {"is_failed": False}

  process = subprocess.run(
    command,
    shell=True,
    cwd=context.input_path,
    encoding='utf-8',
    capture_output=True,
  )

  metrics = {}
  for line in process.stdout.splitlines():
    # remove noise...
    if "test_file" in line or "|" in line:
      continue

    # get the metrics
    try:
      metric, value_str = line.split()
      assert metric[-1] == ':'
      metric = metric[:-1]
      value = float(value_str)
      metrics[metric] = value
    except:
      pass
    print(line)
  
  
  histogram_data = get_histogram_data(process.stdout) #, 5 * metrics["avg"])
  with (context.output_dir / 'latency.plotly.json').open('w') as f:
    json.dump(histogram_data, f)

  return {
    "is_failed": process.returncode != 0,
    **metrics,
  }
