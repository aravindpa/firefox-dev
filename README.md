firefox-dev
===========

This is a fork of the Fedora packaging repo for
[mainline Firefox](http://pkgs.fedoraproject.org/cgit/firefox.git/),
modified to track Mozilla's "Aurora" release channel, otherwise known as
[Firefox Developer Edition](https://www.mozilla.org/firefox/developer/).
If you think you've noticed a problem with this build, go ahead and let me know,
but also remember that this is the pre-beta release. It should still be quite
usable, but it won't be perfect. So be sure to check with Mozilla support and
report any bugs you find with them too. Have fun!

[Like the original repo](https://fedoraproject.org/wiki/Licensing:Main#License_of_Fedora_SPEC_Files)
code specific to this RPM spec repository is published under the MIT license.



## How to install

Those interested in helping test this build of Firefox Developer Edition can
see the instructions below about building from spec. Otherwise, just add the
Copr repository.

Be warned, though: This package obsoletes the firefox package. Both packages
can't be installed on the same system simultaneously.


### Copr makes it easy

...Or, it will, when there is a copr. This package does not yet build without
errors, though. Keep an out for updates!


### Building from spec

First, a little setup: Obviously, you need a copy of this repository.

``` bash
git clone https://github.com/terrycloth/firefox-dev.git
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



## About this repo, and how to contribute

I'll be adding to this section as I figure out *how this repo I've inherited
works* :/

The spec file has a variable called `%tarballdir`, which describes where
rpmbuild will unpack the Firefox source code files. It should look like this:
`~/rpmbuild/BUILD/firefox-dev/mozilla-aurora-XXXXXX...` (with all the `X`s
replaced with the mercurial commit for the latest update). The spec file changes
into this directory before applying patches. So for every patch file, the paths
in the header should be relative to this directory.
