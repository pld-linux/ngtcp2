# TODO:
# - boringssl, picotls, wolfssl >= 5.5.0? (in -crypto-* subpackages)
#
# Conditional build:
%bcond_with	apidocs		# API documentation (files missing in tarball)
%bcond_without	static_libs	# static libraries
%bcond_without	gnutls		# gnutls crypto
%bcond_with	openssl		# openssl crypto (needs patched openssl)
#
Summary:	Effort to implement QUIC protocol (RFC 9000)
Summary(pl.UTF-8):	Próba implementacji protokołu QUIC (RFC 9000)
Name:		ngtcp2
Version:	0.19.0
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/ngtcp2/ngtcp2/releases
Source0:	https://github.com/ngtcp2/ngtcp2/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	62278184df29a743f742b37bf8c0bffc
URL:		https://github.com/ngtcp2/ngtcp2
%{?with_gnutls:BuildRequires:	gnutls-devel >= 3.7.3}
BuildRequires:	libev-devel
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	nghttp3-devel >= 0.2.0
%{?with_openssl:BuildRequires:	openssl-devel(quic) >= 1.1.1}
BuildRequires:	pkgconfig >= 1:0.20
BuildRequires:	rpm-build >= 4.6
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Effort to implement QUIC protocol (RFC 9000).

%description -l pl.UTF-8
Próba implementacji protokołu QUIC (RFC 9000).

%package devel
Summary:	Header files for ngtcp2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ngtcp2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for ngtcp2 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ngtcp2.

%package static
Summary:	Static ngtcp2 library
Summary(pl.UTF-8):	Statyczna biblioteka ngtcp2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ngtcp2 library.

%description static -l pl.UTF-8
Statyczna biblioteka ngtcp2.

%package crypto-gnutls
Summary:	gnutls crypto library for ngtcp2
Summary(pl.UTF-8):	Biblioteka kryptografii gnutls dla ngtcp2
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gnutls-libs >= 3.7.3

%description crypto-gnutls
gnutls crypto library for ngtcp2.

%description crypto-gnutls -l pl.UTF-8
Biblioteka kryptografii gnutls dla ngtcp2.

%package crypto-gnutls-devel
Summary:	Header files for gnutls crypto library for ngtcp2
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki kryptografii gnutls dla ngtcp2
Group:		Development/Libraries
Requires:	%{name}-crypto-gnutls = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	gnutls-devel >= 3.7.3

%description crypto-gnutls-devel
Header files for gnutls crypto library for ngtcp2.

%description crypto-gnutls-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki kryptografii gnutls dla ngtcp2.

%package crypto-gnutls-static
Summary:	Static gnutls crypto library for ngtcp2
Summary(pl.UTF-8):	Statyczna biblioteka kryptografii gnutls dla ngtcp2
Group:		Development/Libraries
Requires:	%{name}-crypto-gnutls-devel = %{version}-%{release}

%description crypto-gnutls-static
Static gnutls crypto library for ngtcp2.

%description crypto-gnutls-static -l pl.UTF-8
Statyczna biblioteka kryptografii gnutls dla ngtcp2.

%package apidocs
Summary:	API documentation for ngtcp2 library
Summary(pl.UTF-8):	Dokumentacja API biblioteki ngtcp2
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for ngtcp2 library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki ngtcp2.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	%{?with_gnutls:--with-gnutls} \
	%{!?with_openssl:--without-openssl}
%{__make}

%if %{with apidocs}
%{__make} -C doc html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libngtcp2*.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/ngtcp2

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	crypto-gnutls -p /sbin/ldconfig
%postun	crypto-gnutls -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README.rst
%attr(755,root,root) %{_libdir}/libngtcp2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libngtcp2.so.15

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libngtcp2.so
%dir %{_includedir}/ngtcp2
%{_includedir}/ngtcp2/ngtcp2.h
%{_includedir}/ngtcp2/ngtcp2_crypto.h
%{_includedir}/ngtcp2/version.h
%{_pkgconfigdir}/libngtcp2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libngtcp2.a
%endif

%if %{with gnutls}
%files crypto-gnutls
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libngtcp2_crypto_gnutls.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libngtcp2_crypto_gnutls.so.7

%files crypto-gnutls-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libngtcp2_crypto_gnutls.so
%{_includedir}/ngtcp2/ngtcp2_crypto_gnutls.h
%{_pkgconfigdir}/libngtcp2_crypto_gnutls.pc

%if %{with static_libs}
%files crypto-gnutls-static
%defattr(644,root,root,755)
%{_libdir}/libngtcp2_crypto_gnutls.a
%endif
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/*
%endif
