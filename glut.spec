Summary:	OpenGL Utility Toolkit (GLUT)
Summary(pl):	OpenGL Utility Toolkit (GLUT)
Name:		glut
Version:	3.7
Release:	1
License:	GPL
Group:		X11/Libraries
Group(pl):	X11/Biblioteki
Source0:	http://reality.sgi.com/mjk_asd/glut3/%name-%version.tar.gz
Source1:	http://reality.sgi.com/mjk_asd/glut3/%name-3.spec.ps.gz
Source2:	http://reality.sgi.com/mjk_asd/glut3/%name-3.spec.pdf
URL:		http://reality.sgi.com/mjk_asd/glut3
Obsoletes:	Mesa-glut
#Patch0:		
BuildRequires:	Mesa-devel >= 3.0
Buildroot:	/tmp/%{name}-%{version}-root-%(id -u -n)

%define	_prefix	/usr/X11R6
%define	_mandir	/usr/X11R6/man

%description
A 3-D graphics library which uses the OpenGL API.

%description -l pl
Biblioteka graficzna 3D u¿ywaj±ca API z OpenGLa.

%package	devel
Summary:	GLUT Devel
Summary(pl):	GLUT Devel
Group:		Libraries/Development
######		Unknown group!
Group(pl):	Biblioteki/Programowanie
Obsoletes:	Mesa-glut-devel

%description devel
%description -l pl devel

%package	static
Summary:	GLUT Static
Summary(pl):	GLUT Static
Group:		Libraries/
######		Unknown group!
Group(pl):	Biblioteki/
Obsoletes:	Mesa-glut-static

%description static
%description -l pl static

%package	demos
Summary:	GLUT demonstration programs.
Summary(pl):	GLUT programy demonstracyjne.
Group:		Libraries/
######		Unknown group!
Group(pl):	Biblioteki/
BuildRequires:	Mesa-devel >= 3.0

%description demos
%description -l pl demos

%package	doc
Summary:	GLUT documentation
Summary(pl):	GLUT documentation
Group:		Libraries/
######		Unknown group!
Group(pl):	Biblioteki/

%description doc
%description -l pl doc

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

#temporary links used to compile demos program
ln -s libglut.so.3.7 libglut.so

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

cd ../../progs
make OPENGL=%{_libdir}/libMesaGL.so GLU=%{_libdir}/libMesaGLU.so

install %{SOURCE1} $RPM_BUILD_DIR/%name-%version
install %{SOURCE2} $RPM_BUILD_DIR/%name-%version


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_mandir}/man3
install -d $RPM_BUILD_ROOT%{_includedir}

install -s lib/glut/libglut.so.3.7 $RPM_BUILD_ROOT%{_libdir}

install lib/gle/libgle.a $RPM_BUILD_ROOT%{_libdir}

install lib/glsmap/libglsmap.a $RPM_BUILD_ROOT%{_libdir}

install lib/mui/libmui.a $RPM_BUILD_ROOT%{_libdir}

cp -rp include/* $RPM_BUILD_ROOT%{_includedir}

(cd man; make DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}/man3 install.man)

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man3/*
gzip -9nf NOTICE CHANGES FAQ.glut README*

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
#%doc
%attr(644,root,root) %{_includedir}/GL/*.h
%attr(644,root,root) %{_includedir}/mui/*.h
%attr(644,root,root) %{_mandir}/man3/*

%files static
%attr(644,root,root) %{_libdir}/lib*.a

%files doc
%doc %name-3.spec.pdf %name-3.spec.ps.gz

%files demos
