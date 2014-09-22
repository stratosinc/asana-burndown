#!/usr/bin/env python

import os

from prettyprint import pp
from asana import asana

WORKSPACE_NAME = "getprotean.com"
ENGINEERING_TEAM = "Engineering"

api = asana.AsanaAPI(os.environ.get('ASANA_API_KEY'), debug=False)

workspace = None
for workspace_attrs in api.list_workspaces():
    if workspace_attrs['name'] == WORKSPACE_NAME:
        workspace = workspace_attrs

projects = {}
for project_attrs in api.list_projects(workspace['id'], include_archived=False):
    project = api.get_project(project_attrs['id'])
    if project['team']['name'] == ENGINEERING_TEAM:
        projects[project['id']] = project

for project in projects.values():
    tasks = api.get_project_tasks(project['id'])
    project['tasks'] = {}
    for task_attrs in tasks:
        task_id = task_attrs['id']
        project['tasks'][task_id] = api.get_task(task_id)

for project in projects.values():
    tasks = project.get('tasks', {}).values()
    open_tasks = [task for task in tasks if not task['completed']]
    closed_tasks = [task for task in tasks if task['completed']]
    print("{:<32} - Open: {:d} Closed: {:d}".format(
        project['name'][:32], len(open_tasks), len(closed_tasks)))
