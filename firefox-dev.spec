# Separated plugins are supported on x86(64) only
%ifarch %{ix86} x86_64
	%define separated_plugins 1
%else
	%define separated_plugins 0
%endif

%ifarch %{ix86} x86_64
	%define run_tests         0
%else
	%define run_tests         0
%endif

# Build as a debug package?
%define debug_build       0

%define default_bookmarks_file %{_datadir}/bookmarks/default-bookmarks.html
%define firefox_app_id  \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}
# Minimal required versions
%global cairo_version 1.13.1
%global freetype_version 2.1.9
%global libnotify_version 0.7.0
%global libvpx_version 1.3.0

%global nspr_version 4.10.10
%global nspr_build_version %(pkg-config --silence-errors --modversion nspr 2>/dev/null || echo 65536)
%global nss_version 3.19.2
%global nss_build_version %(pkg-config --silence-errors --modversion nss 2>/dev/null || echo 65536)

%global sqlite_version 3.8.4.2
# The actual sqlite version (see #480989):
%global sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo 65536)

%global mozappdir     %{_libdir}/%{name}
%global mozappdirdev  %{_libdir}/%{name}-devel-%{version}
%global langpackdir   %{mozappdir}/langpacks

%define official_branding       1
%define build_langpacks         1

%define enable_mozilla_crashreporter       0
%if !%{debug_build}
	%ifarch %{ix86} x86_64
		%define enable_mozilla_crashreporter       1
	%endif
%endif

# Commit ref for the latest release of Firefox Developer Edition.
%define latest_commit  8210de2a2b4fdb1701d3dadf65184bda51d6fbe7
# Short version of the version number (without the date of the latest commit).
%define version_short  47.0a2

# Name of the directory contained inside the Firefox source tarball.
%global tarball_directory  %{_builddir}/%{name}-%{version}/mozilla-aurora-%{latest_commit}
# A shorter, less cumbersome directory name for the unpacked source code.
# tarball_directory moves here.
%global unpacked_source    %{_builddir}/%{name}-%{version}/source


Summary:        Developer Edition (Aurora release channel) of the Mozilla Firefox Web browser
Name:           firefox-dev
# You can see which is the latest version here:
# https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-aurora/
Version:        47.0a2.20160420
Release:        1%{?dist}
URL:            https://www.mozilla.org/firefox/developer/
License:        MPLv1.1 or GPLv2+ or LGPLv2+

Source0:        https://hg.mozilla.org/releases/mozilla-aurora/archive/%{latest_commit}.tar.bz2

%if %{build_langpacks}
Source1:        firefox-langpacks-%{version}.tar.xz
%endif

Source10:       firefox-mozconfig
Source12:       firefox-redhat-default-prefs.js
Source20:       firefox.desktop
Source21:       firefox.sh.in
Source23:       firefox.1
Source24:       mozilla-api-key
Source25:       firefox-symbolic.svg

# Build patches.
Patch0:         firefox-install-dir.patch
Patch3:         mozilla-build-arm.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=814879#c3
Patch18:        xulrunner-24.0-jemalloc-ppc.patch
# workaround linking issue on s390 (JSContext::updateMallocCounter(size_t) not found)
Patch19:        xulrunner-24.0-s390-inlines.patch
Patch20:        firefox-build-prbool.patch
Patch21:        firefox-ppc64le.patch
Patch24:        firefox-debug.patch
Patch25:        rhbz-1219542-s390-build.patch

# Fedora-specific patches.
# Unable to install addons from https pages
Patch204:       rhbz-966424.patch
Patch215:       firefox-enable-addons.patch
Patch219:       rhbz-1173156.patch
Patch221:       firefox-fedora-ua.patch
Patch222:       firefox-gtk3-20.patch
Patch223:       rhbz-1291190-appchooser-crash.patch
Patch224:       mozilla-1170092.patch

# Upstream patches.
Patch301:       mozilla-1205199.patch
Patch302:       mozilla-1228540.patch
Patch303:       mozilla-1228540-1.patch
Patch304:       mozilla-1253216.patch
Patch305:       mozilla-1245076.patch
Patch306:       mozilla-1245076-1.patch

# Debian patches.
Patch400:       Allow-unsigned-addons-in-usr-lib-share-mozilla-exten.patch
Patch401:       mozilla-440908.patch

# Fix Skia Neon stuff on AArch64
# Update https://bugzilla.mozilla.org/show_bug.cgi?id=1142056
# when removed
Patch500:       aarch64-fix-skia.patch

BuildRequires:  pkgconfig(nspr) >= %{nspr_version}
BuildRequires:  pkgconfig(nss) >= %{nss_version}
BuildRequires:  nss-static >= %{nss_version}

BuildRequires:  pkgconfig(libpng)
BuildRequires:  libjpeg-devel
BuildRequires:  zip
BuildRequires:  bzip2-devel
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libIDL-2.0)

BuildRequires:  pkgconfig(gtk+-3.0)

BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(krb5)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(freetype2) >= %{freetype_version}
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(hunspell)
BuildRequires:  pkgconfig(libstartup-notification-1.0)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(libnotify) >= %{libnotify_version}
BuildRequires:  pkgconfig(dri)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  libvpx-devel >= %{libvpx_version}
BuildRequires:  autoconf213
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(gconf-2.0)
BuildRequires:  yasm
BuildRequires:  ImageMagick
BuildRequires:  GConf2-devel

Requires:       mozilla-filesystem

Requires:       nspr >= %{nspr_build_version}
Requires:       nss >= %{nss_build_version}

BuildRequires:  desktop-file-utils
BuildRequires:  system-bookmarks

BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-allocators-1.0)

BuildRequires:  pkgconfig(sqlite3) >= %{sqlite_version}
Requires:       sqlite >= %{sqlite_build_version}

BuildRequires:  pkgconfig(libffi)

Requires:       system-bookmarks

%if %{?run_tests}
BuildRequires:  xorg-x11-server-Xvfb
%endif

Obsoletes:      firefox <= %{version}
Obsoletes:      mozilla <= 37:1.7.13
Provides:       webclient

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance, and portability.

%if %{enable_mozilla_crashreporter}
%global moz_debug_prefix %{_prefix}/lib/debug
%global moz_debug_dir %{moz_debug_prefix}%{mozappdir}
%global uname_m %(uname -m)
%global symbols_file_name firefox-%{version_short}.en-US.%{_os}-%{uname_m}.crashreporter-symbols.zip
%global symbols_file_path %{moz_debug_dir}/%{symbols_file_name}
%global _find_debuginfo_opts -p %{symbols_file_path} -o debugcrashreporter.list
%global crashreporter_pkg_name mozilla-crashreporter-%{name}-debuginfo
%package -n %{crashreporter_pkg_name}
Summary: Debugging symbols used by Mozilla's crash reporter servers
Group: Development/Debug
%description -n %{crashreporter_pkg_name}
This package provides debug information for Firefox, for use by
Mozilla's crash reporter servers.  If you are trying to locally
debug %{name}, you want to install %{name}-debuginfo instead.
%files -n %{crashreporter_pkg_name} -f debugcrashreporter.list
%defattr(-,root,root)
%endif

%if %{run_tests}
%global testsuite_pkg_name mozilla-%{name}-testresults
%package -n %{testsuite_pkg_name}
Summary: Results of testsuite
%description -n %{testsuite_pkg_name}
This package contains results of tests executed during build.
%files -n %{testsuite_pkg_name}
/test_results
%endif





# ========================= Preparation =========================

%prep
%setup -q -c

# Rename unpacked source tarball directory, to a shorter, less unwieldy name.
mv %{tarball_directory} %{unpacked_source}
cd %{unpacked_source}

# Build patches.
%patch0 -b "\~"
#%patch1 -b "\~"
%patch18 -b "\~"
%patch19 -b "\~"
%patch20 -b "\~"
%patch21 -b "\~"
%patch24 -b "\~"

%ifarch s390
%patch25 -b "\~"
%endif

%patch3 -b "\~"

# Fedora-specific patches.
%patch204 -b "\~"
#%patch215 -b "\~"
%patch219 -b "\~"
## THIS WASN'T COMMENTED WHEN I TRIED BUILDING YESTERDAY:
#%patch221 -b "\~"
#%patch222 -b "\~"
%patch223 -b "\~"
#%patch224 -b "\~"

# Upstream patches.
#%patch301 -b "\~"
#%patch302 -b "\~"
#%patch303 -b "\~"
%patch304 -b "\~"
%patch305 -b "\~"
%patch306 -b "\~"

# Debian extension patches.
#%patch400 -b "\~"
#%patch401 -b "\~"

# Fix Skia Neon stuff on AArch64
#%patch500 -b "\~"

rm -f .mozconfig
cp %{SOURCE10} .mozconfig

%if %{official_branding}
echo "ac_add_options --enable-official-branding" >> .mozconfig
echo "ac_add_options --with-branding=browser/branding/aurora" >> .mozconfig
%endif

cp %{SOURCE24} mozilla-api-key

echo "ac_add_options --enable-default-toolkit=cairo-gtk3" >> .mozconfig

echo "ac_add_options --with-system-nspr" >> .mozconfig
echo "ac_add_options --with-system-nss" >> .mozconfig

echo "ac_add_options --enable-system-sqlite" >> .mozconfig

echo "ac_add_options --disable-system-cairo" >> .mozconfig

echo "ac_add_options --enable-system-ffi" >> .mozconfig

echo "ac_add_options --enable-gstreamer=1.0" >> .mozconfig

%if !%{?separated_plugins}
echo "ac_add_options --disable-ipc" >> .mozconfig
%endif

%ifarch %{arm}
echo "ac_add_options --disable-elf-hack" >> .mozconfig
%endif

%if %{?debug_build}
echo "ac_add_options --enable-debug" >> .mozconfig
echo "ac_add_options --disable-optimize" >> .mozconfig
echo "ac_add_options --enable-dtrace" >> .mozconfig
%else
echo "ac_add_options --disable-debug" >> .mozconfig
echo "ac_add_options --enable-optimize" >> .mozconfig
%endif

# s390(x) fails to start with jemalloc enabled
%ifarch s390 s390x
echo "ac_add_options --disable-jemalloc" >> .mozconfig
%endif

%ifarch armv7hl
echo "ac_add_options --with-arch=armv7-a" >> .mozconfig
echo "ac_add_options --with-float-abi=hard" >> .mozconfig
echo "ac_add_options --with-fpu=vfpv3-d16" >> .mozconfig
echo "ac_add_options --disable-elf-hack" >> .mozconfig
%endif
%ifarch armv7hnl
echo "ac_add_options --with-arch=armv7-a" >> .mozconfig
echo "ac_add_options --with-float-abi=hard" >> .mozconfig
echo "ac_add_options --with-fpu=neon" >> .mozconfig
echo "ac_add_options --disable-elf-hack" >> .mozconfig
echo "ac_add_options --disable-ion" >> .mozconfig
echo "ac_add_options --disable-yarr-jit" >> .mozconfig
%endif
%ifarch armv5tel
echo "ac_add_options --with-arch=armv5te" >> .mozconfig
echo "ac_add_options --with-float-abi=soft" >> .mozconfig
echo "ac_add_options --disable-elf-hack" >> .mozconfig
echo "ac_add_options --disable-ion" >> .mozconfig
echo "ac_add_options --disable-yarr-jit" >> .mozconfig
%endif

%ifnarch %{ix86} x86_64
echo "ac_add_options --disable-webrtc" >> .mozconfig
%endif

%if !%{enable_mozilla_crashreporter}
echo "ac_add_options --disable-crashreporter" >> .mozconfig
%endif

%if %{?run_tests}
echo "ac_add_options --enable-tests" >> .mozconfig
%endif

echo "ac_add_options --with-system-jpeg" >> .mozconfig





# ========================= Compile! =========================

%build
# Do not proceed with build if the sqlite require would be broken:
# make sure the minimum requirement is non-empty, ...
sqlite_version=$(expr "%{sqlite_version}" : '\([0-9]*\.\)[0-9]*\.') || exit 1
# ... and that major number of the computed build-time version matches:
case "%{sqlite_build_version}" in
  "$sqlite_version"*) ;;
  *) exit 1 ;;
esac

cd %{unpacked_source}

# Update the various config.guess to upstream release for aarch64 support
find ./ -name config.guess -exec cp /usr/lib/rpm/config.guess {} ';'

# -fpermissive is needed to build with gcc 4.6+ which has become stricter
#
# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
#
# Disable C++ exceptions since Mozilla code is not exception-safe
#
MOZ_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS" | sed -e 's/-Wall//')
#rhbz#1037063
# -Werror=format-security causes build failures when -Wno-format is explicitly given
# for some sources
# Explicitly force the hardening flags for Firefox so it passes the checksec test;
# See also https://fedoraproject.org/wiki/Changes/Harden_All_Packages
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -Wformat-security -Wformat -Werror=format-security"
# Disable null pointer optimization in gcc6 (rhbz#1328045).
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fno-delete-null-pointer-checks"
# Use hardened build.
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fPIC -Wl,-z,relro -Wl,-z,now"

%if %{?debug_build}
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | sed -e 's/-O2//')
%endif

%ifarch s390
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | sed -e 's/-g/-g1/')
# If MOZ_DEBUG_FLAGS is empty, firefox's build will default it to "-g" which
# overrides the -g1 from line above and breaks building on s390
# (OOM when linking, rhbz#1238225)
export MOZ_DEBUG_FLAGS=" "
%endif

%ifarch s390 %{arm} ppc aarch64
MOZ_LINK_FLAGS="-Wl,--no-keep-memory -Wl,--reduce-memory-overheads"
%endif

export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS
export LDFLAGS=$MOZ_LINK_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

MOZ_SMP_FLAGS=-j1

# On x86 architectures, Mozilla can build up to 4 jobs at once in parallel,
# however builds tend to fail on other arches when building in parallel.
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le aarch64
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 2 ] && MOZ_SMP_FLAGS=-j2
[ "$RPM_BUILD_NCPUS" -ge 4 ] && MOZ_SMP_FLAGS=-j4
[ "$RPM_BUILD_NCPUS" -ge 8 ] && MOZ_SMP_FLAGS=-j8
%endif

make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS" MOZ_SERVICES_SYNC="1"

# create debuginfo for crash-stats.mozilla.com
%if %{enable_mozilla_crashreporter}
#cd %{moz_objdir}
make -C objdir buildsymbols
%endif

%if %{?run_tests}
ln -s /usr/bin/certutil objdir/dist/bin/certutil
ln -s /usr/bin/pk12util objdir/dist/bin/pk12util
mkdir test_results
./mach --log-no-times check-spidermonkey &> test_results/check-spidermonkey || true
./mach --log-no-times check-spidermonkey &> test_results/check-spidermonkey-2nd-run || true
./mach --log-no-times cppunittest &> test_results/cppunittest || true
xvfb-run -a ./mach --log-no-times crashtest &> test_results/crashtest || true
./mach --log-no-times gtest &> test_results/gtest || true
xvfb-run -a ./mach --log-no-times jetpack-test &> test_results/jetpack-test || true
# not working right now ./mach marionette-test &> test_results/marionette-test || true
xvfb-run -a ./mach --log-no-times mochitest-a11y &> test_results/mochitest-a11y || true
xvfb-run -a ./mach --log-no-times mochitest-browser &> test_results/mochitest-browser || true
xvfb-run -a ./mach --log-no-times mochitest-chrome &> test_results/mochitest-chrome || true
xvfb-run -a ./mach --log-no-times mochitest-devtools &> test_results/mochitest-devtools || true
xvfb-run -a ./mach --log-no-times mochitest-plain &> test_results/mochitest-plain || true
xvfb-run -a ./mach --log-no-times reftest &> test_results/reftest || true
xvfb-run -a ./mach --log-no-times webapprt-test-chrome &> test_results/webapprt-test-chrome || true
xvfb-run -a ./mach --log-no-times webapprt-test-content &> test_results/webapprt-test-content || true
./mach --log-no-times webidl-parser-test &> test_results/webidl-parser-test || true
xvfb-run -a ./mach --log-no-times xpcshell-test &> test_results/xpcshell-test || true
rm -f  objdir/dist/bin/certutil
rm -f  objdir/dist/bin/pk12util
%endif





# ========================= Install =========================

%install
cd %{unpacked_source}

# set up our default bookmarks
cp -p %{default_bookmarks_file} objdir/dist/bin/browser/defaults/profile/bookmarks.html

# Make sure locale works for langpacks
cat > objdir/dist/bin/browser/defaults/preferences/firefox-l10n.js << EOF
pref("general.useragent.locale", "chrome://global/locale/intl.properties");
EOF

%make_install -C objdir

mkdir -p $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_datadir}/applications}

desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE20}

# set up the firefox start script
rm -rf $RPM_BUILD_ROOT%{_bindir}/firefox
cat %{SOURCE21} > $RPM_BUILD_ROOT%{_bindir}/%{name}
chmod 755 $RPM_BUILD_ROOT%{_bindir}/%{name}

install -p -D -m 644 %{SOURCE23} $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1

rm -f $RPM_BUILD_ROOT/%{mozappdir}/firefox-config
rm -f $RPM_BUILD_ROOT/%{mozappdir}/update-settings.ini

for s in 16 32 48; do
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps
    cp -p browser/branding/aurora/default${s}.png \
               $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/firefox.png
done
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps
cp -p browser/branding/aurora/mozicon128.png \
           $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps/firefox.png
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps
convert browser/branding/aurora/content/about-logo@2x.png -adaptive-resize 256x256 \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps/firefox.png

# Install hight contrast icon
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/symbolic/apps
cp -p %{SOURCE25} \
           $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/symbolic/apps

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<!--
BugReportURL: https://bugzilla.mozilla.org/show_bug.cgi?id=1071061
SentUpstream: 2014-09-22
-->
<application>
  <id type="desktop">%{name}.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <description>
    <p>
      Bringing together all kinds of awesomeness to make browsing better for you.
      Get to your favorite sites quickly – even if you don’t remember the URLs.
      Type your term into the location bar (aka the Awesome Bar) and the autocomplete
      function will include possible matches from your browsing history, bookmarked
      sites and open tabs.
    </p>
    <!-- FIXME: Needs another couple of paragraphs -->
  </description>
  <url type="homepage">http://www.mozilla.org/en-US/</url>
  <screenshots>
    <screenshot type="default">https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/a.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/b.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/c.png</screenshot>
  </screenshots>
  <!-- FIXME: change this to an upstream email address for spec updates
  <updatecontact>someone_who_cares@upstream_project.org</updatecontact>
   -->
</application>
EOF

echo > ../%{name}.lang
%if %{build_langpacks}
# Extract langpacks, make any mods needed, repack the langpack, and install it.
mkdir -p $RPM_BUILD_ROOT%{langpackdir}
tar xf %{SOURCE1}
for langpack in `ls firefox-langpacks/*.xpi`; do
  language=`basename $langpack .xpi`
  extensionID=langpack-$language@firefox.mozilla.org
  mkdir -p $extensionID
  unzip -qq $langpack -d $extensionID
  find $extensionID -type f | xargs chmod 644

  cd $extensionID
  zip -qq -r9mX ../${extensionID}.xpi *
  cd -

  install -m 644 ${extensionID}.xpi $RPM_BUILD_ROOT%{langpackdir}
  language=`echo $language | sed -e 's/-/_/g'`
  echo "%%lang($language) %{langpackdir}/${extensionID}.xpi" >> ../%{name}.lang
done
rm -rf firefox-langpacks

# Install langpack workaround (see #707100, #821169)
function create_default_langpack() {
language_long=$1
language_short=$2
cd $RPM_BUILD_ROOT%{langpackdir}
ln -s langpack-$language_long@firefox.mozilla.org.xpi langpack-$language_short@firefox.mozilla.org.xpi
cd -
echo "%%lang($language_short) %{langpackdir}/langpack-$language_short@firefox.mozilla.org.xpi" >> ../%{name}.lang
}

# Table of fallbacks for each language
# please file a bug at bugzilla.redhat.com if the assignment is incorrect
create_default_langpack "bn-IN" "bn"
create_default_langpack "es-AR" "es"
create_default_langpack "fy-NL" "fy"
create_default_langpack "ga-IE" "ga"
create_default_langpack "gu-IN" "gu"
create_default_langpack "hi-IN" "hi"
create_default_langpack "hy-AM" "hy"
create_default_langpack "nb-NO" "nb"
create_default_langpack "nn-NO" "nn"
create_default_langpack "pa-IN" "pa"
create_default_langpack "pt-PT" "pt"
create_default_langpack "sv-SE" "sv"
create_default_langpack "zh-TW" "zh"
%endif # build_langpacks


mkdir -p $RPM_BUILD_ROOT/%{mozappdir}/browser/defaults/preferences

# System config dir
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/pref

# System extensions
mkdir -p $RPM_BUILD_ROOT%{_datadir}/mozilla/extensions/%{firefox_app_id}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/mozilla/extensions/%{firefox_app_id}

# Copy over the LICENSE
install -p -c -m 644 LICENSE $RPM_BUILD_ROOT/%{mozappdir}

# Use the system hunspell dictionaries
rm -rf ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries

# Enable crash reporter for Firefox application
%if %{enable_mozilla_crashreporter}
# The file being edited here seems to be in the wrong place, *and* already has
# the "[Crash Reporter]" enabled. This spec expects files to wind up in
# ~/rpmbuild/BUILDROOT/firefox-dev-47.0a2.20160422-1.fc24.x86_64/usr/lib64/firefox-dev/
# but for some reason a lot of them are winding up in ...firefox/ instead.
#sed -i -e "s/\[Crash Reporter\]/[Crash Reporter]\nEnabled=1/" $RPM_BUILD_ROOT/%{mozappdir}/application.ini
# Add debuginfo for crash-stats.mozilla.com
mkdir -p $RPM_BUILD_ROOT/%{moz_debug_dir}
cp objdir/dist/%{symbols_file_name} $RPM_BUILD_ROOT/%{moz_debug_dir}
%endif

%if %{run_tests}
# Add debuginfo for crash-stats.mozilla.com
mkdir -p $RPM_BUILD_ROOT/test_results
cp test_results/* $RPM_BUILD_ROOT/test_results
%endif

# Default
cp %{SOURCE12} ${RPM_BUILD_ROOT}%{mozappdir}/browser/defaults/preferences


# === Move libraries to where they belong, under firefox-dev, not plain firefox! ===
# firefox-dev creates a symlink from `dictionaries` to system hunspell library,
# so we don't need this copy.
rm -r %{buildroot}/%{_libdir}/firefox/dictionaries
# `browser` directories conflict, so let's make a backup.
mv %{buildroot}/%{_libdir}/%{name}/browser \
	%{buildroot}/%{_libdir}/%{name}/browser.dev~
# Move everything from firefox to firefox-dev.
mv -f %{buildroot}/%{_libdir}/firefox/* \
	%{buildroot}/%{_libdir}/%{name}
# Merge backup of `browser` back in.
mv -f %{buildroot}/%{_libdir}/%{name}/browser.dev~/* \
	%{buildroot}/%{_libdir}/%{name}/browser/
# Rename directories for the devel package.
mv %{buildroot}/%{_libdir}/firefox-devel-%{version_short} \
	%{buildroot}/%{mozappdirdev}
# Clean up directories we don't need anymore.
rmdir %{buildroot}/%{_libdir}/firefox
rmdir %{buildroot}/%{_libdir}/%{name}/browser.dev~





# ========================= Pre/post-transaction Scriptlets =========================

# Moves defaults/preferences to browser/defaults/preferences
%pretrans -p <lua>
require 'posix'
require 'os'
if (posix.stat("%{mozappdir}/browser/defaults/preferences", "type") == "link") then
  posix.unlink("%{mozappdir}/browser/defaults/preferences")
  posix.mkdir("%{mozappdir}/browser/defaults/preferences")
  if (posix.stat("%{mozappdir}/defaults/preferences", "type") == "directory") then
    for i,filename in pairs(posix.dir("%{mozappdir}/defaults/preferences")) do
      os.rename("%{mozappdir}/defaults/preferences/"..filename, "%{mozappdir}/browser/defaults/preferences/"..filename)
    end
    f = io.open("%{mozappdir}/defaults/preferences/README","w")
    if f then
      f:write("Content of this directory has been moved to %{mozappdir}/browser/defaults/preferences.")
      f:close()
    end
  end
end


%pre


%preun
# is it a final removal?
if [ $1 -eq 0 ]; then
  rm -rf %{mozappdir}/components
  rm -rf %{mozappdir}/extensions
  rm -rf %{mozappdir}/plugins
  rm -rf %{langpackdir}
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi





# ========================= Files owned by this package =========================

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{mozappdir}/firefox
%{mozappdir}/firefox-bin
%doc %{_mandir}/man1/*
%dir %{_sysconfdir}/%{name}/*
%dir %{_datadir}/mozilla/extensions/*
%dir %{_libdir}/mozilla/extensions/*
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/applications/*.desktop
%dir %{mozappdir}
%doc %{mozappdir}/LICENSE
%{mozappdir}/browser/chrome
%{mozappdir}/browser/chrome.manifest
%{mozappdir}/browser/components
%{mozappdir}/browser/defaults/preferences/firefox-redhat-default-prefs.js
%{mozappdir}/browser/features
%attr(644, root, root) %{mozappdir}/browser/blocklist.xml
%dir %{mozappdir}/browser/extensions
%{mozappdir}/browser/extensions/*

%if %{build_langpacks}
%dir %{langpackdir}
%endif

%{mozappdir}/browser/omni.ja
%{mozappdir}/browser/icons
%{mozappdir}/run-mozilla.sh
%{mozappdir}/application.ini
%exclude %{mozappdir}/removed-files
%{_datadir}/icons/hicolor/16x16/apps/firefox.png
%{_datadir}/icons/hicolor/32x32/apps/firefox.png
%{_datadir}/icons/hicolor/48x48/apps/firefox.png
%{_datadir}/icons/hicolor/128x128/apps/firefox.png
%{_datadir}/icons/hicolor/256x256/apps/firefox.png
%{_datadir}/icons/hicolor/symbolic/apps/firefox-symbolic.svg
%{mozappdir}/webapprt-stub
%dir %{mozappdir}/webapprt
%{mozappdir}/webapprt/omni.ja
%{mozappdir}/webapprt/webapprt.ini

%if %{enable_mozilla_crashreporter}
%{mozappdir}/crashreporter
%{mozappdir}/crashreporter.ini
%{mozappdir}/Throbber-small.gif
%{mozappdir}/browser/crashreporter-override.ini
%endif

%{mozappdir}/*.so
%{mozappdir}/gtk2/*.so
%{mozappdir}/defaults/pref/channel-prefs.js
%{mozappdir}/dependentlibs.list
%{mozappdir}/dictionaries
%{mozappdir}/omni.ja
%{mozappdir}/platform.ini
%{mozappdir}/plugin-container
%{mozappdir}/gmp-clearkey
%exclude %{_includedir}
%exclude %{mozappdirdev}
%exclude %{_datadir}/idl





# ========================= Change log =========================

%changelog
* Wed Apr 27 2016 Andrew Toskin <andrew@tosk.in> - 47.0a2.20160426-1
- First working build of Firefox Aurora / Developer Edition.
