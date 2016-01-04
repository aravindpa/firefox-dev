#!/bin/bash

# Get the source code for the latest Firefox Aurora release.
export VERSION=$(grep -P "^Version:" firefox-dev.spec | grep -Po "[0-9\.a]{6}")
export LATEST_COMMIT=$(basename $(curl "https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-aurora/firefox-$VERSION.en-US.linux-x86_64.txt" | tail -n1))
echo
echo "*** Downloading latest release of Firefox Aurora..."
curl -O "https://hg.mozilla.org/releases/mozilla-aurora/archive/$LATEST_COMMIT.tar.bz2"
mv $LATEST_COMMIT.tar.bz2 firefox-$VERSION.tar.bz2

# Get the langpacks too.
export LANGPACK_URL="https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-aurora-l10n/linux-x86_64/xpi/"
mkdir -p firefox-langpacks
cd firefox-langpacks
echo
echo "*** Downloading langpacks for Firefox..."
curl $LANGPACK_URL | egrep -o "\".*?firefox-$VERSION.*?\.xpi\"" | sed 's/"//g' | awk "{print \"https://archive.mozilla.org\" \$0}" | xargs wget
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
