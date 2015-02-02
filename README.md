# taskwarrior-kactivities
TaskWarrior wrapper to allow goruping tasks by activity (KDE)

## Usage

First of all, it is advisable to place the script somewhere in your $PATH
(or create a shell alias) and rename it to something easier to type than
task.py. My personal preference is to call it just 't'.

If you run the command like you would run the regular TaskWarrior,
it will behave exactly like TaskWarrior apart from filtering the
results to show only the tasks for the current activity.

If you want to give a command that should affect (or list) all tasks
regardless of the activity they belong to, you need to pass 'all'
as the first argument for the script (or just call TaskWarrior directly).

```
    # Shows the tasks for the current activity
    t

    # Shows all tasks, regardless of the activity they belong to
    t all

    # Creates a new task for the current activity
    t add Update the README.md file

    # Creates a new task for the project inside the current activity
    t add Update the README.md file project:TaskWarriorWrapper
```

## What does it do

The script only modifies the arguments given to it, and passes them
to the TaskWarrior. In essence, it just prefixes the project name
with the name of the activity, if you specify the project name;
otherwise, it uses the activity name as the project name.

For example, if the current activity is called 'TaskWarrior Development'

```
    t add Update the README.md file
        -> becomes task add project:taskwarrior_development Update the README.md file

    t add Update the README.md file project:documentation
        -> becomes task add project:taskwarrior_development:documentation Update the README.md file
```

## Requirements

This script is written in Python 3. It only requires the dbus module
to be installed.

