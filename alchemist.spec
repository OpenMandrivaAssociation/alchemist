%define	major	0
%define libname %mklibname alchemist %{major}

Summary:	A multi-sourced configuration back-end
Name:		alchemist
Version:	1.0.37
Release:	%mkrel 4
License:	GPLv2+
Group:		System/Base
Source0:	%{name}-%{version}.tar.bz2
Patch0:         %{name}-1.0.37-fix-python2.6.patch
BuildRequires:	libxml2 >= 2.3.8
BuildRequires:	libxslt-devel >= 0.9.0
BuildRequires:	doxygen >= 1.2.7
BuildRequires:	python-devel
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	chrpath
BuildRequires:	multiarch-utils >= 1.0.3
BuildRoot:	%{_tmppath}/%{name}-%{version}-root


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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall

install -d %{buildroot}%{_mandir}
cd src
doxygen
cp -a doc/man/* %{buildroot}%{_mandir}/

python -O %{_libdir}/python%{pyver}/compileall.py %{buildroot}%py_platsitedir

%if %mdkversion >= 1020
%multiarch_includes %{buildroot}%{_includedir}/alchemist/alchemist.h
%multiarch_includes %{buildroot}%{_includedir}/alchemist/blackbox.h
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

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root,755)
%doc AUTHORS COPYING ChangeLog README
%dir %{_libdir}/alchemist
%dir %{_libdir}/alchemist/blackbox
%{_libdir}/lib*.so.*
%{_libdir}/alchemist/blackbox/*.so.*
%{_sysconfdir}/alchemist
%{_localstatedir}/cache/alchemist


%files -n %{libname}-devel
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README
%doc src/doc/html
%if %mdkversion >= 1020
%multiarch %{multiarch_includedir}/alchemist/alchemist.h
%multiarch %{multiarch_includedir}/alchemist/blackbox.h
%endif
%{_includedir}/alchemist/alchemist.h
%{_includedir}/alchemist/blackbox.h
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_mandir}/*/*
%{_libdir}/alchemist/blackbox/*a
%{_libdir}/alchemist/blackbox/*.so

%files -n python-alchemist
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README
%py_platsitedir/*


