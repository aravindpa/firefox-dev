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

[Like the original repo](https://fedoraproject.org/wiki/Licensing:Main#License_of_Fedora_SPEC_Files),
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
into that account whenever you build your packages. However, the
[`mock`](https://fedoraproject.org/wiki/Mock) command uses a chroot to build the
packages, which sandboxes your RPM builds, so creating a new user account
shouldn't be necessary anymore. If you use Mock, add your user account to the
`mock` group and you're good to go.

``` bash
sudo usermod -a -G mock YOUR_USERNAME
```

You obviously will also need a copy of this repository.

``` bash
git clone https://gitlab.com/terrycloth/firefox-dev.git
cd firefox-dev
```

Then, to fetch the source code for the latest release of Firefox Developer
Edition, we have a convenient script. It looks up information about the latest
release, checks to see if you already have the latest source, and downloads the
tarball if you don't. It also updates the version and release numbers in the
spec file, and adds an entry to the spec file's changelog section. You will be
prompted for your name and email, to add to the changelog, so enter those before
you walk away and let the script download things. Mozilla releases updates
(almost) daily, so always run this script to make sure you have the very latest
source code.

``` bash
./get-source.bash
```

Firefox Developer Edition has dependencies which you also need to install before
building.

``` bash
sudo dnf install alsa-lib-devel autoconf213 bzip2-devel freetype-devel gcc-c++ GConf2-devel GConf2-devel gstreamer1-devel gstreamer1-plugins-base-devel gtk2-devel gtk3-devel hunspell-devel ImageMagick krb5-devel libcurl-devel libffi-devel libicu-devel libIDL-devel libjpeg-devel libnotify-devel libpng-devel libvpx-devel libXrender-devel libXt-devel mesa-libGL-devel nspr-devel nss-devel nss-static pango-devel pulseaudio-libs-devel sqlite-devel startup-notification-devel yasm zlib-devel
```

And finally you can build the actual package. Note that Mock places the
generated files in a directory that looks something like
`/var/lib/mock/fedora-VERSION-ARCH/result/` -- with VERSION and ARCH depending
on the version and architecture of the instance of Fedora running on your
system.

``` bash
# Build a source RPM from the spec file and local tarballs.
mock --buildsrpm --spec $(pwd)/firefox-dev.spec --sources $(pwd)
# Optionally, build the binary RPM from the generated source RPM.
mock --rebuild /PATH/TO/SRC.RPM
```

Building the source RPM should only take a minute or two; it may take somewhat
longer the first time, as Mock sets up the chroot with the needed build tools.
Building the binary RPM may take a few hours, depending on your system hardware.



## About this repo, and how to contribute

I'll be adding to this section as I figure out *how this repo I've inherited
works* :/
