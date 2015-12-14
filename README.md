firefox-dev
===========

This is a fork of http://pkgs.fedoraproject.org/cgit/firefox.git/
tracking Mozilla's Aurora release channel, otherwise known as [Firefox
Developer Edition](https://www.mozilla.org/firefox/developer/).

### Getting the goods

Fetch it from Copr while it's hot!

```
dnf copr enable bob131/firefox-dev
dnf install firefox-dev
```

Be warned: This package obsoletes the firefox package; both packages
can't be installed on the same system simultaneously.

### Building from spec

This assumes an empty or absent `~/rpmbuild` directory.

```
hub clone Bob131/firefox-dev && cd firefox-dev
export VER="`grep -P "^Version:" firefox-dev.spec | grep -Po "[0-9\.a]{6}"`"
curl -O "https://hg.mozilla.org/releases/mozilla-aurora/archive/$(basename `curl https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-aurora/firefox-$VER.en-US.linux-x86_64.txt | tail -n1`).tar.bz2" && ls *.tar.bz2 | xargs -I {} mv {} mozilla-aurora-{}
export URL="https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-aurora-l10n/linux-x86_64/xpi/" && mkdir firefox-langpacks; cd firefox-langpacks && curl $URL | egrep -o "\".*?firefox-$VER.*?\.xpi\"" | sed 's/"//g' | awk "{print \"https://archive.mozilla.org\" \$0}" | xargs wget && for f in *; do mv $f `echo $f | awk 'match($0, /firefox-.*?\.(.*?)\.langpack.xpi/, a){print a[1] ".xpi"}'`; done; cd .. && tar -cvf - firefox-langpacks | xz -zc - > firefox-langpacks-$VER.tar.xz && rm -rf firefox-langpacks
mkdir ~/rpmbuild
ln -s `pwd` ~/rpmbuild/SOURCES
rpmbuild -ba firefox-dev.spec
```

## Frequently Asked Questions

(also known as "questions that have never been asked but the author felt
needed answering anyway")

### Aurora refuses to use my preexisting Firefox profile! What do?

This should do the trick:

```
touch ~/.mozilla/firefox/ignore-dev-edition-profile
```

### Why the `-dev` suffix instead of the usual `-devel`?

I'm far from an expert on these matters, but personally I would expect
packages with the `-devel` suffix to contain actual library headers and
whatnot. This package includes no such thing.

### What license is this repo under?

As per the [Fedora wiki](https://fedoraproject.org/wiki/Licensing:Main#License_of_Fedora_SPEC_Files),
the original repo is under the MIT and as such so are my additional
contributions.
