#!/bin/bash

# Exit script if any commands return errors. Treat unset variables as an error.
set -eu

# Find the version number and commit hash of the latest Firefox Aurora release.
echo "*** Looking up the latest release..."
curl "https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-aurora/" -o index.html
export version_short=$(grep -Eo 'firefox-[[:digit:]]+\.[[:alnum:]]+' index.html | tail -n1 | grep -Eo '[[:digit:]]+\.[[:alnum:]]+' -m 1)
curl "https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-aurora/firefox-${version_short}.en-US.linux-x86_64.txt" -o firefox-latest-info.txt
export date=$(grep -Eo '[[:digit:]]{8}' -m 1 firefox-latest-info.txt)
export version_date=${version_short}.${date}
export latest_commit=$(basename $(tail -n1 firefox-latest-info.txt))
rm index.html firefox-latest-info.txt
export download_source_url="https://hg.mozilla.org/releases/mozilla-aurora/archive/${latest_commit}.tar.bz2"

echo
echo "Latest commit: ${latest_commit}"
echo "Version:       ${version_date}"

if [ -f "${latest_commit}.tar.bz2" ]; then
	echo
	echo "** Looks like you already have the latest source files."
else
	# Update the spec file to use latest Firefox release.
	sed -i -r "s/^(%global version_short[[:space:]]+)[[:digit:]]+\.[[:alnum:]]+/\1${version_short}/" firefox-dev.spec
	sed -i -r "s/^(Version:[[:space:]]+)[[:digit:]]+\.[[:alnum:]]+\.[[:digit:]]+/\1${version_date}/" firefox-dev.spec
	sed -i -r "s/^(%global latest_commit[[:space:]]+)[[:alnum:]]+/\1${latest_commit}/" firefox-dev.spec

	# Add an entry to the change log.
	echo
	echo "** Updating the package changelog..."
	echo "What's your name?"
	read packager_name
	echo "What's your email address?"
	read packager_email
	sed -i -r "s/^(%changelog)$/\1\n* $(date '+%a %b %d %Y') ${packager_name} <${packager_email}> - ${version_date}-1\n- Updated to ${version_date}.\n/" firefox-dev.spec

	# Get the source code for the latest Firefox release.
	echo
	echo "*** Downloading latest release of Firefox Aurora..."
	curl -O "${download_source_url}"

	# Get the langpacks too.
	mkdir -p firefox-langpacks
	cd firefox-langpacks
	curl "https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-aurora-l10n/linux-x86_64/xpi/" -o index.html
	echo
	echo "*** Downloading langpacks for Firefox..."
	grep -Eo "\".*?firefox-${version_short}.*?\.xpi\"" index.html | sed -r 's/"(.*)"/https:\/\/archive.mozilla.org\1/g' | xargs wget
	rm index.html
	echo
	echo "*** Repacking language files..."
	for file in ./*
		do mv ${file} $(echo ${file} | awk 'match($0, /firefox-.*?\.(.*?)\.langpack.xpi/, a){print a[1] ".xpi"}')
	done
	cd ..
	tar -cvf - firefox-langpacks | xz -zc - > firefox-dev-langpacks-${version_date}.tar.xz
	rm -rf firefox-langpacks

	echo
	echo "*** All finished!"
fi
