Summary:	GLUT
Summary(pl):	GLUT
Name:		glut
Version:	3.7
Release:	1
License:	GPL
Group:		Libraries
Group(pl):	Biblioteki
Source0:	http://reality.sgi.com/mjk_asd/glut3/%name-%version.tar.gz
Source1:	http://reality.sgi.com/mjk_asd/glut3/%name-3.spec.ps.gz
URL:		http://reality.sgi.com/mjk_asd/glut3
Obsoletes:	Mesa-glut
Patch0:		
Buildroot:	/tmp/%{name}-%{version}-root-%(id -u -n)

%define	_prefix	/usr/X11R6
%define	_mandir	/usr/X11R6/man

%description


%description -l pl
 # optional package =====================

%package	devel
Summary:	GLUT Devel
Summary(pl):	GLUT Devel
Group:		Libraries/Development
######		Unknown group!
Group(pl):	Biblioteki/Programowanie
Obsoletes:	Mesa-glut-devel

%description devel


%description -l pl devel
 # end of optional package ==============

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

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc
%attr(755,root,root) %{_libdir}/libglut.so.3.7
# optional package

%files devel
%defattr(644,root,root,755)
%doc
%attr(644,root,root) %{_libdir}/lib*.a
#%attr(644,root,root) %{_includedir}/*.h
%attr(644,root,root) %{_mandir}/man3/*
#end of optional package
