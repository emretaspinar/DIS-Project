# How to run
1. use docker-compose-up in the directory with the Dockerfile (if you haven't moved the readme it is this directory)

## troubleshooting on windows
If it doesn't work have you tried starting WSL?
If it still doesn't work have you tried starting Dockerdesktop?

If it still doesn't work contact a docker expert, we didn't run into any problems that couldn't be fixed in one of those ways.

If you are on mac or linux and it doesn't work conact a docker expert, we ran the container on a windows machine.

If it still doesn't work you can watch this video of it working: https://youtu.be/liQUAuYwMUY

# Where to find an SQL statement
The easiest place to find an SQL statement is in database.py, for example there is one on line 41

# Where to find a regular expression
There is a regular expression in models/team.py on line 13

# Features
You can search for teams on the teams page
You can see stats about the teams
If you click on a team you can see the players for the team and some stats about them
If you click on the matches button on the players page you can see the matches their team has played and some stats about them
If you click on the players button on the matches page you can return to the players page
If you click on the home button on either the matches or players page you return to the teams page 
