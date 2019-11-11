#!/bin/bash

# Royalnet must be installed with `develop`
VERSION=$(python3.7 -m royalpack.version)

rm -rf dist
python setup.py sdist bdist_wheel
twine upload "dist/{packname}-$VERSION"*
git add *
git commit -m "$VERSION"
git push
hub release create --message "Version $VERSION" --prerelease "$VERSION"
