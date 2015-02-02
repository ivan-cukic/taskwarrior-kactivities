#!/usr/bin/python3

###############################################################################

# Location of the task executable
taskwarrior_bin="/usr/bin/task"

###############################################################################

import sys
import dbus
import re
from itertools import *
from subprocess import call

activities = dbus.SessionBus().get_object('org.kde.ActivityManager',
                                          '/ActivityManager/Activities')

# Returns the name of the activity formatted to fit the
# project name for TaskWarrior
def current_activity_slug():
    activity = activities.CurrentActivity()
    slug_base = activities.ActivityName(activity).lower()
    return re.sub(r"[^A-Za-z0-9]", "_", slug_base)

# Separates a list according to a predicate
def partition(pred, iterable):
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)

# Does the argument define a project?
def is_project_tag(tag):
    return tag.startswith("project:")

# By default, using the current activity name as the project
project_tag_present = False
project_name = "project:" + current_activity_slug()

other_tags, project_tag = partition(is_project_tag, sys.argv[1:])

# Adding the activity to the project name
# The activity slug would be prettier with dashes instead of
# underscores, but task warrior sometimes thinks we want to
# subtract strings...
for arg in project_tag:
    project_tag_present = True
    project_name = arg.replace("project:",
                               "project:" + current_activity_slug() + ":")

# Initial command
command = [taskwarrior_bin]

# If the first argument is 'all', then do not add the activity tag
other_tags   = list(other_tags)
all_mode     = other_tags and other_tags[0] == "all"
task_id_mode = other_tags and other_tags[0].isdigit()

if all_mode:
    # If the first argument is a number, it is (probably)
    # the id of a task, no need to do anything about the
    # project name. The task id identifies a task regardless
    # of the current activity.
    # We only need to act if one of the arguments was the
    # project

    # Removing the first argument ('all') if exists
    if other_tags:
        other_tags = other_tags[1:]

elif task_id_mode:
    # If the first argument is a number, it is (probably) the id
    # of a task, no need to do anything about the project name
    # unless the user has specified a project. In that case, we
    # still want to tag it with the activity name
    if project_tag_present:
        other_tags = other_tags + [project_name]

else:
    # Otherwise add the project tag to the start
    command = command + [project_name]

# Arguments to pass apart from the project tag
args = command + other_tags

# Running the task warrior
# print(args)
call(args)


