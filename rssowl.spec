%define gcj_support 1

Name:           rssowl
Summary:        RSS, RDF and Atom Newsreader
Version:        1.2.3
Release:        %mkrel 9
Epoch:          0
License:        CPL
Group:          Development/Java
URL:            http://www.rssowl.org/
Source0:        rssowl_1_2_3_src-CLEAN.tar.bz2
Source1:        %{name}.script
Source2:        %{name}.desktop
Patch0:         %{name}-use-jce.patch
Patch1:         %{name}-build0.patch
Patch3:         %{name}-build1.patch
Patch5:         %{name}-browser.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Requires:       java >= 0:1.4.2
Requires:       xerces-j2
BuildRequires:  java-devel >= 0:1.4.2
BuildRequires:  ImageMagick
BuildRequires:  ant, itext, jdom, jakarta-commons-codec, jakarta-commons-httpclient, eclipse-platform >= 1:3.3.0
BuildRequires:  libgconf-java
BuildRequires:  ant, jpackage-utils >= 0:1.5
BuildRequires:  xerces-j2
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%else
BuildArch:       noarch
%endif
Requires:         itext, jdom, jakarta-commons-codec, jakarta-commons-httpclient, eclipse-platform >= 1:3.3.0
Requires:         libgconf-java
Requires:         firefox-devel
BuildRequires:    desktop-file-utils
Requires(post):   desktop-file-utils
Requires(postun): desktop-file-utils

%description
RSSOwl is an RSS/RDF/Atom Newsreader written in Java using SWT as
fast graphic library. Read News in a tabfolder, save favorites in
categories, Export to PDF/RTF/HTML/OPML, Import Feeds from OPML,
perform fulltext-search, use the integrated browser.

%description -l de
RSSOwl ist ein RSS/RDF/Atom Newsreader in Java mit SWT als
GUI-Bibliothek. Einige der Features sind Export von Nachrichten nach
PDF/RTF/HTML, Import/Export mit OPML, Volltextsuche und der
integrierte Browser.

%prep
%setup -q -n rssowl_1_2_3_src
%patch0 -p0
%patch1 -p0
%patch3 -p0
%patch5 -p0
# This package doesn't contain any MPL licensed code.
rm doc/mpl-v11.txt
%{__perl} -pi -e 's/<javac/<javac debug="true"/g' src/build.xml

%build
export CLASSPATH=
export OPT_JAR_LIST=:
build-jar-repository -p lib swt-gtk jdom itext jakarta-commons-codec jakarta-commons-httpclient glib0.4 gconf2.12 gtk2.10 xerces-j2
ln -s %{_javadir}/itext.jar lib/iTextAsian.jar
ln -s /usr/share/eclipse/plugins/org.eclipse.jface_3*.jar lib
cd src
%{ant} deploy_linux

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_javadir}
install -m 644 rssowl.jar $RPM_BUILD_ROOT%{_javadir}/rssowl-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && %{__ln_s} rssowl-%{version}.jar rssowl.jar)

# FIXME:  do these really need to be converted?  Couldn't they be shipped as PNGs?
convert img/16x16.gif img/16x16.png
convert img/24x24.gif img/24x24.png
convert img/32x32.gif img/32x32.png
convert -resize 48x48 img/32x32.gif img/48x48.png
# FIXME:  this is ugly :)
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/24x24/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
install -m 644 img/32x32.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/rssowl.png
install -m 644 img/16x16.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/rssowl.png
install -m 644 img/24x24.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/24x24/apps/rssowl.png
install -m 644 img/32x32.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/rssowl.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
%{_bindir}/desktop-file-install --vendor ""                 \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/applications        \
        --add-category X-Mandriva-Internet-News                \
        %{SOURCE2}

mkdir -p $RPM_BUILD_ROOT/%{_bindir}
cp %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/%{name}
sed --in-place "s:/usr/lib:%{_libdir}:" \
  $RPM_BUILD_ROOT%{_bindir}/%{name}
sed --in-place "s:/usr/share:%{_datadir}:" \
  $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__perl} -pi -e 's|\@LIBDIR\@|%{_libdir}|g;' \
              -e 's|\@VERSION\@|2.0|g;' \
  %{buildroot}%{_bindir}/%{name}
chmod 755 $RPM_BUILD_ROOT/%{_bindir}/%{name}

%{__perl} -pi -e 's/\r$//g' doc/tutorial/en/*.html
%{__perl} -pi -e 's/\r$//g' doc/tutorial/en/styles/*
%{__perl} -pi -e 's/\r$//g' doc/*.{xml,html,txt,template}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%post 
%if %{gcj_support}
%{update_gcjdb}
%endif
%{update_desktop_database}
%update_icon_cache hicolor

%postun 
%if %{gcj_support}
%{clean_gcjdb}
%endif
%{clean_desktop_database}
%clean_icon_cache hicolor

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644, root, root, 0755)
%doc doc/*
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/16x16/apps/%%{name}.png
%{_datadir}/icons/hicolor/24x24/apps/%%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%%{name}.png
%attr(0755,root,root) %{_bindir}/%{name}
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif
