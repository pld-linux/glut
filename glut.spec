Summary:	OpenGL Utility Toolkit (GLUT)
Summary(pl):	OpenGL Utility Toolkit (GLUT)
Name:		glut
Version:	3.7
Release:	2
License:	GPL
Group:		X11/Libraries
Group(pl):	X11/Biblioteki
Source0:	http://reality.sgi.com/mjk_asd/glut3/%name-%version.tar.gz
Source1:	http://reality.sgi.com/mjk_asd/glut3/%name-3.spec.ps.gz
Source2:	http://reality.sgi.com/mjk_asd/glut3/%name-3.spec.pdf
URL:		http://reality.sgi.com/mjk_asd/glut3
Obsoletes:	Mesa-glut
BuildRequires:	Mesa-devel >= 3.0
Buildroot:	/tmp/%{name}-%{version}-root-%(id -u -n)

%define	_prefix	/usr/X11R6
%define	_mandir	/usr/X11R6/man
%define	_examplesdir	/usr/src/examples

%description
A 3-D graphics library which uses the OpenGL API.

%description -l pl
Biblioteka graficzna 3D u¿ywaj±ca API z OpenGLa.

%package	devel
Summary:	GLUT Development environment
Summary(pl):	¦rodowisko programistyczne GLUT
Group:		X11/Development/Libraries
Group(pl):	X11/Programowanie/Biblioteki
Obsoletes:	Mesa-glut-devel
Requires:	%{name} = %{version}

%description devel
Header files needed for development aplications using GLUT library.

%description -l pl devel
Pliki nag³ówkowe dla biblioteki GLUT.

%package	static
Summary:	GLUT Static libraries
Summary(pl):	Biblioteki statyczne do biblioteki GLUT
Group:		X11/Development/Libraries
Group(pl):	X11/Programowanie/Biblioteki
Obsoletes:	Mesa-glut-static
Requires:	%{name}-devel = %{version}

%description static
The static version of the GLUT library.

%description -l pl static
Biblioteki statyczne dla biblioteki GLUT.

%package	examples
Summary:	GLUT demonstration programs.
Summary(pl):	GLUT programy demonstracyjne.
Group:		X11/Development/Examples
Group(pl):	X11/Programowanie/Przyk³ady

%description examples
Sample program.

%description -l pl examples
Przyk³adowe programy.

%package	doc
Summary:	GLUT documentation
Summary(pl):	GLUT documentation
Group:		X11/Development/Libraries
Group(pl):	X11/Programowanie/Biblioteki

%description doc
GLUT documentation.

%description -l pl doc
Dokumentacja dla biblioteki GLUT.

%prep
%setup -q

%build
rm -f Glut.cf
cp linux/Glut.cf .
./mkmkfiles.imake
cd lib/glut
rm -f Makefile
cp ../../linux/Makefile .
make depend
make

#make libgle.a
(cd ../gle;make)

#make libglsmap.a
(cd ../glsmap;make)

#make libmui.a
(cd ../mui;make)

#prepare to make manuals
(cd ../../man;xmkmf)
(cd ../../man/gle; \
    sed s/XXX/\$\(MANDIR\)/ Imakefile > Imakefile.sed; \
    rm -f Imakefile; mv Imakefile.sed Imakefile; \
    xmkmf; \
    sed s/install::/ii::/ Makefile >Makefile.sed; \
    sed s/all::// Makefile.sed >Makefile.sed2; \
    rm -f Makefile; rm -f Makefile.sed; \
    sed s/ii::/install::/ Makefile.sed2 >Makefile)

install %{SOURCE1} $RPM_BUILD_DIR/%name-%version
install %{SOURCE2} $RPM_BUILD_DIR/%name-%version


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_mandir}/man3
install -d $RPM_BUILD_ROOT%{_includedir}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%name

install -s lib/glut/libglut.so.3.7 $RPM_BUILD_ROOT%{_libdir}

install lib/gle/libgle.a $RPM_BUILD_ROOT%{_libdir}

install lib/glsmap/libglsmap.a $RPM_BUILD_ROOT%{_libdir}

install lib/mui/libmui.a $RPM_BUILD_ROOT%{_libdir}

cp -rp include/* $RPM_BUILD_ROOT%{_includedir}

(cd man; make DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}/man3 install.man)

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man3/*
gzip -9nf NOTICE CHANGES FAQ.glut README*

#installing examples...
(cd progs; cp -Rp * $RPM_BUILD_ROOT%{_examplesdir}/%name)

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {CHANGES,NOTICE,FAQ.glut,README*}.gz
%attr(755,root,root) %{_libdir}/libglut.so.3.7

%files devel
%defattr(644,root,root,755)
%attr(644,root,root) %{_includedir}/GL/*.h
%attr(644,root,root) %{_includedir}/mui/*.h
%attr(644,root,root) %{_mandir}/man3/*

%files static
%attr(644,root,root) %{_libdir}/lib*.a

%files doc
%doc %name-3.spec.pdf %name-3.spec.ps.gz

%files examples
%defattr(644,root,root,755)
%dir %{_examplesdir}/%name/*
