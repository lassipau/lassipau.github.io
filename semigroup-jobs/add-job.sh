#!/bin/sh

# sync the updated Semigroup-jobs database to github

git pull
git add semigroup-jobs.db
git commit -m "Added a job"
git push
