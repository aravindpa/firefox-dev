firefox-dev
===========

This is a fork of the Fedora packaging repo for
[mainline Firefox](http://pkgs.fedoraproject.org/cgit/firefox.git/),
modified to track Mozilla's "Aurora" release channel, otherwise known as
[Firefox Developer Edition](https://www.mozilla.org/firefox/developer/).
If you think you've noticed a problem with this build, go ahead and let me know,
but also remember that this is the pre-beta release. It should still be quite
usable, but it won't be perfect. So be sure to check with Mozilla support and
report any bugs you find to them too. Have fun!

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
errors, though. Watch this repo for updates!


### Building from spec

[The Fedora Wiki](https://fedoraproject.org/wiki/How_to_create_an_RPM_package#Preparing_your_system)
has a detailed guide on the basic setup required, which you should follow, with
one possible exception: The Wiki suggests adding a new user account, and logging
into that account whenever you build your packages. I'd rather just do it from a
virtual machine with a clean installation of Fedora, as it's easier to keep
track of any dependencies or configurations you might need to add on top of the
base OS. But it's up to you. Adding whichever user account you choose to the
`mock` group, as they recommend, may still be helpful, though.

``` bash
sudo usermod -a -G mock YOUR_USERNAME
```

Once you have the RPM build tools installed, your user account set up, and the
`rpmbuild` directory created, you obviously will also need a copy of this
repository. I like to put it in `~/rpmbuild/SPECS/firefox-dev`

``` bash
cd ~/rpmbuild/SPECS
git clone https://gitlab.com/terrycloth/firefox-dev.git
cd firefox-dev
```

Then, to fetch the source code for the latest release of Firefox Developer
Edition, we have a convenient script. It also updates the version and release
numbers in the spec file. Mozilla releases updates just about every day, so
always run this script to make sure you have the very latest source code.

``` bash
./GET_SOURCE.bash
```

Firefox Developer Edition has dependencies which you also need to install before
building.

``` bash
sudo dnf install alsa-lib-devel autoconf213 bzip2-devel freetype-devel gcc-c++ GConf2-devel GConf2-devel gstreamer1-devel gstreamer1-plugins-base-devel gtk2-devel gtk3-devel hunspell-devel ImageMagick krb5-devel libcurl-devel libffi-devel libicu-devel libIDL-devel libjpeg-devel libnotify-devel libpng-devel libvpx-devel libXrender-devel libXt-devel mesa-libGL-devel nspr-devel nss-devel nss-static pango-devel pulseaudio-libs-devel sqlite-devel startup-notification-devel yasm zlib-devel
```

And finally you can build the actual package.

``` bash
rpmbuild --define "%_sourcedir $(pwd)" -ba firefox-dev.spec
```

You need that `--define` flag because rpmbuild normally searches for both the
source tarball and the patches in `~/rpmbuild/SOURCES/`, but we keep the patch
files all together in this repository, and it's easier to just download the
tarball here too.

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
