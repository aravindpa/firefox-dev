#!/bin/bash

# Exit script if any commands return errors. Treat unset variables as an error.
set -eu

# Find the version number and commit hash of the latest Firefox Aurora release.
echo "*** Looking up the latest release..."
curl "https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-aurora/" -o index.html
export VERSION=$(grep -E 'firefox-[[:digit:]]+\.[[:alnum:]]+' -m 1 -o index.html | grep -E -m 1 -o '[[:digit:]]+\.[[:alnum:]]+')
export VERSION_DATE=$VERSION.$(date +%Y%m%d)
export LATEST_COMMIT=$(basename $(curl "https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-aurora/firefox-$VERSION.en-US.linux-x86_64.txt" | tail -n1))
export SHORT_COMMIT=$(echo "$LATEST_COMMIT" | grep -Eo '^[[:alnum:]]{7}')
rm index.html
export DOWNLOAD_SOURCE_URL="https://hg.mozilla.org/releases/mozilla-aurora/archive/$LATEST_COMMIT.tar.bz2"

# Update the spec file to use latest Firefox release.
sed -i -r "s/^(Version:[[:space:]]+)[[:digit:]]+\.[[:alnum:]]+\.[[:digit:]]+/\1$VERSION_DATE/" firefox-dev.spec
sed -i -r "s/^(%define revision[[:space:]]+)[[:alnum:]]+/\1$LATEST_COMMIT/" firefox-dev.spec
sed -i -r "s/^(%define revision_short[[:space:]]+)[[:alnum:]]+/\1$SHORT_COMMIT/" firefox-dev.spec

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
grep -Eo "\".*?firefox-$VERSION.*?\.xpi\"" index.html | sed -r 's/"(.*)"/https:\/\/archive.mozilla.org\1/g' | xargs wget
rm index.html
echo
echo "*** Repacking language files..."
for f in *
	do mv $f $(echo $f | awk 'match($0, /firefox-.*?\.(.*?)\.langpack.xpi/, a){print a[1] ".xpi"}')
done
cd ..
tar -cvf - firefox-langpacks | xz -zc - > firefox-langpacks-$VERSION.tar.xz
rm -rf firefox-langpacks

echo
echo "*** All finished!"
