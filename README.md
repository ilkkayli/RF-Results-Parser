# RF-Results-Parser

Purpose:
Used for gathering Robot Framework test results from Jenkins jobs and calculating overall pass rate.

Prerequisities:
Python
Change the locPage-variable to the url where your Jenkins jobs are.
Column named "Robot Results" added for every job on the web page.

Funtionalities:
Updates a log file that contains pass rate for a single date. One line per date.
It is possible to schedule this script to be run by Windows Task Scheduler.