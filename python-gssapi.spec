# NOTE: tests are disabled since should_be has not yet been packaged.
# To re-enable, uncomment the 'check' section and lines marked 'for tests'
%global run_tests 0
%global with_python3 1

Name:           python-gssapi
Version:        1.2.0
Release:        1%{?dist}
Summary:        Python Bindings for GSSAPI (RFC 2743/2744 and extensions)

License:        ISC
URL:            https://github.com/pythongssapi/python-gssapi
Source0:        https://github.com/pythongssapi/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  python2-devel
BuildRequires:  krb5-devel >= 1.10
BuildRequires:  krb5-libs >= 1.10
BuildRequires:  Cython >= 0.21
BuildRequires:  python-setuptools
BuildRequires:  python-tox
Requires:       krb5-libs >= 1.10
Requires:       python-six
Requires:       python-enum34
Requires:       python-decorator

%if 0%{?run_tests}
BuildRequires:  python-nose
BuildRequires:  python-nose-parameterized
BuildRequires:  python-shouldbe
BuildRequires:  krb5-server >= 1.10
%endif

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-Cython

%if 0%{?run_tests}
BuildRequires:  python3-nose
BuildRequires:  python3-nose-parameterized
BuildRequires:  python3-should-be
%endif
%endif

%description
A set of Python bindings to the GSSAPI C library providing both
a high-level pythonic interfaces and a low-level interfaces
which more closely matches RFC 2743.  Includes support for
RFC 2743, as well as multiple extensions.

%if 0%{?with_python3}
%package -n python3-gssapi
Summary:        Python 3 Bindings for GSSAPI (RFC 2743/2744 and extensions)

Requires:       krb5-libs >= 1.10
Requires:       python3-six
Requires:       python3 >= 3.4
Requires:       python3-decorator

%description -n python3-gssapi
A set of Python 3 bindings to the GSSAPI C library providing both
a high-level pythonic interfaces and a low-level interfaces
which more closely matches RFC 2743.  Includes support for
RFC 2743, as well as multiple extensions.
%endif

%prep
%setup -q

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
CFLAGS="%{optflags}" %{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
popd
%endif


%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}

# fix permissions on shared objects (mock seems to set them
# to 0775, whereas a normal build gives 0755)
find %{buildroot}%{python3_sitearch}/gssapi -name '*.so' \
    -exec chmod 0755 {} \;

popd
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}

# fix permissions on shared objects (mock seems to set them
# to 0775, whereas a normal build gives 0755)
find %{buildroot}%{python2_sitearch}/gssapi -name '*.so' \
    -exec chmod 0755 {} \;

%check
%if 0%{?run_tests}
%{__python2} setup.py nosetests

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py nosetests
popd
%endif
%endif


%files
%doc README.txt
%license LICENSE.txt
%{python2_sitearch}/*

%if 0%{?with_python3}
%files -n python3-gssapi
%doc README.txt
%license LICENSE.txt
%{python3_sitearch}/*
%endif


%changelog
* Thu Mar 03 2016 Robbie Harwood <rharwood@redhat.com. - 1.2.0-1
- New upstream release 1.2.0 fixes delegated creds issue

* Fri Sep 04 2015 Robbie Harwood <rharwood@redhat.com> - 1.1.3-1
- New upstream minor release

* Thu Aug 20 2015 Simo Sorce <simo@redhat.com> - 1.1.2-1
- New minor release.
- Resolves #1254458
- Fixes a crash bug when inquiring incomplete security contexts

* Tue Apr 28 2015 Simo Sorce <simo@redhat.com> - 1.1.1-1
- New minor release.

* Thu Feb 19 2015 Solly Ross <sross@redhat.com> - 1.1.0-1
- Initial Packaging
