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
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-aodhclient
BuildRequires:  python3-cinderclient
BuildRequires:  python3-eventlet
BuildRequires:  python3-futurist
BuildRequires:  python3-glanceclient
BuildRequires:  python3-heatclient
BuildRequires:  python3-ironicclient
BuildRequires:  python3-keystoneauth1
BuildRequires:  python3-keystonemiddleware
BuildRequires:  python3-mock
BuildRequires:  python3-monascaclient
BuildRequires:  python3-mox3
BuildRequires:  python3-muranoclient
BuildRequires:  python3-neutronclient
BuildRequires:  python3-novaclient
BuildRequires:  python3-os-testr
BuildRequires:  python3-oslo-db
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-concurrency
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-messaging
BuildRequires:  python3-oslo-middleware
BuildRequires:  python3-oslo-policy
BuildRequires:  python3-oslo-vmware
BuildRequires:  python3-PuLP
BuildRequires:  python3-swiftclient
BuildRequires:  python3-tenacity
BuildRequires:  systemd
BuildRequires:  openstack-macros

BuildRequires:  python3-django-horizon
BuildRequires:  python3-jsonpath-rw
BuildRequires:  python3-psycopg2

Requires:  python3-congressclient
Requires:  python3-heat-translator
Requires:  python3-paramiko
Requires:  python3-tosca-parser
Requires:  python3-antlr3runtime

Requires: openstack-%{pypi_name}-common = %{version}-%{release}

Requires(pre): shadow-utils
%if 0%{?rhel} && 0%{?rhel} < 8
%{?systemd_requires}
%else
%{?systemd_ordering} # does not exist on EL7
%endif

%description
OpenStack Congress is Policy Management for OpenStack.

%package -n     python3-%{pypi_name}
Summary:        OpenStack Congress Service
%{?python_provide:%python_provide python3-%{pypi_name}}


Requires: python3-aodhclient >= 0.9.0
Requires: python3-eventlet
Requires: python3-keystoneauth1 >= 3.4.0
Requires: python3-keystonemiddleware >= 4.17.0
Requires: python3-pbr
Requires: python3-keystoneclient >= 1:3.8.0
Requires: python3-heatclient >= 1.10.0
Requires: python3-mistralclient >= 3.1.0
Requires: python3-muranoclient >= 0.8.2
Requires: python3-novaclient >= 1:9.1.0
Requires: python3-neutronclient >= 6.7.0
Requires: python3-cinderclient >= 3.3.0
Requires: python3-swiftclient >= 3.2.0
Requires: python3-ironicclient >= 2.3.0
Requires: python3-alembic
Requires: python3-glanceclient  >= 1:2.8.0
Requires: python3-tackerclient  >= 0.8.0
Requires: python3-routes
Requires: python3-six
Requires: python3-oslo-concurrency >= 3.26.0
Requires: python3-oslo-config >= 2:5.2.0
Requires: python3-oslo-context >= 2.19.2
Requires: python3-oslo-db >= 4.27.0
Requires: python3-oslo-messaging >= 5.29.0
Requires: python3-oslo-policy >= 1.30.0
Requires: python3-oslo-serialization >= 2.18.0
Requires: python3-oslo-service >= 1.24.0
Requires: python3-oslo-utils >= 3.33.0
Requires: python3-oslo-middleware >= 3.31.0
Requires: python3-oslo-vmware >= 2.17.0
Requires: python3-oslo-log >= 3.36.0
Requires: python3-oslo-upgradecheck >= 0.1.0
Requires: python3-webob
Requires: python3-netaddr >= 0.7.18
Requires: python3-cryptography >= 2.1
Requires: python3-jsonschema >= 2.6.0
Requires: python3-monascaclient >= 1.12.1
Requires: python3-requests >= 2.14.2
Requires: python3-tenacity >= 4.4.0

Requires: python3-PuLP
Requires: python3-paste
Requires: python3-paste-deploy
Requires: python3-dateutil
Requires: python3-jsonpath-rw
Requires: python3-psycopg2
Requires: python3-PyYAML

%description -n python3-%{pypi_name}
%{common_desc}
This package contains the Congress python library.

%package common
Summary:  %{pypi_name} common files
Requires: python3-%{pypi_name} = %{version}-%{release}

%description common
%{common_desc}

This package contains the Congress common files.

%package -n python3-%{pypi_name}-tests
Summary:    Congress unit and functional tests
%{?python_provide:%python_provide python3-%{pypi_name}-tests}
Requires:   python3-%{pypi_name} = %{version}-%{release}

Requires:  python3-fixtures
Requires:  python3-hacking
Requires:  python3-mock
Requires:  python3-oslotest
Requires:  python3-os-testr
Requires:  python3-subunit
Requires:  python3-tenacity
Requires:  python3-testrepository
Requires:  python3-testtools

Requires: python3-cliff
Requires:  python3-webtest

%description -n python3-%{pypi_name}-tests
%{common_desc}.

This package contains the Congress unit test files.

%if 0%{?with_doc}
# Documentation package
%package -n python3-%{pypi_name}-doc
Summary:        Documentation for OpenStack Congress service
%{?python_provide:%python_provide python3-%{pypi_name}-doc}

BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-oslo-upgradecheck
BuildRequires:  python3-mistralclient
BuildRequires:  python3-sphinxcontrib-apidoc
BuildRequires:  python3-tackerclient

%description -n python3-%{pypi_name}-doc
Documentation for OpenStack Congress service
%endif

# antlr3runtime
%package -n python3-antlr3runtime
Summary:        Antlr 3 Runtime built buy OpenStack Congress
%{?python_provide:%python_provide python3-antlr3runtime}
License: BSD

%description -n python3-antlr3runtime
Antlr 3 Runtime built buy OpenStack Congress

%prep
%autosetup -n openstack-%{pypi_name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# Remove python2 specific code when building non py2 package as this leads to failing bytecompilation
rm -rf congress/datalog/Python2 antlr3runtime/Python

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{py3_build}

# Generate sample config and add the current directory to PYTHONPATH so
# oslo-config-generator doesn't skip congress entry points.
PYTHONPATH=. oslo-config-generator --config-file=./etc/%{pypi_name}-config-generator.conf --output-file=./etc/%{pypi_name}.conf

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sphinx-build -W -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

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
#PYTHONPATH=. %{__python3} setup.py testr
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

%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/%{pypi_name}/tests

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/openstack_%{pypi_name}-*.egg-info
%exclude %{python3_sitelib}/%{pypi_name}/tests

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
%files -n python3-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python3-antlr3runtime
%license thirdparty/antlr3-antlr-3.5/LICENSE.txt
%{python3_sitelib}/antlr3runtime
%exclude %{python3_sitelib}/antlr3runtime/Python

%changelog
