"""
Sample implementation of a CLI wrapper with QA-Board.
"""
import re
import sys
import json
import subprocess
from pathlib import Path

import click

def slugify(s):
  return s.strip().lower().replace(" ", "_").replace("(", "").replace(")", "").replace(",", "")

def get_histogram_data(lines, cutoff=None):
  # https://plotly.com/javascript/bar-charts/
  x = []
  y = []
  for line in lines:
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
  testname = context.params.get('testname')
  if not testname:
    click.secho("You must specify a sysbench testname: XXX in your config:", fg='red', bold=True)
    click.secho("Options: oltp_*.lua, fileio, cpu, memory, threads, mutex", fg='red')
    return {"is_failed": True}

  options = ' '.join(
    [f"--{key}={value}" if not isinstance(value, bool) else f"--{key}"
    for key, value in context.params.items()
    if key not in ('testname', 'prepare', 'clean', 'command')
  ])

  commands = [
    f"sysbench {testname} prepare" if context.params.get('prepare') else None,
    f"sysbench {testname} run {options} {context.params.get('command', '')}",
    f"sysbench {testname} clean" if context.params.get('clean') else None,
  ]
  commands = [c for c in commands if c]
  command = ' && '.join(commands)
  click.secho(command, fg='cyan')
  if context.dryrun:
    return {"is_failed": False}

  lines = []
  # https://stackoverflow.com/questions/803265/getting-realtime-output-using-subprocess
  process = subprocess.Popen(
    command,
    shell=True,
    cwd=context.input_path if testname == 'fileio' else Path(),
    encoding='utf-8',
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    bufsize=1,
    errors='replace',
  )
  while True:
      line = process.stdout.readline()
      if line == '' and process.poll() is not None:
          break
      if line:
        # remove noise...
        if "test_file" in line or "|" in line:
          continue
        print(line.strip(), flush=True)
        lines.append(line)
  returncode = process.poll()

  # Parse the metrics with some aweful code
  metrics = {}
  section = ""
  for line in lines:
    # print(line)
    try:
      *metric_parts, value_str = line.split()
      metric = '_'.join(metric_parts)
      assert metric[-1] == ':'
      metric = metric[:-1]
      metric = slugify(metric)
      if 'avg/stddev' in metric:
        v_avg_str, v_stddev_str = value_str.split('/')
        v_avg, v_stddev = float(v_avg_str), float(v_stddev_str)
        m = metric.replace("_avg/stddev", "")
        metrics[f"{m}_avg"] = v_avg
        metrics[f"{m}_stddev"] = v_stddev
      else:
        value = float(value_str.replace("s", ""))
        if metric in ('min', 'avg', 'max', 'sum', '95th_percentile'):
          metric = f"{section}_{metric}"
        metrics[metric] = value
        # print(f"METRIC {metric} : {value}")
    except Exception as e:
      # print(e)
      if ':' in line:
        section = line.split(':', maxsplit=1)[0]
        section = slugify(section)



  histogram_data = get_histogram_data(lines) #, 5 * metrics["avg"])
  with (context.output_dir / 'latency.plotly.json').open('w') as f:
    json.dump(histogram_data, f)

  return {
    "is_failed": process.returncode != 0,
    **metrics,
  }
