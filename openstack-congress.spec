# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%global pypi_name congress

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global with_doc 1

%global common_desc \
OpenStack Congress Service is an open policy framework for OpenStack

Name:           openstack-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack Congress Service

License:        ASL 2.0
URL:            https://launchpad.net/%{pypi_name}
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{name}-%{upstream_version}.tar.gz
Source1:        openstack-congress-server.service
Source2:        congress.logrotate

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-aodhclient
BuildRequires:  python%{pyver}-cinderclient
BuildRequires:  python%{pyver}-eventlet
BuildRequires:  python%{pyver}-futurist
BuildRequires:  python%{pyver}-glanceclient
BuildRequires:  python%{pyver}-heatclient
BuildRequires:  python%{pyver}-ironicclient
BuildRequires:  python%{pyver}-keystoneauth1
BuildRequires:  python%{pyver}-keystonemiddleware
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-monascaclient
BuildRequires:  python%{pyver}-mox3
BuildRequires:  python%{pyver}-muranoclient
BuildRequires:  python%{pyver}-neutronclient
BuildRequires:  python%{pyver}-novaclient
BuildRequires:  python%{pyver}-os-testr
BuildRequires:  python%{pyver}-oslo-db
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-oslo-concurrency
BuildRequires:  python%{pyver}-oslo-log
BuildRequires:  python%{pyver}-oslo-messaging
BuildRequires:  python%{pyver}-oslo-middleware
BuildRequires:  python%{pyver}-oslo-policy
BuildRequires:  python%{pyver}-oslo-vmware
BuildRequires:  python%{pyver}-PuLP
BuildRequires:  python%{pyver}-swiftclient
BuildRequires:  python%{pyver}-tenacity
BuildRequires:  systemd
BuildRequires:  openstack-macros

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-jsonpath-rw
BuildRequires:  python-psycopg2
%else
BuildRequires:  python%{pyver}-jsonpath-rw
BuildRequires:  python%{pyver}-psycopg2
%endif

Requires:  python%{pyver}-congressclient
Requires:  python%{pyver}-heat-translator
Requires:  python%{pyver}-paramiko
Requires:  python%{pyver}-tosca-parser
Requires:  python%{pyver}-antlr3runtime

Requires: openstack-%{pypi_name}-common = %{version}-%{release}

Requires(pre): shadow-utils
%if 0%{?rhel} && 0%{?rhel} < 8
%{?systemd_requires}
%else
%{?systemd_ordering} # does not exist on EL7
%endif

%description
OpenStack Congress is Policy Management for OpenStack.

%package -n     python%{pyver}-%{pypi_name}
Summary:        OpenStack Congress Service
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}


Requires: python%{pyver}-aodhclient >= 0.9.0
Requires: python%{pyver}-eventlet
Requires: python%{pyver}-keystoneauth1 >= 3.4.0
Requires: python%{pyver}-keystonemiddleware >= 4.17.0
Requires: python%{pyver}-pbr
Requires: python%{pyver}-keystoneclient >= 1:3.8.0
Requires: python%{pyver}-heatclient >= 1.10.0
Requires: python%{pyver}-mistralclient >= 3.1.0
Requires: python%{pyver}-muranoclient >= 0.8.2
Requires: python%{pyver}-novaclient >= 1:9.1.0
Requires: python%{pyver}-neutronclient >= 6.7.0
Requires: python%{pyver}-cinderclient >= 3.3.0
Requires: python%{pyver}-swiftclient >= 3.2.0
Requires: python%{pyver}-ironicclient >= 2.3.0
Requires: python%{pyver}-alembic
Requires: python%{pyver}-glanceclient  >= 1:2.8.0
Requires: python%{pyver}-tackerclient  >= 0.8.0
Requires: python%{pyver}-routes
Requires: python%{pyver}-six
Requires: python%{pyver}-oslo-concurrency >= 3.26.0
Requires: python%{pyver}-oslo-config >= 2:5.2.0
Requires: python%{pyver}-oslo-context >= 2.19.2
Requires: python%{pyver}-oslo-db >= 4.27.0
Requires: python%{pyver}-oslo-messaging >= 5.29.0
Requires: python%{pyver}-oslo-policy >= 1.30.0
Requires: python%{pyver}-oslo-serialization >= 2.18.0
Requires: python%{pyver}-oslo-service >= 1.24.0
Requires: python%{pyver}-oslo-utils >= 3.33.0
Requires: python%{pyver}-oslo-middleware >= 3.31.0
Requires: python%{pyver}-oslo-vmware >= 2.17.0
Requires: python%{pyver}-oslo-log >= 3.36.0
Requires: python%{pyver}-oslo-upgradecheck >= 0.1.0
Requires: python%{pyver}-webob
Requires: python%{pyver}-netaddr >= 0.7.18
Requires: python%{pyver}-cryptography >= 2.1
Requires: python%{pyver}-jsonschema >= 2.6.0
Requires: python%{pyver}-monascaclient >= 1.12.1
Requires: python%{pyver}-requests >= 2.20.0
Requires: python%{pyver}-tenacity >= 4.4.0

# Handle python2 exception
%if %{pyver} == 2
Requires: python-PuLP
Requires: python-paste
Requires: python-paste-deploy
Requires: python-dateutil
Requires: python-jsonpath-rw
Requires: python-psycopg2
Requires: PyYAML
%else
Requires: python%{pyver}-PuLP
Requires: python%{pyver}-paste
Requires: python%{pyver}-paste-deploy
Requires: python%{pyver}-dateutil
Requires: python%{pyver}-jsonpath-rw
Requires: python%{pyver}-psycopg2
Requires: python%{pyver}-PyYAML
%endif

%description -n python%{pyver}-%{pypi_name}
%{common_desc}
This package contains the Congress python library.

%package common
Summary:  %{pypi_name} common files
Requires: python%{pyver}-%{pypi_name} = %{version}-%{release}

%description common
%{common_desc}

This package contains the Congress common files.

%package -n python%{pyver}-%{pypi_name}-tests
Summary:    Congress unit and functional tests
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}-tests}
Requires:   python%{pyver}-%{pypi_name} = %{version}-%{release}

Requires:  python%{pyver}-fixtures
Requires:  python%{pyver}-hacking
Requires:  python%{pyver}-mock
Requires:  python%{pyver}-oslotest
Requires:  python%{pyver}-os-testr
Requires:  python%{pyver}-subunit
Requires:  python%{pyver}-tenacity
Requires:  python%{pyver}-testrepository
Requires:  python%{pyver}-testtools

# Handle python2 exception
%if %{pyver} == 2
Requires: python-cliff
Requires:  python-webtest
%else
Requires: python%{pyver}-cliff
Requires:  python%{pyver}-webtest
%endif

%description -n python%{pyver}-%{pypi_name}-tests
%{common_desc}.

This package contains the Congress unit test files.

%if 0%{?with_doc}
# Documentation package
%package -n python%{pyver}-%{pypi_name}-doc
Summary:        Documentation for OpenStack Congress service
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}-doc}

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-oslo-upgradecheck
BuildRequires:  python%{pyver}-mistralclient
BuildRequires:  python%{pyver}-sphinxcontrib-apidoc
BuildRequires:  python%{pyver}-tackerclient

%description -n python%{pyver}-%{pypi_name}-doc
Documentation for OpenStack Congress service
%endif

# antlr3runtime
%package -n python%{pyver}-antlr3runtime
Summary:        Antlr 3 Runtime built buy OpenStack Congress
%{?python_provide:%python_provide python%{pyver}-antlr3runtime}
License: BSD

%description -n python%{pyver}-antlr3runtime
Antlr 3 Runtime built buy OpenStack Congress

%prep
%autosetup -n openstack-%{pypi_name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# Remove python2 specific code when building non py2 package as this leads to failing bytecompilation
%if %{pyver} != 2
rm -rf congress/datalog/Python2 antlr3runtime/Python
%endif

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{pyver_build}

# Generate sample config and add the current directory to PYTHONPATH so
# oslo-config-generator-%{pyver} doesn't skip congress entry points.
PYTHONPATH=. oslo-config-generator-%{pyver} --config-file=./etc/%{pypi_name}-config-generator.conf --output-file=./etc/%{pypi_name}.conf

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sphinx-build-%{pyver} -W -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/%{pypi_name}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{pypi_name}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{pypi_name}

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/%{pypi_name}
install -p -D -m 640 etc/%{pypi_name}.conf %{buildroot}%{_sysconfdir}/%{pypi_name}/%{pypi_name}.conf
install -d -m 750 %{buildroot}%{_sysconfdir}/%{pypi_name}/keys
mv %{buildroot}%{_prefix}/etc/%{pypi_name}/api-paste.ini %{buildroot}%{_sysconfdir}/%{pypi_name}/api-paste.ini
# Remove duplicate config files under /usr/etc/congress
rmdir %{buildroot}%{_prefix}/etc/%{pypi_name}

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-%{pypi_name}

# Install systemd units
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/openstack-%{pypi_name}-server.service

#%check
# FIXME: tests are taking too long, investigate if they are hung or simply need more time
#PYTHONPATH=. %{pyver_bin} setup.py testr
#%if 0%{with tests}
#PYTHONPATH=/usr/share/openstack-dashboard/ ./run_tests.sh -N -P
#%endif

%pre common
getent group %{pypi_name} >/dev/null || groupadd -r %{pypi_name}
getent passwd %{pypi_name} >/dev/null || \
    useradd -r -g %{pypi_name} -d %{_sharedstatedir}/%{pypi_name} -s /sbin/nologin \
    -c "OpenStack Congress Daemons" %{pypi_name}
exit 0

%post
%systemd_post openstack-%{pypi_name}-server.service

%preun
%systemd_preun openstack-%{pypi_name}-server.service

%postun
%systemd_postun_with_restart openstack-%{pypi_name}-server.service

%files
%license LICENSE
%{_bindir}/%{pypi_name}*
%{_unitdir}/openstack-%{pypi_name}-server.service

%files -n python%{pyver}-%{pypi_name}-tests
%license LICENSE
%{pyver_sitelib}/%{pypi_name}/tests

%files -n python%{pyver}-%{pypi_name}
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{pypi_name}
%{pyver_sitelib}/openstack_%{pypi_name}-*.egg-info
%exclude %{pyver_sitelib}/%{pypi_name}/tests

%files common
%license LICENSE
%doc README.rst
%dir %{_sysconfdir}/%{pypi_name}
%config(noreplace) %attr(0640, root, %{pypi_name}) %{_sysconfdir}/%{pypi_name}/%{pypi_name}.conf
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/%{pypi_name}/api-paste.ini
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-%{pypi_name}
%dir %attr(0750, %{pypi_name}, root) %{_sysconfdir}/%{pypi_name}/keys
%dir %attr(0750, %{pypi_name}, root) %{_localstatedir}/log/%{pypi_name}
%dir %{_sharedstatedir}/%{pypi_name}
%dir %{_datadir}/%{pypi_name}

%if 0%{?with_doc}
%files -n python%{pyver}-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python%{pyver}-antlr3runtime
%license thirdparty/antlr3-antlr-3.5/LICENSE.txt
%{pyver_sitelib}/antlr3runtime
%if %{pyver} == 2
%exclude %{pyver_sitelib}/antlr3runtime/Python3
%else
%exclude %{pyver_sitelib}/antlr3runtime/Python
%endif

%changelog
