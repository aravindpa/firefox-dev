# Option: Freetype Patch (FC3+)
%define freetype_fc3 1

%define desktop_file_utils_version 0.9

%define indexhtml file:///usr/share/doc/HTML/index.html

ExclusiveArch: i386 x86_64 ia64 ppc s390 s390x

Summary:        Mozilla Firefox Web browser.
Name:           firefox
Version:        1.0.1
Release:        6
Epoch:          0
URL:            http://www.mozilla.org/projects/firefox/
License:        MPL/LGPL
Group:          Applications/Internet
Source0:        firefox-%{version}-source.tar.bz2
Source1:        firefox-gnomestripe-0.1.tar.gz
Source2:        firefox-1.0-langpacks-3.tar.bz2

Source10:       mozconfig-firefox
Source11:       firefox-redhat-default-bookmarks.html
Source12:       firefox-redhat-default-prefs.js
Source20:       firefox.desktop
Source21:       firefox.sh.in
Source22:       firefox.png
Source23:       firefox.xpm
Source24:       firefox.1
Source50:       firefox-xremote-client.sh.in
Source55:       firefox-rebuild-databases.pl.in
Source100:      find-external-requires

# build patches
Patch1:         firefox-0.7.3-freetype-compile.patch
Patch2:         firefox-1.0-prdtoa.patch
Patch3:         firefox-1.0-gcc4-compile.patch
Patch4:         firefox-1.0-recv-fortify.patch

# customization patches
Patch20:        firefox-redhat-homepage.patch
Patch21:        firefox-0.7.3-default-plugin-less-annoying.patch
Patch22:        firefox-0.7.3-psfonts.patch
Patch24:        firefox-PR1-default-applications.patch
Patch25:        firefox-PR1-software-update.patch
Patch26:        firefox-RC1-stock-icons-be.patch
Patch27:        firefox-RC1-stock-icons-fe.patch
Patch28:        firefox-RC1-stock-icons-gnomestripe.patch
Patch29:        firefox-gnomestripe-0.1-livemarks.patch
Patch30:        mozilla-1.7.3-pango-render.patch
Patch31:        firefox-1.0-pango-selection.patch
Patch32:        firefox-1.0-pango-space-width.patch
Patch33:        firefox-1.0-pango-rounding.patch

# local bugfixes
Patch40:        firefox-PR1-gnome-vfs-default-app.patch
Patch41:        firefox-PR1-stack-direction.patch
Patch42:        firefox-1.0-download-to-desktop.patch

# backported patches
Patch90:        firefox-PR1-gtk-file-chooser-morefixes.patch

# official upstream patches
Patch101:       firefox-PR1-pkgconfig.patch
Patch102:       mozilla-1.7.3-xptcall-s390.patch
Patch103:       firefox-1.0-xptcall-s390.patch
Patch104:       firefox-1.0-nspr-s390.patch
Patch105:       firefox-1.0-useragent.patch
Patch106:       firefox-1.0-gtk-system-colors.patch
Patch107:       firefox-1.0-remote-intern-atoms.patch
Patch108:       firefox-1.0-g-application-name.patch
Patch109:       firefox-1.0-execshield-nspr.patch
Patch110:       firefox-1.0-execshield-xpcom.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libpng-devel, libjpeg-devel
BuildRequires:  zlib-devel, zip
BuildRequires:  libIDL-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gtk2-devel
BuildRequires:  gnome-vfs2-devel
BuildRequires:  libgnome-devel
BuildRequires:  libgnomeui-devel
BuildRequires:  krb5-devel
BuildRequires:  pango-devel
BuildRequires:  autoconf213
%if %{freetype_fc3}
BuildRequires:  freetype-devel >= 2.1.9
%else
BuildRequires:  freetype-devel
%endif

Requires:       desktop-file-utils >= %{desktop_file_utils_version}
Obsoletes:      phoenix, mozilla-firebird, MozillaFirebird
Provides:       mozilla-firebird = %{epoch}:%{version}, MozillaFirebird = %{epoch}:%{version}
Provides:       webclient
%define ffdir %{_libdir}/firefox-%{version}

AutoProv: 0
%define _use_internal_dependency_generator 0
%define __find_requires %{SOURCE100}

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

#---------------------------------------------------------------------

%prep
%setup -q -n mozilla
%{__tar} -xzf %{SOURCE1}
%if %{freetype_fc3}
%patch1 -p0
%endif
%patch2  -p0
%patch3  -p0
%patch4  -p0
%patch20 -p0
%patch21 -p1
%patch22 -p1
%patch24 -p0
%patch25 -p0
%patch26 -p0
%patch27 -p0
%patch28 -p0
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch40 -p1
%patch41 -p0
%patch42 -p0
%patch90 -p0
%patch101 -p0
%patch102 -p0
%patch103 -p1
%patch104 -p0
%patch105 -p0
%patch106 -p0
%patch107 -p0
%patch108 -p0
%patch109 -p0
%patch110 -p0

%{__rm} -f .mozconfig
%{__cp} %{SOURCE10} .mozconfig

# set up our default bookmarks
%{__cp} %{SOURCE11} $RPM_BUILD_DIR/mozilla/profile/defaults/bookmarks.html


#---------------------------------------------------------------------

%build
autoconf-2.13

export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed s/-O2/-Os/`
export MOZILLA_OFFICIAL=1
export BUILD_OFFICIAL=1
MAKE="gmake %{?_smp_mflags}" make -f client.mk build

#---------------------------------------------------------------------

%install
%{__rm} -rf $RPM_BUILD_ROOT

cd xpinstall/packager/
%{__make} MOZILLA_BIN="\$(DIST)/bin/firefox-bin" STRIP=/bin/true
cd -

%{__mkdir_p} $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_datadir}/applications}

%{__tar} -C $RPM_BUILD_ROOT%{_libdir}/ -xzf dist/firefox-*-linux-gnu.tar.gz
%{__mv} $RPM_BUILD_ROOT%{_libdir}/firefox $RPM_BUILD_ROOT%{ffdir}

%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/firefox-*-linux-gnu.tar

%{__install} -p -D %{SOURCE22} $RPM_BUILD_ROOT%{_datadir}/pixmaps/firefox.png

desktop-file-install --vendor mozilla \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category X-Fedora \
  --add-category Application \
  --add-category Network \
  %{SOURCE20} 

# set up the firefox start script
%{__cat} %{SOURCE21} | %{__sed} -e 's,FFDIR,%{ffdir},g' -e 's,LIBDIR,%{_libdir},g' > \
  $RPM_BUILD_ROOT%{_bindir}/firefox
%{__chmod} 755 $RPM_BUILD_ROOT%{_bindir}/firefox

# set up our default preferences
%{__cat} %{SOURCE12} | %{__sed} -e 's,FIREFOX_RPM_VR,%{version}-%{release},g' > rh-default-prefs
%{__cp} rh-default-prefs $RPM_BUILD_ROOT/%{ffdir}/greprefs/all-redhat.js
%{__cp} rh-default-prefs $RPM_BUILD_ROOT/%{ffdir}/defaults/pref/all-redhat.js
%{__rm} rh-default-prefs

# set up our default bookmarks
%{__install} -p -D %{SOURCE11} $RPM_BUILD_ROOT%{ffdir}/defaults/profile/US/bookmarks.html
%{__install} -p -D %{SOURCE11} $RPM_BUILD_ROOT%{ffdir}/defaults/profile/bookmarks.html

%{__cat} %{SOURCE50} | %{__sed} -e 's,FFDIR,%{ffdir},g' -e 's,LIBDIR,%{_libdir},g' > \
  $RPM_BUILD_ROOT%{ffdir}/firefox-xremote-client

%{__chmod} 755 $RPM_BUILD_ROOT%{ffdir}/firefox-xremote-client
%{__install} -p -D %{SOURCE24} $RPM_BUILD_ROOT%{_mandir}/man1/firefox.1
%{__cat} %{SOURCE55} | %{__sed} -e 's,FFDIR,%{ffdir},g' > \
  $RPM_BUILD_ROOT/%{ffdir}/firefox-rebuild-databases.pl
%{__chmod} 755 $RPM_BUILD_ROOT/%{ffdir}/firefox-rebuild-databases.pl

%{__rm} -f $RPM_BUILD_ROOT%{ffdir}/firefox-config

cd $RPM_BUILD_ROOT%{ffdir}/chrome
find . -name "*" -type d -maxdepth 1 -exec %{__rm} -rf {} \;
cd -

# Install language packs
#cd $RPM_BUILD_ROOT%{ffdir}/chrome
#  mkdir lang
#  cd $RPM_BUILD_ROOT%{ffdir}/chrome/lang
#    mv ../installed-chrome.txt ./installed-chrome.txt
#    tar xvjf %{SOURCE2}
#
#    # Extract jar, modify the homepage, repack
#    for i in `ls *.jar`; do
#      rm -rf locale
#      LANGPACK=`basename $i .jar`
#      unzip $LANGPACK.jar
#      perl -pi -e "s|browser.startup.homepage.*$|browser.startup.homepage=%{indexhtml}|g;" locale/browser-region/region.properties
#      rm -rf $LANGPACK.jar
#      zip -r -D $LANGPACK.jar locale
#      rm -rf locale
#    done
#
#    mv -v *.jar ..
#  cd -
#cd -

#cat > $RPM_BUILD_ROOT%{ffdir}/defaults/pref/firefox-l10n.js << EOF
#pref("general.useragent.locale", "chrome://global/locale/intl.properties");
#EOF
#chmod 644 $RPM_BUILD_ROOT%{ffdir}/defaults/pref/firefox-l10n.js


# another bug fixed by looking at the debian package
%{__mkdir_p} $RPM_BUILD_ROOT%{ffdir}/chrome/icons/default/
%{__cp} %{SOURCE23} $RPM_BUILD_ROOT%{ffdir}/chrome/icons/default/default.xpm
%{__cp} %{SOURCE23} $RPM_BUILD_ROOT%{ffdir}/icons/default.xpm

# own mozilla plugin dir (#135050)
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins

# ghost files
touch $RPM_BUILD_ROOT%{ffdir}/chrome/chrome.rdf
for overlay in {"browser","communicator","inspector","messenger","navigator"}; do
  %{__mkdir_p} $RPM_BUILD_ROOT%{ffdir}/chrome/overlayinfo/$overlay/content
  touch $RPM_BUILD_ROOT%{ffdir}/chrome/overlayinfo/$overlay/content/overlays.rdf
done
touch $RPM_BUILD_ROOT%{ffdir}/components.ini
touch $RPM_BUILD_ROOT%{ffdir}/components/compreg.dat
touch $RPM_BUILD_ROOT%{ffdir}/components/xpti.dat
%{__mkdir_p}  $RPM_BUILD_ROOT%{ffdir}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}
touch $RPM_BUILD_ROOT%{ffdir}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}/install.rdf
touch $RPM_BUILD_ROOT%{ffdir}/extensions/installed-extensions-processed.txt
touch $RPM_BUILD_ROOT%{ffdir}/extensions/Extensions.rdf



#---------------------------------------------------------------------

%clean
%{__rm} -rf $RPM_BUILD_ROOT

#---------------------------------------------------------------------

%post
update-desktop-database %{_datadir}/applications

umask 022
%{ffdir}/firefox-rebuild-databases.pl || :

# create extensions directory
%{ffdir}/firefox -register

%postun
update-desktop-database %{_datadir}/applications
umask 022
# was this an upgrade?
if [ $1 -gt 1 ]; then
  %{ffdir}/firefox-rebuild-databases.pl
fi

%preun
# is it a final removal?
if [ $1 -eq 0 ]; then
  %{__rm} -rf %{ffdir}/chrome/overlayinfo
  %{__rm} -rf %{ffdir}/components
  %{__rm} -f  %{ffdir}/chrome/*.rdf
  %{__rm} -rf %{ffdir}/extensions
  %{__rm} -f %{ffdir}/components.ini
fi

%files
%defattr(-,root,root,-)
%{_bindir}/firefox
%{_mandir}/man1/*
%{_datadir}/applications/mozilla-%{name}.desktop
%{_datadir}/pixmaps/firefox.png
%{ffdir}
%{_libdir}/mozilla

%ghost %{ffdir}/chrome/chrome.rdf
%ghost %{ffdir}/chrome/overlayinfo/browser/content/overlays.rdf
%ghost %{ffdir}/chrome/overlayinfo/communicator/content/overlays.rdf
%ghost %{ffdir}/chrome/overlayinfo/inspector/content/overlays.rdf
%ghost %{ffdir}/chrome/overlayinfo/messenger/content/overlays.rdf
%ghost %{ffdir}/chrome/overlayinfo/navigator/content/overlays.rdf
%ghost %{ffdir}/components.ini
%ghost %{ffdir}/components/compreg.dat
%ghost %{ffdir}/components/xpti.dat
%ghost %{ffdir}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}/install.rdf
%ghost %{ffdir}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}/install.rdf
%ghost %{ffdir}/extensions/installed-extensions-processed.txt
%ghost %{ffdir}/extensions/Extensions.rdf


#---------------------------------------------------------------------

%changelog
* Tue Mar 22 2005 Christopher Aillon <caillon@redhat.com> 0:1.0.1-6
- Add patch to fix italic rendering errors with certain fonts (e.g. Tahoma)
- Re-enable jsd since there is now a venkman version that works with Firefox.

* Tue Mar  8 2005 Christopher Aillon <caillon@redhat.com> 0:1.0.1-5
- Add patch to compile against new fortified glibc macros

* Fri Mar  4 2005 Christopher Aillon <caillon@redhat.com> 0:1.0.1-4
- Build against gcc4, add build patches to do so.

* Thu Mar  3 2005 Christopher Aillon <caillon@redhat.com> 0:1.0.1-3
- Remerge firefox-1.0-pango-selection.patch
- Add execshield patches for ia64 and ppc
- BuildRequires libgnome-devel, libgnomeui-devel

* Sun Feb 27 2005 Christopher Aillon <caillon@redhat.com> 0:1.0.1-2
- Add upstream fix to reduce round trips to xserver during remote control
- Add upstream fix to call g_set_application_name

* Thu Feb 24 2005 Christopher Aillon <caillon@redhat.com> 0:1.0.1-1
- Update to 1.0.1 fixing several security flaws.
- Temporarily disable langpacks to workaround startup issues (#145806)
- Request the correct system colors from gtk (#143423)

* Tue Dec 28 2004 Christopher Aillon <caillon@redhat.com> 0:1.0-8
- Add upstream langpacks

* Sat Dec 25 2004 Christopher Aillon <caillon@redhat.com> 0:1.0-7
- Make sure we get a URL passed in to firefox (#138861)
- Mark some generated files as ghost (#136015)

* Wed Dec 15 2004 Christopher Aillon <caillon@redhat.com> 0:1.0-6
- Don't have downloads "disappear" when downloading to desktop (#139015)
- Add RPM version to the useragent
- BuildRequires pango-devel

* Sat Dec 11 2004 Christopher Aillon <caillon@redhat.com> 0:1.0-5
- Fix spacing in textareas when using pango for rendering
- Enable pango rendering by default.
- Enable smooth scrolling by default

* Fri Dec  3 2004 Christopher Aillon <caillon@redhat.com> 0:1.0-4
- Add StartupWMClass patch from Damian Christey (#135830)
- Use system colors by default (#137810)
- Re-add s390(x)

* Sat Nov 20 2004 Christopher Blizzard <blizzard@redhat.com> 0:1.0-3
- Add patch that uses pango for selection.

* Fri Nov 12 2004 Christopher Aillon <caillon@redhat.com> 0:1.0-2
- Fix livemarks icon issue. (#138989)

* Tue Nov  8 2004 Christopher Aillon <caillon@redhat.com> 0:1.0-1
- Firefox 1.0

* Thu Nov  4 2004 Christopher Aillon <caillon@redhat.com> 0:0.99-1.0RC1.3
- Add support for GNOME stock icons. (bmo #233461)

* Sat Oct 30 2004 Warren Togami <wtogami@redhat.com> 0:0.99-1.0RC1.2
- #136330 BR freetype-devel with conditions
- #135050 firefox should own mozilla plugin dir

* Sat Oct 30 2004 Christopher Aillon <caillon@redhat.com> 0:0.99-1.0RC1.1
- Update to firefox-rc1
- Add patch for s390(x)

* Tue Oct 26 2004 Christopher Aillon <caillon@redhat.com>
- Fix LD_LIBRARY_PATH at startup (Steve Knodle)

* Fri Oct 22 2004 Christopher Aillon <caillon@redhat.com> 0:0.10.1-1.0PR1.21
- Prevent inlining of stack direction detection (#135255)

* Tue Oct 19 2004 Christopher Aillon <caillon@redhat.com> 0:0.10.1-1.0PR1.20
- More file chooser fixes:
    Pop up a confirmation dialog before overwriting files (#134648)
    Allow saving as complete once again
- Fix for upstream 263263.

* Tue Oct 19 2004 Christopher Aillon <caillon@redhat.com> 0:0.10.1-1.0PR1.18
- Fix for upstream 262689.

* Mon Oct 18 2004 Christopher Blizzard <blizzard@redhat.com 0:0.10.1-1.0PR1.16
- Update pango patch to one that defaults to off

* Mon Oct 18 2004 Christopher Blizzard <blizzard@redhat.com> 0:0.10.1-1.0PR1.15
- Fix problem where default apps aren't showing up in the download
  dialog (#136261)
- Fix default height being larger than the available area, cherry picked
  from upstream

* Mon Oct 18 2004 Christopher Blizzard <blizzard@redhat.com> 0:0.10.1-1.0PR1.13
- Actually turn on pango in the mozconfig

* Sat Oct 16 2004 Christopher Aillon <caillon@redhat.com> 0:0.10.1-1.0PR1.12
- Disable the default application checks. (#133713)
- Disable the software update feature. (#136017)

* Wed Oct 13 2004 Christopher Blizzard <blizzard@redhat.com>
- Use pango for rendering

* Tue Oct 12 2004 Christopher Aillon <caillon@redhat.com> 0:0.10.1-1.0PR1.10
- Fix for 64 bit crash at startup (b.m.o #256603)

* Fri Oct  8 2004 Christopher Aillon <caillon@redhat.com> 0:0.10.1-1.0PR1.9
- Fix compile issues (#134914)
- Add patch to fix button focus issues (#133507)
- Add patches to fix tab focus stealing issue (b.m.o #124750)

* Fri Oct  1 2004 Christopher Aillon <caillon@redhat.com> 0:0.10.1-1.0PR1.8
- Update to 0.10.1
- Fix tab switching keybindings (#133504)

* Fri Oct  1 2004 Bill Nottingham <notting@redhat.com> 0:0.10.0-1.0PR1.7
- filter out library Provides: and internal Requires:

* Thu Sep 30 2004 Christopher Aillon <caillon@redhat.com> 0:0.10.0-1.0PR1.6
- Prereq desktop-file-utils >= 0.9

* Thu Sep 30 2004 Christopher Aillon <caillon@redhat.com> 0:0.10.0-1.0PR1.5
- Add clipboard access prevention patch.

* Wed Sep 29 2004 Christopher Aillon <caillon@redhat.com> 0:0.10.0-1.0PR1.4
- Add the xul mime type to the .desktop file

* Tue Sep 28 2004 Christopher Aillon <caillon@redhat.com> 0:0.10.0-1.0PR1.3
- Backport the GTK+ file chooser.
- Update desktop database after uninstall.

* Mon Sep 27 2004 Christopher Aillon <caillon@redhat.com> 0:0.10.0-1.0PR1.2
- Change the vendor to mozilla not fedora
- Build with --disable-strip so debuginfo packages work (#133738)
- Add pkgconfig patch (bmo #261090)

* Fri Sep 24 2004 Christopher Aillon <caillon@redhat.com> 0:0.10.0-1.0PR1.1
- Add a BR for desktop-file-utils
- Update default configuration options to use the firefox mozconfig (#132916)
- Use Red Hat bookmarks (#133262)
- Update default homepage (#132721)
- Fix JS math on AMD64 (#133226)
- Build with MOZILLA_OFICIAL (#132917)

* Tue Sep 14 2004 Christopher Aillon <caillon@redhat.com> 0:0.10.0-1.0PR1.0
- Update to 1.0PR1
- Update man page references to say Firefox instead of Firebird
- Remove gcc34 and extensions patch; they are now upstream
- Update desktop database
- Minor tweaks to the .desktop file

* Fri Sep 03 2004 Christopher Aillon <caillon@redhat.com> 0:0.9.3-8
- Fixup .desktop entry Name, GenericName, and Comment (#131602)
- Add MimeType desktop entry (patch from jrb@redhat.com)
- Build with --disable-xprint

* Tue Aug 31 2004 Warren Togami <wtogami@redhat.com> 0:0.9.3-7
- rawhide import
- fedora.us #1765 NetBSD's freetype 2.1.8 compat patch

* Sun Aug 29 2004 Adrian Reber <adrian@lisas.de> 0:0.9.3-0.fdr.6
- and mng support is disabled again as it seams that there is
  no real mng support in the code

* Sat Aug 28 2004 Adrian Reber <adrian@lisas.de> 0:0.9.3-0.fdr.5
- remove ldconfig from scriptlets (bug #1846 comment #40)
- reenabled mng support (bug #1971)
- removed --enable-strip to let rpm to the stripping (bug #1971)
- honor system settings in firefox.sh (bug #1971)
- setting umask 022 in scriptlets (bug #1962)

* Sat Aug 07 2004 Adrian Reber <adrian@lisas.de> 0:0.9.3-0.fdr.4
- copy the icon to the right place(TM)

* Fri Aug 06 2004 Adrian Reber <adrian@lisas.de> 0:0.9.3-0.fdr.3
- readded the xpm removed in 0:0.9.2-0.fdr.5

* Thu Aug 05 2004 Adrian Reber <adrian@lisas.de> 0:0.9.3-0.fdr.2
- added mozilla-1.7-psfonts.patch from rawhide mozilla

* Thu Aug 05 2004 Adrian Reber <adrian@lisas.de> 0:0.9.3-0.fdr.1
- updated to 0.9.3
- removed following from .mozconfig:
    ac_add_options --with-system-mng
    ac_add_options --enable-xprint
    ac_add_options --disable-dtd-debug
    ac_add_options --disable-freetype2
    ac_add_options --enable-strip-libs
    ac_add_options --enable-reorder
    ac_add_options --enable-mathml
    ac_add_options --without-system-nspr

* Tue Aug 03 2004 Adrian Reber <adrian@lisas.de> 0:0.9.2-0.fdr.5
- applied parts of the patch from Matthias Saou (bug #1846)
- delete empty directories in %%{ffdir}/chrome
- more cosmetic changes to the spec file

* Wed Jul 14 2004 Adrian Reber <adrian@lisas.de> 0:0.9.2-0.fdr.4
- mozilla-default-plugin-less-annoying.patch readded

* Tue Jul 13 2004 Adrian Reber <adrian@lisas.de> 0:0.9.2-0.fdr.3
- added krb5-devel as build requirement

* Tue Jul 13 2004 Adrian Reber <adrian@lisas.de> 0:0.9.2-0.fdr.2
- added patch from bugzilla.mozilla.org (bug #247846)
- removed Xvfb hack

* Fri Jul 09 2004 Adrian Reber <adrian@lisas.de> 0:0.9.2-0.fdr.1
- updated to 0.9.2

* Mon Jul 05 2004 Warren Togami <wtogami@redhat.com> 0:0.9.1-0.fdr.3
- mharris suggestion for backwards compatibilty with Xvfb hack

* Tue Jun 29 2004 Adrian Reber <adrian@lisas.de> 0:0.9.1-0.fdr.2
- added massive hack from the debian package to create the
  extension directory

* Tue Jun 29 2004 Adrian Reber <adrian@lisas.de> 0:0.9.1-0.fdr.1
- updated to 0.9.1

* Wed Jun 17 2004 Adrian Reber <adrian@lisas.de> 0:0.9-0.fdr.4
- remove extensions patch
- add post hack to create extensions
- enable negotiateauth extension
- copy icon to browser/app/default.xpm
- --enable-official-branding

* Wed Jun 17 2004 Adrian Reber <adrian@lisas.de> 0:0.9-0.fdr.3
- extensions patch

* Wed Jun 16 2004 Adrian Reber <adrian@lisas.de> 0:0.9-0.fdr.2
- added gnome-vfs2-devel as BuildRequires
- added gcc-3.4 patch 

* Wed Jun 16 2004 Adrian Reber <adrian@lisas.de> 0:0.9-0.fdr.1
- updated to 0.9
- dropped x86_64 patches
- dropped xremote patches

* Wed May 26 2004 Adrian Reber <adrian@lisas.de> 0:0.8-0.fdr.13
- remove unused files: mozilla-config

* Sun May 23 2004 David Hill <djh[at]ii.net> 0:0.8-0.fdr.12
- update mozconfig (fixes bug #1443)
- installation directory includes version number

* Mon May 10 2004 Justin M. Forbes <64bit_fedora@comcast.net> 0:0.8-0.fdr.11
- merge x86_64 release 10 with fedora.us release 10 bump release to 11

* Mon Apr 19 2004 Justin M. Forbes <64bit_fedora@comcast.net> 0:0.8-0.fdr.10
- rebuild for FC2
- change Source71 to properly replace Source7 for maintainability

* Sun Apr 18 2004 Warren Togami <wtogami@redhat.com> 0:0.8-0.fdr.10
- 3rd xremote patch
- test -Os rather than -O2

* Sun Apr 18 2004 Gene Czarcinski <gene@czarc.net>
- more x86_64 fixes
- fix firefix-xremote-client for x86_64 (similar to what is done for
  firefox.sh.in)

* Sat Apr 03 2004 Warren Togami <wtogami@redhat.com> 0:0.8-0.fdr.9
- xremote patch for thunderbird integration #1113
- back out ugly hack from /usr/bin/firefox
- correct default bookmarks

* Wed Feb 25 2004 Adrian Reber <adrian@lisas.de> - 0:0.8-0.fdr.7
- readded the new firefox icons

* Sat Feb 21 2004 Adrian Reber <adrian@lisas.de> - 0:0.8-0.fdr.6
- removed new firefox icons

* Wed Feb 18 2004 Adrian Reber <adrian@lisas.de> - 0:0.8-0.fdr.5
- nothing

* Thu Feb 12 2004 Gene Czarcinski <czar@acm.org>
- update for x86_64 ... usr mozilla-1.6 patches
- change "firefox-i*" to "firefox-*" in above stuff

* Tue Feb 10 2004 Adrian Reber <adrian@lisas.de> - 0:0.8-0.fdr.4
- another icon changed

* Tue Feb 10 2004 Adrian Reber <adrian@lisas.de> - 0:0.8-0.fdr.3
- startup script modified

* Mon Feb 09 2004 Adrian Reber <adrian@lisas.de> - 0:0.8-0.fdr.2
- new firefox icon
- more s/firebird/firefox/

* Mon Feb 09 2004 Adrian Reber <adrian@lisas.de> - 0:0.8-0.fdr.1
- new version: 0.8
- new name: firefox

* Sun Oct 19 2003 Adrian Reber <adrian@lisas.de> - 0:0.7-0.fdr.2
- s/0.6.1/0.7/
- changed user-app-dir back to .phoenix as .mozilla-firebird
  is not working as expected
- manpage now also available as MozillaFirebird.1

* Thu Oct 16 2003 Adrian Reber <adrian@lisas.de> - 0:0.7-0.fdr.1
- updated to 0.7
- provides webclient
- run regxpcom and regchrome after installation and removal
- added a man page from the debian package
- changed user-app-dir from .phoenix to .mozilla-firebird

* Tue Jul 29 2003 Adrian Reber <adrian@lisas.de> - 0:0.6.1-0.fdr.2
- now with mozilla-default-plugin-less-annoying.patch; see bug #586

* Tue Jul 29 2003 Adrian Reber <adrian@lisas.de> - 0:0.6.1-0.fdr.1
- updated to 0.6.1
- changed buildrequires for XFree86-devel from 0:4.3.0 to 0:4.2.1 
  it should now also build on RH80

* Sun Jul 13 2003 Adrian Reber <adrian@lisas.de> - 0:0.6-0.fdr.5.rh90
- enabled the type ahead extension: bug #484

* Sun Jul 13 2003 Adrian Reber <adrian@lisas.de> - 0:0.6-0.fdr.4.rh90
- renamed it again back to MozillaFirbird
- added libmng-devel to BuildRequires
- startup homepage is now www.fedora.us
- improved the startup script to use the unix remote protocol 
  to open a new window

* Thu May 19 2003 Adrian Reber <adrian@lisas.de> - 0:0.6-0.fdr.3.rh90
- new icon from http://iconpacks.mozdev.org/phoenix/iconshots/flame48true.png
- now using gtk2 as toolkit
- renamed again back to mozilla-firebird (I like it better)
- Provides: MozillaFirebird for compatibility with previous releases
- changed default bookmarks.html to contain links to www.fedora.us

* Thu May 19 2003 Adrian Reber <adrian@lisas.de> - 0:0.6-0.fdr.2.rh90
- renamed package to MozillaFirebird and all files with the old name
- enabled mng, mathml, xinerama support
- now honouring RPM_OPT_FLAGS

* Thu May 19 2003 Adrian Reber <adrian@lisas.de> - 0:0.6-0.fdr.1.rh90
- updated to 0.6

* Thu May 01 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.6-0.fdr.0.1.cvs20030501.rh90
- Updated to CVS.
- Renamed to mozilla-firebird.

* Sat Apr 05 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.6-0.fdr.0.3.cvs20030409.rh90
- Updated to CVS.
- Removed hard-coded library path.

* Sat Apr 05 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.6-0.fdr.0.3.cvs20030402.rh90
- Changed Prereq to Requires.
- Changed BuildRequires to gtk+-devel (instead of file).
- Recompressed source with bzip2.
- Removed post.

* Tue Apr 02 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.6-0.fdr.0.2.cvs20030402.rh90
- Added desktop-file-utils to BuildRequires.
- Changed category to X-Fedora-Extra.
- Updated to CVS.

* Sun Mar 30 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.6-0.fdr.0.2.cvs20030328.rh90
- Added Epoch:0.
- Added libgtk-1.2.so.0 to the BuildRequires

* Fri Mar 28 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.6-0.fdr.0.1.cvs20030328.rh90
- Updated to latest CVS.
- Moved phoenix startup script into its own file

* Wed Mar 26 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.6-0.fdr.0.1.cvs20030326.rh90
- Updated to latest CVS.
- Changed release to 9 vs 8.1.
- Added cvs script.
- added encoding to desktop file.

* Sun Mar 23 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.6-0.fdr.0.1.cvs20030323.rh81
- Updated to latest CVS.
- added release specification XFree86-devel Build Requirement.
- changed chmod to %attr

* Fri Mar 21 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.6-0.fdr.0.1.cvs20030317.rh81
- Fixed naming scheme.
- Fixed .desktop file.

* Mon Mar 17 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.6-cvs20030317.1
- Updated to CVS.

* Fri Mar 14 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.6-cvs20030313.2
- General Tweaking.

* Thu Mar 13 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.6-cvs20030313.1
- Updated CVS.
- Modified mozconfig.

* Sun Mar 09 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.6-cvs20030309.1
- Initial RPM release.
