#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# BUILD WARNING:
#  Remove qt-devel and qt3-devel and any kde*-devel on your system !
#  Having KDE libraries may cause FTBFS here !

# Note for RHEL6 / Fedora:
#  Do *NOT* use 'byacc' to build sip4-tqt.
#  Instead, use 'bison' with a wrapper shell script.
#  e.g. /usr/local/bin/yacc
#   contains 'bison --yacc $@'

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg sip4-tqt
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	4.10.5
Release:	%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Python/C++ bindings generator runtime library
Group:		Development/Tools/Building
URL:		http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}

Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/dependencies/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:	libtqt4-devel >= %{?epoch:%{epoch}:}4.2.0
BuildRequires:	trinity-filesystem >= %{tde_version}

%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif

# BISON support
BuildRequires:  bison

# FLEX support
BuildRequires:	flex

# PYTHON support
BuildRequires:  pkgconfig(python)

# YACC support
%if 0%{?rhel} >= 8 || 0%{?fedora} >= 31
BuildRequires:  byacc
%endif

%description

SIP is a tool for generating bindings for C++ classes with some ideas
borrowed from SWIG, but capable of tighter bindings because of its
specificity towards C++ and Python.

##########

%package -n sip4-tqt
Summary:	Python/C++ bindings generator (Runtime Library)
Group:		Development/Tools/Building
Requires:	trinity-filesystem >= %{tde_version}
Requires:	pkgconfig(python)

%description -n sip4-tqt
SIP is a tool for generating bindings for C++ classes with some ideas
borrowed from SWIG, but capable of tighter bindings because of its
specificity towards C++ and Python.

%files -n sip4-tqt
%defattr(-,root,root,-)
%{python_sitearch}/sip_tqt.so
%if 0%{?mdkversion} || 0%{?pclinuxos} || 0%{?rhel} == 7 || 0%{?suse_version}
%{python_sitearch}/sip_tqt_config.py*
%{python_sitearch}/sip_tqt_distutils.py*
%if 0%{?rhel} == 7
%{python_sitearch}/__pycache__/sip_tqt_config.*.pyc
%{python_sitearch}/__pycache__/sip_tqt_distutils.*.pyc
%endif
%else
%pycached %{python_sitearch}/sip_tqt_config.py
%pycached %{python_sitearch}/sip_tqt_distutils.py
%endif

##########

%package -n sip4-tqt-devel
Summary:		Python/C++ bindings generator (Development Files)
Group:			Development/Libraries/Python
Requires:		sip4-tqt = %{?epoch:%{epoch}:}%{version}-%{release}

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
%{tde_bindir}/sip-tqt
%{tde_includedir}/sip-tqt.h

##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
# unset QTDIR QTINC QTLIB
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

mkdir build
cd build
%__python ../configure.py \
	-b %{tde_bindir} \
	-d %{python_sitearch} \
	-e %{tde_includedir} \
	-u STRIP="" \
%if "%{?toolchain}" == "clang"
  -p linux-clang \
%endif
	CFLAGS="${RPM_OPT_FLAGS} -I%{_includedir}/tqt -I%{_includedir}/tqt3 -I${PWD}/../sipgen -DYYERROR_VERBOSE" \
	CXXFLAGS="${RPM_OPT_FLAGS} -I%{_includedir}/tqt -I%{_includedir}/tqt3 -I${PWD}/../sipgen -DYYERROR_VERBOSE"

%install
%__make install DESTDIR=%{?buildroot} -C build

