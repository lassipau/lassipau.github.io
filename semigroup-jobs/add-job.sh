#!/bin/sh

# sync the updated DPS-jobs database to github

git pull
git add dps-jobs.db
git commit -m "Added a job"
git push
