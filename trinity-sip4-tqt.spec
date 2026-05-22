%bcond clang 1

# TDE variables
%define tde_pkg sip4-tqt
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:		trinity-%{tde_pkg}
Version:	14.1.6
Release:	1
Summary:	Python/C++ bindings generator runtime library
Group:		Development/Tools/Building
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{version}/main/dependencies/%{tarball_name}-%{version}.tar.xz

BuildRequires:  pkgconfig(tqt-mt)
BuildRequires:	pkgconfig(tqt)
BuildRequires:	trinity-filesystem >= %{version}

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:  make

# BISON support
BuildRequires:  bison

# FLEX support
BuildRequires:	flex

# PYTHON support
BuildRequires:  pkgconfig(python)
BuildRequires:  python%{pyver}dist(setuptools)

%description
SIP is a tool for generating bindings for C++ classes with some ideas
borrowed from SWIG, but capable of tighter bindings because of its
specificity towards C++ and Python.

##########

%package -n sip4-tqt
Summary:	Python/C++ bindings generator (Runtime Library)
Group:		Development/Tools/Building
Requires:	trinity-filesystem >= %{version}
Requires:	pkgconfig(python)

%description -n sip4-tqt
SIP is a tool for generating bindings for C++ classes with some ideas
borrowed from SWIG, but capable of tighter bindings because of its
specificity towards C++ and Python.

%files -n sip4-tqt
%defattr(-,root,root,-)
%{python_sitearch}/sip_tqt.so
%{python_sitearch}/sip_tqt_config.py*
%{python_sitearch}/sip_tqt_distutils.py*

##########

%package -n sip4-tqt-devel
Summary:		Python/C++ bindings generator (Development Files)
Group:			Development/Libraries/Python
Requires:		sip4-tqt = %{EVRD}

Requires:    pkgconfig(python)

%description -n sip4-tqt-devel
SIP is a tool for generating bindings for C++ classes with some ideas
borrowed from SWIG, but capable of tighter bindings because of its
specificity towards C++ and Python.

SIP was originally designed to generate Python bindings for KDE and so
has explicit support for the signal slot mechanism used by the Qt/KDE
class libraries.

Features:
- connecting TQt signals to Python functions and class methods
- connecting Python signals to TQt slots
- overloading virtual member functions with Python class methods
- protected member functions
- abstract classes
- enumerated types
- global class instances
- static member functions.

This package contains the code generator tool and the development headers
needed to develop Python bindings with sip.

%files -n sip4-tqt-devel
%defattr(-,root,root,-)
%{tde_prefix}/bin/sip-tqt
%{tde_prefix}/include/sip-tqt.h

%prep
%autosetup -n %{tarball_name}-%{version}


%build
# unset QTDIR QTINC QTLIB

mkdir build
cd build
%__python ../configure.py \
	-b %{tde_prefix}/bin \
	-d %{python_sitearch} \
	-e %{tde_prefix}/include \
	-u STRIP="" \
  %{?with_clang:-p linux-clang} \
	CFLAGS="${RPM_OPT_FLAGS} -I%{_includedir}/tqt -I%{_includedir}/tqt3 -I${PWD}/../sipgen -DYYERROR_VERBOSE" \
	CXXFLAGS="${RPM_OPT_FLAGS} -I%{_includedir}/tqt -I%{_includedir}/tqt3 -I${PWD}/../sipgen -DYYERROR_VERBOSE"

%install
%__make install DESTDIR=%{?buildroot} -C build

