# NOTE: tests are disabled since should_be has not yet been packaged.
# To re-enable, uncomment the 'check' section and lines marked 'for tests'
%global run_tests 0
%global with_python3 1

Name:           python-gssapi
Version:        1.5.0
Release:        3%{?dist}
Summary:        Python Bindings for GSSAPI (RFC 2743/2744 and extensions)

License:        ISC
URL:            https://github.com/pythongssapi/python-gssapi
Source0:        https://github.com/pythongssapi/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

# Patches

BuildRequires:  python2-devel
BuildRequires:  krb5-devel >= 1.10
BuildRequires:  krb5-libs >= 1.10
BuildRequires:  python2-Cython >= 0.21
BuildRequires:  python2-setuptools
BuildRequires:  gcc

# For autosetup
BuildRequires: git

%if 0%{?run_tests}
BuildRequires:  %{_bindir}/tox
BuildRequires:  python2-nose
BuildRequires:  python2-nose-parameterized
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

%global _description\
A set of Python bindings to the GSSAPI C library providing both\
a high-level pythonic interfaces and a low-level interfaces\
which more closely matches RFC 2743.  Includes support for\
RFC 2743, as well as multiple extensions.

%description %_description

%package -n python2-gssapi
Summary: %summary
Requires:       krb5-libs >= 1.10
Requires:       python2-six
Requires:       python2-enum34
Requires:       python2-decorator
%{?python_provide:%python_provide python2-gssapi}

%description -n python2-gssapi %_description

%if 0%{?with_python3}
%package -n python3-gssapi
Summary:        Python 3 Bindings for GSSAPI (RFC 2743/2744 and extensions)

Requires:       krb5-libs >= 1.10
Requires:       python3-six
Requires:       python3-decorator

%description -n python3-gssapi
A set of Python 3 bindings to the GSSAPI C library providing both
a high-level pythonic interfaces and a low-level interfaces
which more closely matches RFC 2743.  Includes support for
RFC 2743, as well as multiple extensions.
%endif

%prep
%autosetup -S git -n %{name}-%{version}

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


%files -n python2-gssapi
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
* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.5.0-3
- Rebuilt for Python 3.7

* Tue May 08 2018 Robbie Harwood <rharwood@redhat.com> - 1.5.0-2
- Fix tox dependency

* Fri Apr 06 2018 Robbie Harwood <rharwood@redhat.com> - 1.5.0-1
- Prepare for release 1.5.0

* Wed Mar 07 2018 Robbie Harwood <rharwood@redhat.com> - 1.4.1-2
- Add gcc to build-deps

* Fri Feb 16 2018 Robbie Harwood <rharwood@redhat.com> - 1.4.1-1
- Prepare for release 1.4.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.3.0-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Dec 01 2017 Robbie Harwood <rharwood@redhat.com> - 1.3.0-1
- New upstream release v1.3.0

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2.0-8
- Python 2 binary package renamed to python2-gssapi
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr 04 2017 Robbie Harwood <rharwood@redhat.com> 1.2.0-5
- Fix problem where gss_display_status can infinite loop
- Move to autosetup and rpm-git-tree

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.2.0-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Mar 03 2016 Robbie Harwood <rharwood@redhat.com> - 1.2.0-1
- New upstream version 1.2.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 30 2015 Robbie Harwood <rharwood@redhat.com> - 1.1.4-1
- New upstream version 1.1.4
- Resolves #1286458

* Wed Nov 04 2015 Robert Kuska <rkuska@redhat.com> - 1.1.3-2
- Rebuilt for Python3.5 rebuild

* Fri Sep 04 2015 Robbie Harwood <rharwood@redhat.com> - 1.1.3-1
- New upstream minor release

* Thu Aug 20 2015 Simo Sorce <simo@redhat.com> - 1.1.2-1
- New minor release.
- Resolves #1254458
- Fixes a crash bug when inquiring incomplete security contexts

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 28 2015 Simo Sorce <simo@redhat.com> - 1.1.1-1
- New minor release.

* Thu Feb 19 2015 Solly Ross <sross@redhat.com> - 1.1.0-1
- Initial Packaging
