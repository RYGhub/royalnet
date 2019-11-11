#!/bin/bash

# Set me to your pack name!
PACKNAME="{packname}"

# Royalnet must be installed with `develop`
VERSION=$(python3.7 -m "$PACKNAME.version")

rm -rf dist
python setup.py sdist bdist_wheel
twine upload "dist/$PACKNAME-$VERSION"*
git add *
git commit -m "$VERSION"
git push
hub release create --message "Version $VERSION" --prerelease "$VERSION"
