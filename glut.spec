Summary:	OpenGL Utility Toolkit (GLUT)
Summary(pl):	OpenGL Utility Toolkit (GLUT)
Name:		glut
Version:	3.7
Release:	9
License:	GPL
Group:		X11/Libraries
Source0:	http://reality.sgi.com/mjk_asd/glut3/%{name}-%{version}.tar.gz
Source1:	http://reality.sgi.com/mjk_asd/glut3/%{name}-3.spec.ps.gz
Patch0:		%{name}-examples-paths.patch
Patch1:		%{name}-link.patch
URL:		http://reality.sgi.com/mjk_asd/glut3/
BuildRequires:	OpenGL-devel
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	Mesa-glut
Requires:	OpenGL

%define 	_noautoreqdep	libGL.so.1 libGLU.so.1
%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
A 3-D graphics library which uses the OpenGL API.

%description -l pl
Biblioteka graficzna 3D u¿ywaj±ca API z OpenGL.

%package devel
Summary:	GLUT Development environment
Summary(pl):	¦rodowisko programistyczne GLUT
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}
Requires:	OpenGL-devel
Obsoletes:	Mesa-glut-devel

%description devel
Header files needed for development aplications using GLUT library.

%description devel -l pl
Pliki nag³ówkowe dla biblioteki GLUT.

%package static
Summary:	GLUT Static libraries
Summary(pl):	Biblioteki statyczne do biblioteki GLUT
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}
Obsoletes:	Mesa-glut-static

%description static
The static version of the GLUT library.

%description static -l pl
Biblioteki statyczne dla biblioteki GLUT.

%package examples
Summary:	GLUT demonstration programs
Summary(pl):	GLUT programy demonstracyjne
Group:		X11/Development/Libraries

%description examples
Sample programs.

%description examples -l pl
Przyk³adowe programy.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

install %{SOURCE1} .

%build
rm -f Glut.cf
cp -f linux/Glut.cf .
./mkmkfiles.imake
cd lib/glut
rm -f Makefile
cp -f ../../linux/Makefile .
%{__make} depend
%{__make} "BOOTSTRAPCFLAGS=%{rpmcflags} -fPIC" \
	"CDEBUGFLAGS=" "CCOPTIONS=%{rpmcflags} -fPIC" \
	"CXXDEBUGFLAGS=" "CXXOPTIONS=%{rpmcflags} -fPIC"

#make libglsmap.a
(cd ../glsmap; %{__make} "BOOTSTRAPCFLAGS=%{rpmcflags}" \
	"CDEBUGFLAGS=" "CCOPTIONS=%{rpmcflags}" \
	"CXXDEBUGFLAGS=" "CXXOPTIONS=%{rpmcflags}")

#make libmui.a
(cd ../mui; %{__make} "BOOTSTRAPCFLAGS=%{rpmcflags}" \
	"CDEBUGFLAGS=" "CCOPTIONS=%{rpmcflags}" \
	"CXXDEBUGFLAGS=" "CXXOPTIONS=%{rpmcflags}")

#prepare to make manuals
(cd ../../man
	sed s/gle// Imakefile > Imakefile.tmp
	mv -f Imakefile.tmp Imakefile
	xmkmf
)

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_mandir}/man3,%{_includedir}} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install lib/glut/libglut.so.*.* $RPM_BUILD_ROOT%{_libdir}
ln -sf libglut.so.3 $RPM_BUILD_ROOT%{_libdir}/libglut.so

install lib/*/lib*.a $RPM_BUILD_ROOT%{_libdir}

rm -f include/GL/tube.h
cp -rp include/* $RPM_BUILD_ROOT%{_includedir}

(cd man; make DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}/man3 install.man)

gzip -9nf NOTICE CHANGES FAQ.glut README*

#installing examples...
(cd progs
find . -name Makefile.win -o -name Makefile.sgi -o -name Makefile.bak | xargs rm -f
cp -rp * $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version})

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc *.gz
%{_includedir}/GL/*.h
%{_includedir}/mui
%{_libdir}/lib*.so
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
