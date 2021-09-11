#!/bin/bash

helpFunction() {
  echo "Usage:  $0 command version"
  echo "Example ./release.sh perform 1.0.0 1.0.1"
  echo "Example ./release.sh checkout 1.0.0"
  echo ""
  echo -e "\tperform:  tag current release and prepare next one"
  echo -e "\tcheckout: checkout release for deployment"
  echo ""
  echo "relase-version.json"
  cat release-version.json
  exit 1
}

if [ -z "$1" ]; then
  helpFunction
fi

if [ "$1" == "perform" ]; then
  echo "Selected $2:"

  prev_version=$(jq -r '.version' release-version.json)
  tag_name="pyaws-$prev_version"
  echo "Releasing $prev_version, tagging $tag_name"

  echo "1. Reset hard to origin master"
  git reset --hard origin/master

  echo "2. Pulling changes"
  git pull origin master

  echo "3. Tagging "
  git tag "$tag_name"
  git push origin "$tag_name"
  git push --follow-tags

  echo "4. Push changes to release version:"
  echo "{\"version\": \"$3\"}" > release-version.json
  git add release-version.json
  git commit -m "Preparing next release $3"
  git push origin master
  exit 0
fi

if [ "$1" == "checkout" ]; then
 echo "Selected $1:"
 tag_name="pyaws-$2"
 branch_name="branch-install-$tag_name"
 git reset --hard origin/master
 git clean -f -d
 git pull origin master
 git fetch -p
 git checkout -b "$branch_name" "$tag_name"
 echo "Switched to the: $branch_name"
fi