#!/bin/bash

# Usage: ./release.sh [version]
# If version is not provided, it will be extracted from setup.py

# Make sure we're on main branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" != "main" ] && [ "$BRANCH" != "master" ]; then
  echo "You must be on the main or master branch to release"
  exit 1
fi

# Ensure the working directory is clean
if [ -n "$(git status --porcelain)" ]; then
  echo "Your working directory is not clean. Commit or stash changes first."
  exit 1
fi

# Extract version from setup.py
SETUP_VERSION=$(grep -o 'version="[^"]*"' setup.py | cut -d'"' -f2)

if [ -z "$SETUP_VERSION" ]; then
  echo "Failed to extract version from setup.py"
  exit 1
fi

# If version parameter is provided, check that it matches setup.py
if [ -n "$1" ]; then
  if [ "$1" != "$SETUP_VERSION" ]; then
    echo "Error: Provided version ($1) doesn't match version in setup.py ($SETUP_VERSION)"
    echo "Please update setup.py first or omit the version parameter."
    exit 1
  fi
  VERSION=$1
else
  VERSION=$SETUP_VERSION
fi

# Run tests
echo "Running tests..."
python -m pytest
if [ $? -ne 0 ]; then
  echo "Tests failed. Fix them before releasing."
  exit 1
fi

# Confirm with the user
echo "This will create and push tag v$VERSION based on version in setup.py."
read -p "Do you want to continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Release canceled."
  exit 1
fi

# Add version tag
git tag -a "v$VERSION" -m "Release version $VERSION"

# Push the tag
git push origin "v$VERSION"

echo "Tag v$VERSION created and pushed."
echo "GitHub Actions workflow should now start automatically."
echo "Check the status at: https://github.com/ishiland/geosupport-suggest/actions"