Summary:	OpenGL Utility Toolkit (GLUT)
Summary(pl):	OpenGL Utility Toolkit (GLUT)
Name:		glut
Version:	3.7
Release:	2
License:	GPL
Group:		X11/Libraries
Group(pl):	X11/Biblioteki
Source0:	http://reality.sgi.com/mjk_asd/glut3/%{name}-%{version}.tar.gz
Source1:	http://reality.sgi.com/mjk_asd/glut3/%{name}-3.spec.ps.gz
URL:		http://reality.sgi.com/mjk_asd/glut3/
Obsoletes:	Mesa-glut
BuildRequires:	Mesa-devel >= 3.0
Buildroot:	/tmp/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%define		_examplesdir	/usr/src/examples

%description
A 3-D graphics library which uses the OpenGL API.

%description -l pl
Biblioteka graficzna 3D używająca API z OpenGL.

%package devel
Summary:	GLUT Development environment
Summary(pl):	Środowisko programistyczne GLUT
Group:		X11/Development/Libraries
Group(pl):	X11/Programowanie/Biblioteki
Obsoletes:	Mesa-glut-devel
Requires:	%{name} = %{version}

%description devel
Header files needed for development aplications using GLUT library.

%description -l pl devel
Pliki nagłówkowe dla biblioteki GLUT.

%package static
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

%package examples
Summary:	GLUT demonstration programs
Summary(pl):	GLUT programy demonstracyjne
Group:		X11/Development/Examples
Group(pl):	X11/Programowanie/Przykłady

%description examples
Sample program.

%description -l pl examples
Przykładowe programy.

%prep
%setup -q

install %{SOURCE1} .

%build
rm -f Glut.cf
cp linux/Glut.cf .
./mkmkfiles.imake
cd lib/glut
rm -f Makefile
cp ../../linux/Makefile .
make depend
make CXXDEBUGFLAGS="$RPM_OPT_FALGS"

#make libgle.a
(cd ../gle;make CXXDEBUGFLAGS="$RPM_OPT_FALGS")

#make libglsmap.a
(cd ../glsmap;make CXXDEBUGFLAGS="$RPM_OPT_FALGS")

#make libmui.a
(cd ../mui;make CXXDEBUGFLAGS="$RPM_OPT_FALGS")

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

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_mandir}/man3,%{_includedir}} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}

install lib/glut/libglut.so.*.* $RPM_BUILD_ROOT%{_libdir}

install lib/*/lib*.a $RPM_BUILD_ROOT%{_libdir}

cp -rp include/* $RPM_BUILD_ROOT%{_includedir}

(cd man; make DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}/man3 install.man)

strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.*

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man3/* \
	NOTICE CHANGES FAQ.glut README*

#installing examples...
(cd progs; cp -rp * $RPM_BUILD_ROOT%{_examplesdir}/%{name})

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {CHANGES,NOTICE,FAQ.glut,README*}.gz
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc %{name}-3.spec.ps.gz
%{_includedir}/GL/*.h
%{_includedir}/mui
%{_mandir}/man3/*

%files static
%attr(644,root,root) %{_libdir}/lib*.a

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}
