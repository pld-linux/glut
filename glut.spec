Summary:	OpenGL Utility Toolkit (GLUT)
Name:		glut
Version:	3.7
Release:	12
License:	GPL
Group:		Libraries
Source0:	http://www.opengl.org/resources/libraries/glut/%{name}-%{version}.tar.gz
# Source0-md5: dc932666e2a1c8a0b148a4c32d111ef3
Source1:	http://www.opengl.org/resources/libraries/glut/%{name}-3.spec.ps.gz
# Source1-md5:	7be4cfb04953bca413482890279c8b31
Patch0:		%{name}-examples-paths.patch
Patch1:		%{name}-link.patch
Patch2:		%{name}-lib64.patch
URL:		http://www.opengl.org/resources/libraries/glut.html
BuildRequires:	OpenGL-devel
BuildRequires:	/bin/csh
Requires:	OpenGL
Obsoletes:	Mesa-glut
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	_noautoreqdep	libGL.so.1 libGLU.so.1

%description
A 3-D graphics library which uses the OpenGL API.

%description -l pl
Biblioteka graficzna 3D używająca API z OpenGL.

%package devel
Summary:	GLUT Development environment
Summary(pl):	Środowisko programistyczne GLUT
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	OpenGL-devel
Obsoletes:	Mesa-glut-devel

%description devel
Header files needed for development aplications using GLUT library.

%description devel -l pl
Pliki nagłówkowe dla biblioteki GLUT.

%package static
Summary:	GLUT Static libraries
Summary(pl):	Biblioteki statyczne do biblioteki GLUT
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}
Obsoletes:	Mesa-glut-static

%description static
The static version of the GLUT library.

%description static -l pl
Biblioteki statyczne dla biblioteki GLUT.

%package examples
Summary:	GLUT demonstration programs
Summary(pl):	GLUT programy demonstracyjne
Group:		Development/Libraries

%description examples
Sample programs.

%description examples -l pl
Przykładowe programy.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%ifarch amd64
%patch2 -p1
%endif

install %{SOURCE1} .

%build
rm -f Glut.cf
cp -f linux/Glut.cf .
./mkmkfiles.imake

rm -f lib/glut/Makefile
cp -f linux/Makefile lib/glut

%{__make} -C lib/glut depend
%{__make} -C lib/glut \
	"BOOTSTRAPCFLAGS=%{rpmcflags} -fPIC" \
	"CDEBUGFLAGS=" \
	"CCOPTIONS=%{rpmcflags} -fPIC" \
	"CXXDEBUGFLAGS=" \
	"CXXOPTIONS=%{rpmcflags} -fPIC"

#make libglsmap.a
%{__make} -C lib/glsmap \
	"BOOTSTRAPCFLAGS=%{rpmcflags}" \
	"CDEBUGFLAGS=" \
	"CCOPTIONS=%{rpmcflags}" \
	"CXXDEBUGFLAGS=" \
	"CXXOPTIONS=%{rpmcflags}"

#make libmui.a
%{__make} -C lib/mui \
	"BOOTSTRAPCFLAGS=%{rpmcflags}" \
	"CDEBUGFLAGS=" \
	"CCOPTIONS=%{rpmcflags}" \
	"CXXDEBUGFLAGS=" \
	"CXXOPTIONS=%{rpmcflags}"

#prepare to make manuals
cd man
sed s/gle// Imakefile > Imakefile.tmp
mv -f Imakefile.tmp Imakefile
xmkmf
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_mandir}/man3,%{_includedir}} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install lib/glut/libglut.so.*.* $RPM_BUILD_ROOT%{_libdir}
ln -sf libglut.so.3 $RPM_BUILD_ROOT%{_libdir}/libglut.so

install lib/*/lib*.a $RPM_BUILD_ROOT%{_libdir}

rm -f include/GL/tube.h
cp -rp include/* $RPM_BUILD_ROOT%{_includedir}

%{__make} -C man install.man \
	DESTDIR=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}/man3

#installing examples...
cd progs
find . -name Makefile.win -o -name Makefile.sgi -o -name Makefile.bak | xargs rm -f
cp -rp * $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc NOTICE CHANGES FAQ.glut README*
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
