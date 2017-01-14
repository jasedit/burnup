#!/usr/bin/env python3

import datetime
from itertools import accumulate

import argparse as ap
import plotly
import yaml

def load_project(file):
  with open(args.file, 'Ur') as fp:
    project = yaml.load(fp)
  return project

def save_project(project, file):
  with open(args.file, 'w') as fp:
      yaml.dump(project, fp)

def new_project(args):

  project = {
  'title': args.title,
  'stats': []
  }

  save_project(project, args.file)

def plot_rate(args):

  project = load_project(args.file)
  dates, counts = zip(*project['stats'])
  counts = accumulate(counts)

  plotly.offline.plot([plotly.graph_objs.Scatter(x=list(dates), y=list(counts))])

def add_burn(args):
  project = load_project(args.file)
  project['stats'].append((datetime.datetime.now(), args.count))

  save_project(project, args.file)

if __name__ == "__main__":
  prsr = ap.ArgumentParser()
  subprs = prsr.add_subparsers()

  newprsr = subprs.add_parser('new')

  newprsr.add_argument('title', help='Project Title')
  newprsr.add_argument('file', help='Location to save project')
  newprsr.set_defaults(func=new_project)

  rprsr = subprs.add_parser('rate')
  rprsr.add_argument('file', help='Project location')
  rprsr.set_defaults(func=plot_rate)

  addprser = subprs.add_parser('add')
  addprser.add_argument('file', help='Project location')
  addprser.add_argument('count', type=int, help='New count')
  addprser.set_defaults(func=add_burn)

  args = prsr.parse_args()


  if 'func' in args:
    args.func(args)