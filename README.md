firefox-dev
===========

This is a fork of
[the Fedora packaging repo for mainline Firefox](http://pkgs.fedoraproject.org/cgit/firefox.git/),
tracking Mozilla's Aurora release channel, otherwise known as
[Firefox Developer Edition](https://www.mozilla.org/firefox/developer/).



## How to install

Those interested in helping test this build of Firefox Developer Edition can
see the instructions below about building from spec. Otherwise, just add the
Copr repository.

Be warned, though: This package obsoletes the firefox package. Both packages
can't be installed on the same system simultaneously.


### Copr makes it easy

``` bash
sudo dnf copr enable bob131/firefox-dev
sudo dnf install firefox-dev
```


### Building from spec

First, a little setup: Obviously, you need a copy of this repository.

``` bash
git clone https://github.com/Bob131/firefox-dev.git
cd firefox-dev
```

Then, to fetch the source code for the latest release of Firefox Developer
Edition, we have a convenient script. It also updates the version and release
numbers in the spec file. Mozilla releases updates just about every day, so
always run this script to make sure you have the very latest source code.

``` bash
./GET_SOURCE.bash
```

And finally you can build the actual package.

``` bash
rpmbuild --define "%_sourcedir $(pwd)" -ba firefox-dev.spec
```

Getting updates for our packaging repo is easy:

``` bash
git pull origin master
```

And then if there's a new release, you download the latest Firefox source
again.



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
