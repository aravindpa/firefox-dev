#!/bin/bash

# Exit script if any commands return errors. Treat unset variables as an error.
set -eu

# Find the version number and commit hash of the latest Firefox Aurora release.
echo "*** Looking up the latest release..."
curl "https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-aurora/" -o index.html
export VERSION_NUMBER=$(grep -Eo 'firefox-[[:digit:]]+\.[[:alnum:]]+' -m 1 index.html | grep -Eo '[[:digit:]]+\.[[:alnum:]]+' -m 1)
curl "https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-aurora/firefox-$VERSION_NUMBER.en-US.linux-x86_64.txt" -o firefox-latest-info.txt
export DATE=$(grep -Eo '[[:digit:]]{8}' -m 1 firefox-latest-info.txt)
export VERSION_DATE=$VERSION_NUMBER.$DATE
export LATEST_COMMIT=$(basename $(tail -n1 firefox-latest-info.txt))
rm index.html firefox-latest-info.txt
export DOWNLOAD_SOURCE_URL="https://hg.mozilla.org/releases/mozilla-aurora/archive/$LATEST_COMMIT.tar.bz2"

echo
echo "Latest commit: $LATEST_COMMIT"
echo "Version:       $VERSION_DATE"

# Update the spec file to use latest Firefox release.
sed -i -r "s/^(Version:[[:space:]]+)[[:digit:]]+\.[[:alnum:]]+\.[[:digit:]]+/\1$VERSION_DATE/" firefox-dev.spec
sed -i -r "s/^(%define revision[[:space:]]+)[[:alnum:]]+/\1$LATEST_COMMIT/" firefox-dev.spec

# Get the source code for the latest Firefox release.
echo
echo "*** Downloading latest release of Firefox Aurora..."
curl -O "$DOWNLOAD_SOURCE_URL"

# Get the langpacks too.
mkdir -p firefox-langpacks
cd firefox-langpacks
curl "https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-aurora-l10n/linux-x86_64/xpi/" -o index.html
echo
echo "*** Downloading langpacks for Firefox..."
grep -Eo "\".*?firefox-$VERSION_NUMBER.*?\.xpi\"" index.html | sed -r 's/"(.*)"/https:\/\/archive.mozilla.org\1/g' | xargs wget
rm index.html
echo
echo "*** Repacking language files..."
for f in *
	do mv $f $(echo $f | awk 'match($0, /firefox-.*?\.(.*?)\.langpack.xpi/, a){print a[1] ".xpi"}')
done
cd ..
tar -cvf - firefox-langpacks | xz -zc - > firefox-langpacks-$VERSION_NUMBER.tar.xz
rm -rf firefox-langpacks

echo
echo "*** All finished!"
