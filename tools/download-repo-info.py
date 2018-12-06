#!/usr/bin/python3

import os
import re
import sys
import argparse
import json

from github import Github

parser = argparse.ArgumentParser(description="Repository info download tool.")
parser.add_argument("--repo", dest = "repo_url", action = "store", type = str, required = True, help = "URL of the github repo.")
parser.add_argument("--to", dest = "folder", action = "store", type = str, help = "Destination folder. If not specified, it'll be created depending on the repo name.")
parser.add_argument("--api-token", dest = "api_token", action = "store", type = str, help = "GitHub API token.")
args = parser.parse_args(sys.argv[1:])


m = re.findall( r'^.*github\.com/([^/]+)/([^/\?]+)$', args.repo_url )
if len(m) == 0:
    print("%s is not a valid github.com URL." % args.repo_url)
    quit()

ghub = Github(args.api_token)
owner_name, repo_name = m[0]
repo = ghub.get_repo("%s/%s" % (owner_name, repo_name))

if args.folder is None:
    args.folder = os.path.abspath('./github.com/%s/%s' % (owner_name, repo_name))
else:
    args.folder = os.path.abspath(args.folder)

if os.path.exists(args.folder):
    print("folder %s already exists." % args.folder)
    quit()

print("creating folder %s ..." % args.folder)

os.makedirs(args.folder, exist_ok=True)

for issue in repo.get_issues(state='all'):
    filename = os.path.join(args.folder, "issue%d.json" % issue.number)
    print("saving %s ..." % filename)
    ji = issue.raw_data
    ji['reactions'] = []
    ji['events'] = []

    for reaction in issue.get_reactions():
        try:
            ji['reactions'].append( reaction.raw_data )
        except Exception as e:
            print("%s" % str(e))

    for event in issue.get_events():
        try:
            ji['events'].append( event.raw_data )
        except Exception as e:
            print("%s" % str(e))
    
    with open(filename, 'w+t') as fp:
        fp.write(json.dumps(ji))
