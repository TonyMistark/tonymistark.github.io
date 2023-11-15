#!/bin/sh

cd ./public
ls -al
git add -f .
git commit -m "Site deployed by GitHub Actions"
echo " ---->> finishe commit ----->>"
git checkout -b hexo
git remote add origin git@github.com:TonyMistark/tonymistark.github.io.git
git push origin hexo -f
