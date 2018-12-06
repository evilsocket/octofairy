#!/usr/bin/python3

# https://stackoverflow.com/questions/37558271/python-sklearn-deprecation-warning
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

import os
import sys
import argparse
import json
import glob
import numpy as np
from sklearn import preprocessing

def block_histogram(s):
    histogram = [0.0] * 256
    if s is None:
        return histogram
    l = len(s) 
    for byte in bytes(s.encode('utf-8')):
        histogram[byte] += 1
    return [x / float(l) if l is not 0 else 0 for x in histogram] 

def was_closed_with_commit(issue):
    for event in issue['events']:
        if event['event'] == 'closed' and event['commit_id'] is not None:
            return True
    return False

def get_classification(issue):
    if issue['state'] == 'open':
        return 0.0
    elif was_closed_with_commit(issue):
        return 1.0
    else:
        return 2.0

def to_vector(issue):
    v = []

    # len and histogram of the title
    v += [len(issue['title'])]
    v += block_histogram(issue['title'])
    # len and histogram of the body
    v += [len(issue['body']) if issue['body'] is not None else 0.0]
    v += block_histogram(issue['body'])
    # number of reactions
    v += [len(issue['reactions'])]
    # number of events
    v += [len(issue['events'])]
    # number of comments
    v += [issue['comments']]

    return get_classification(issue), np.asarray(v)
    
parser = argparse.ArgumentParser(description="Repository info download tool.")
parser.add_argument("--folder", dest = "folder", action = "store", type = str, required = True, help = "Folder of the JSON files.")
parser.add_argument("--to", dest = "output", action = "store", default = "data.csv", type = str, help = "Output file.")
args = parser.parse_args(sys.argv[1:])

args.folder = os.path.abspath(args.folder)
if not os.path.exists(args.folder):
    print("folder %s does not exists." % args.folder)
    quit()

issues = []
for filename in glob.glob( os.path.join( args.folder, "issue*.json") ):
    with open(filename, 'rt') as fp:
        issues.append( json.loads(fp.read()) )

print("vectorializing %d issues ..." % len(issues))

X = []
y = []

for issue in issues:
    label, x = to_vector(issue)
    X.append(x)
    y.append(label)

X = preprocessing.normalize(X)

data = []

for i, label in enumerate(y):
    data.append( np.concatenate(([label], X[i])) )

print("saving to %s ..." % args.output)

np.savetxt(args.output, data, delimiter=",")

