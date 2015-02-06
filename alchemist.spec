%define	major	0
%define libname %mklibname alchemist %{major}
%define pyver 2.7
Summary:		A multi-sourced configuration back-end
Name:		alchemist
Version:		1.0.37
Release:		8
License:		GPLv2+
Group:		System/Base
Source0:		%{name}-%{version}.tar.bz2
Patch0:         %{name}-1.0.37-fix-python2.6.patch
Patch1:		%{name}-1.0.37-fix-underlinking.patch
BuildRequires:	libxml2 >= 2.3.8
BuildRequires:	pkgconfig(libxslt) >= 0.9.0
BuildRequires:	doxygen >= 1.2.7
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(glib-2.0) >= 2.0
BuildRequires:	chrpath
BuildRequires:	multiarch-utils >= 1.0.3

%description
The alchemist is a back-end configuration architecture, which provides
multi-sourced configuration at the data level, postponing translation to
native format until the last stage. It uses XML as an intermediary data
encoding, and can be extended to arbitrarily large configuration scenarios.

%package -n	%{libname}
Summary:	Shared libraries for alchemist
Group:		System/Libraries

%description -n %{libname}
The alchemist is a back-end configuration architecture, which provides
multi-sourced configuration at the data level, postponing translation to
native format until the last stage. It uses XML as an intermediary data
encoding, and can be extended to arbitrarily large configuration scenarios.

%package -n	%{libname}-devel
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	alchemist-devel libalchemist-devel

%description -n	%{libname}-devel
The alchemist is a back-end configuration architecture, which provides
multi-sourced configuration at the data level, postponing translation to
native format until the last stage. It uses XML as an intermediary data
encoding, and can be extended to arbitrarily large configuration scenarios.

This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package -n	python-alchemist
Summary:	Python bindings for alchemist apps
Group:		Development/Python
Requires:	%{libname} = %{version}
Provides:	alchemist
Requires:	python

%description -n	python-alchemist
The alchemist is a back-end configuration architecture, which provides
multi-sourced configuration at the data level, postponing translation to
native format until the last stage. It uses XML as an intermediary data
encoding, and can be extended to arbitrarily large configuration scenarios.

%prep

%setup -q
%patch0 -p1 -b .python26
%patch1 -p1
# lib64 fix
find -type f | xargs perl -pi -e "s|/usr/lib|%{_libdir}|g"

%build
export CFLAGS="-Wall -DNDEBUG -fPIC %{optflags}"
[ -f  /usr/share/automake/depcomp ] && cp -f /usr/share/automake/{depcomp,ylwrap} . || :

%configure2_5x \
    --enable-shared \
    --enable-static

%make

%install
%makeinstall

install -d %{buildroot}%{_mandir}
cd src
doxygen
cp -a doc/man/* %{buildroot}%{_mandir}/

python -O %{_libdir}/python%{pyver}/compileall.py %{buildroot}%py_platsitedir

%if %mdkversion >= 1020
%_multiarch_includes %{buildroot}%{_includedir}/alchemist/alchemist.h
%_multiarch_includes %{buildroot}%{_includedir}/alchemist/blackbox.h
%endif

# nuke rpath
chrpath -d %{buildroot}%{_libdir}/*.so
chrpath -d %{buildroot}%{_libdir}/alchemist/blackbox/*.so
chrpath -d %{buildroot}%py_platsitedir/*.so

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif


%files -n %{libname}
%doc AUTHORS COPYING ChangeLog README
%dir %{_libdir}/alchemist
%dir %{_libdir}/alchemist/blackbox
%{_libdir}/lib*.so.*
%{_libdir}/alchemist/blackbox/*.so.*
%{_sysconfdir}/alchemist
%{_localstatedir}/cache/alchemist


%files -n %{libname}-devel
%doc AUTHORS COPYING ChangeLog README
%doc src/doc/html
%{_includedir}/alchemist/alchemist.h
%{_includedir}/alchemist/blackbox.h
%{_libdir}/*.a
%{_libdir}/*.so
%{_mandir}/*/*
%{_libdir}/alchemist/blackbox/*a
%{_libdir}/alchemist/blackbox/*.so
%if %mdkversion >= 1020
%_multiarch %{multiarch_includedir}/alchemist/alchemist.h
%_multiarch %{multiarch_includedir}/alchemist/blackbox.h
%endif

%files -n python-alchemist
%doc AUTHORS COPYING ChangeLog README
%py_platsitedir/*




%changelog
* Mon Nov 08 2010 Funda Wang <fwang@mandriva.org> 1.0.37-7mdv2011.0
+ Revision: 595014
- rebuild for py2.7

  + Michael Scherer <misc@mandriva.org>
    - rebuild for python 2.7

* Thu May 21 2009 Jérôme Brenier <incubusss@mandriva.org> 1.0.37-5mdv2011.0
+ Revision: 378200
- patch to fix build with python 2.6 modified
- patch to fix underlinking added
- add a patch for build with python 2.6
- drop the old patch for pyhton 2.5
- fix license (GPLv2+)
- fix cache/alchemist location
- remove BR duplicate

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Thu Mar 13 2008 Andreas Hasenack <andreas@mandriva.com> 1.0.37-2mdv2008.1
+ Revision: 187663
- fixed group
- rebuild for 2008.1

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Sat Mar 10 2007 Stefan van der Eijk <stefan@mandriva.org> 1.0.37-1mdv2007.1
+ Revision: 140789
- 1.0.37

  + Nicolas Lécureuil <neoclust@mandriva.org>
    - Import alchemist

* Tue Jun 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.36-2mdv2007.0
- rebuild

* Mon May 23 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0.36-1mdk
- initial Mandriva import

* Thu Mar 03 2005 Tim Waugh <twaugh@redhat.com> 1.0.36-1
- Rebuild for new GCC.

* Mon Nov 08 2004 Jeremy Katz <katzj@redhat.com> - 1.0.35-1
- build for python 2.4

* Thu Sep 23 2004 Than Ngo <than@redhat.com> 1.0.34-1
- add Prereq: /sbin/ldconfig

