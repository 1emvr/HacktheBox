#!/usr/bin/env bash
# use pass + pass-git-helper credential store
git add .
git commit -m "$1"
git push
