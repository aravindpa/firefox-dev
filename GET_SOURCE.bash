#!/bin/bash

# Exit script if any commands return errors. Treat unset variables as an error.
set -eu

# Find the version number and commit hash of the latest Firefox Aurora release.
echo "*** Looking up the latest release..."
curl "https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-aurora/" -o index.html
export VERSION_SHORT=$(grep -Eo 'firefox-[[:digit:]]+\.[[:alnum:]]+' -m 1 index.html | grep -Eo '[[:digit:]]+\.[[:alnum:]]+' -m 1)
curl "https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-aurora/firefox-$VERSION_SHORT.en-US.linux-x86_64.txt" -o firefox-latest-info.txt
export DATE=$(grep -Eo '[[:digit:]]{8}' -m 1 firefox-latest-info.txt)
export VERSION_DATE=$VERSION_SHORT.$DATE
export LATEST_COMMIT=$(basename $(tail -n1 firefox-latest-info.txt))
rm index.html firefox-latest-info.txt
export DOWNLOAD_SOURCE_URL="https://hg.mozilla.org/releases/mozilla-aurora/archive/$LATEST_COMMIT.tar.bz2"

echo
echo "Latest commit: $LATEST_COMMIT"
echo "Version:       $VERSION_DATE"

if [ -f "$LATEST_COMMIT.tar.bz2" ]
	then echo
	echo "** Looks like you already have the latest source files."
else
	# Update the spec file to use latest Firefox release.
	sed -i -r "s/^(%global version_short[[:space:]]+)[[:digit:]]+\.[[:alnum:]]+/\1$VERSION_SHORT/" firefox-dev.spec
	sed -i -r "s/^(Version:[[:space:]]+)[[:digit:]]+\.[[:alnum:]]+\.[[:digit:]]+/\1$VERSION_DATE/" firefox-dev.spec
	sed -i -r "s/^(%global latest_commit[[:space:]]+)[[:alnum:]]+/\1$LATEST_COMMIT/" firefox-dev.spec

	# Add an entry to the change log.
	echo
	echo "Updating the packagechangelog..."
	echo "What's your name?"
	read PACKAGER_NAME
	echo "What's your email address?"
	read PACKAGER_EMAIL
	sed -i -r "s/^(%changelog)$/\1\n* $(date '+%a %b %d %Y') $PACKAGER_NAME <$PACKAGER_EMAIL> - $VERSION_DATE-1\n- Updated to $VERSION_DATE.\n/" firefox-dev.spec

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
	grep -Eo "\".*?firefox-$VERSION_SHORT.*?\.xpi\"" index.html | sed -r 's/"(.*)"/https:\/\/archive.mozilla.org\1/g' | xargs wget
	rm index.html
	echo
	echo "*** Repacking language files..."
	for f in *
		do mv $f $(echo $f | awk 'match($0, /firefox-.*?\.(.*?)\.langpack.xpi/, a){print a[1] ".xpi"}')
	done
	cd ..
	tar -cvf - firefox-langpacks | xz -zc - > firefox-dev-langpacks-$VERSION_DATE.tar.xz
	rm -rf firefox-langpacks

	echo
	echo "*** All finished!"
fi
