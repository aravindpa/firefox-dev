%define desktop_file_utils_version 0.3

ExclusiveArch: i386 x86_64 ia64 ppc

Summary:        Mozilla Firefox Web browser.
Name:           firefox
Version:        0.10.0
Release:        1.0PR1.1
Epoch:          0
URL:            http://www.mozilla.org/projects/firefox/
License:        MPL/LGPL
Group:          Applications/Internet
Source0:        http://ftp.mozilla.org/pub/mozilla.org/firefox/releases/0.10/firefox-1.0PR-source.tar.bz2
Source1:        firefox-redhat-default-bookmarks.html
Source2:        mozconfig-firefox
Source3:        firefox.desktop
Source4:        firefox.png
Source6:        firefox.sh.in
Source7:        firefox-xremote-client.sh.in
Source8:        firefox.1
Source9:        firefox-rebuild-databases.pl.in
Source10:       firefox.xpm
Patch1:         firefox-redhat-homepage.patch
Patch2:         firefox-0.7.3-default-plugin-less-annoying.patch
Patch3:         firefox-0.7.3-psfonts.patch
Patch4:         firefox-0.7.3-freetype-compile.patch
Patch100:       firefox-PR1-js-64bit-math.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libpng-devel, libjpeg-devel
BuildRequires:  zlib-devel, zip
BuildRequires:  ORBit-devel, libIDL-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gtk2-devel, gnome-vfs2-devel
BuildRequires:  krb5-devel
BuildRequires:  desktop-file-utils >= %{desktop_file_utils_version}
Obsoletes:      phoenix, mozilla-firebird, MozillaFirebird
Provides:       mozilla-firebird = %{epoch}:%{version}, MozillaFirebird = %{epoch}:%{version}
Provides:       webclient
%define ffdir %{_libdir}/firefox-%{version}

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

#---------------------------------------------------------------------

%prep
%setup -q -n mozilla
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p0
%patch100 -p0
%{__rm} -f .mozconfig
%{__cp} %{SOURCE2} .mozconfig

# set up our default bookmarks
%{__cp} %{SOURCE1} $RPM_BUILD_DIR/mozilla/profile/defaults/bookmarks.html


#---------------------------------------------------------------------

%build
export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed s/-O2/-Os/`
export MOZILLA_OFFICIAL=1
export BUILD_OFFICIAL=1
MAKE="gmake %{?_smp_mflags}" make -f client.mk build

#---------------------------------------------------------------------

%install
%{__rm} -rf $RPM_BUILD_ROOT

cd xpinstall/packager/
%{__make} MOZILLA_BIN="\$(DIST)/bin/firefox-bin"
cd -

%{__mkdir_p} $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_datadir}/applications}

%{__tar} -C $RPM_BUILD_ROOT%{_libdir}/ -xzf dist/firefox-*-linux-gnu.tar.gz
%{__mv} $RPM_BUILD_ROOT%{_libdir}/firefox $RPM_BUILD_ROOT%{ffdir}

%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/firefox-*-linux-gnu.tar

%{__install} -p -D %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/pixmaps/firefox.png

desktop-file-install --vendor fedora \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category X-Fedora \
  --add-category Application \
  --add-category Network \
  %{SOURCE3} 

%{__cat} %{SOURCE6} | %{__sed} -e 's,FFDIR,%{ffdir},g' -e 's,LIBDIR,%{_libdir},g' > \
  $RPM_BUILD_ROOT%{_bindir}/firefox

%{__chmod} 755 $RPM_BUILD_ROOT%{_bindir}/firefox

%{__install} -p -D %{SOURCE1} $RPM_BUILD_ROOT%{ffdir}/defaults/profile/US/bookmarks.html
%{__install} -p -D %{SOURCE1} $RPM_BUILD_ROOT%{ffdir}/defaults/profile/bookmarks.html
%{__cat} %{SOURCE7} | %{__sed} -e 's,FFDIR,%{ffdir},g' -e 's,LIBDIR,%{_libdir},g' > \
  $RPM_BUILD_ROOT%{ffdir}/firefox-xremote-client

%{__chmod} 755 $RPM_BUILD_ROOT%{ffdir}/firefox-xremote-client
%{__install} -p -D %{SOURCE8} $RPM_BUILD_ROOT%{_mandir}/man1/firefox.1
%{__cat} %{SOURCE9} | %{__sed} -e 's,FFDIR,%{ffdir},g' > \
  $RPM_BUILD_ROOT/%{ffdir}/firefox-rebuild-databases.pl
%{__chmod} 755 $RPM_BUILD_ROOT/%{ffdir}/firefox-rebuild-databases.pl

%{__rm} -f $RPM_BUILD_ROOT%{ffdir}/firefox-config

cd $RPM_BUILD_ROOT%{ffdir}/chrome
find . -name "*" -type d -maxdepth 1 -exec %{__rm} -rf {} \;
cd -

# another bug fixed by looking at the debian package
%{__mkdir_p} $RPM_BUILD_ROOT%{ffdir}/chrome/icons/default/
%{__cp} %{SOURCE10} $RPM_BUILD_ROOT%{ffdir}/chrome/icons/default/default.xpm
%{__cp} %{SOURCE10} $RPM_BUILD_ROOT%{ffdir}/icons/default.xpm

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
%{ffdir}
%{_datadir}/applications/fedora-%{name}.desktop
%{_datadir}/pixmaps/firefox.png

#---------------------------------------------------------------------

%changelog
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
