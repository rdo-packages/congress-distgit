%global pypi_name congress

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack Congress Service

License:        ASL 2.0
URL:            https://launchpad.net/%{pypi_name}
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
Source1:        openstack-congress-server.service
Source2:        congress.logrotate

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-aodhclient
BuildRequires:  python-ceilometerclient
BuildRequires:  python-cinderclient
BuildRequires:  python-django-horizon
BuildRequires:  python-django-openstack-auth
BuildRequires:  python-eventlet
BuildRequires:  python-futurist
BuildRequires:  python-glanceclient
BuildRequires:  python-heatclient
BuildRequires:  python-ironicclient
BuildRequires:  python-keystoneauth1
BuildRequires:  python-mock
BuildRequires:  python-monascaclient
BuildRequires:  python-mox3
BuildRequires:  python-muranoclient
BuildRequires:  python-neutronclient
BuildRequires:  python-novaclient
BuildRequires:  python-os-testr
BuildRequires:  python-oslo-db
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-concurrency
BuildRequires:  python-oslo-log
BuildRequires:  python-oslo-messaging
BuildRequires:  python-oslo-middleware
BuildRequires:  python-oslo-policy
BuildRequires:  python-oslo-vmware
BuildRequires:  python-PuLP
BuildRequires:  python-swiftclient
BuildRequires:  python-tenacity

Requires:  python-congressclient
Requires:  python-eventlet
Requires:  python-heatclient >= 1.6.1
Requires:  python-heat-translator
Requires:  python-neutronclient >= 5.1.0
Requires:  python-oslo-log >= 3.11.0
Requires:  python-oslo-db >= 4.15.0
Requires:  python-oslo-policy >= 1.17.0
Requires:  python-oslo-service >= 1.10.0
Requires:  python-oslo-messaging >= 5.14.0
Requires:  python-paramiko
Requires:  python-routes
Requires:  python-tosca-parser
Requires:  python-webob
Requires:  python-antlr3runtime

Requires: openstack-%{pypi_name}-common = %{version}-%{release}

Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
OpenStack Congress is Policy Management for OpenStack.

%package -n     python-%{pypi_name}
Summary:        OpenStack Congress Service
%{?python_provide:%python_provide python2-%{pypi_name}}


Requires: python-aodhclient >= 0.7.0
Requires: python-babel
Requires: python-eventlet
Requires: python-PuLP
Requires: python-keystoneauth1 >= 2.18.0
Requires: python-keystonemiddleware >= 4.12.0
Requires: python-paste
Requires: python-paste-deploy
Requires: python-pbr
Requires: python-keystoneclient >= 1:3.8.0
Requires: python-heatclient >= 1.6.1
Requires: python-muranoclient >= 0.8.2
Requires: python-novaclient >= 1:6.0.0
Requires: python-neutronclient >= 5.1.0
Requires: python-ceilometerclient >= 2.5.0
Requires: python-cinderclient >= 1.6.0
Requires: python-swiftclient >= 3.2.0
Requires: python-ironicclient >= 1.11.0
Requires: python-alembic
Requires: python-dateutil
Requires: python-glanceclient  >= 2.5.0
Requires: python-routes
Requires: python-six
Requires: python-oslo-concurrency >= 3.8.0
Requires: python-oslo-config >= 2:3.14.0
Requires: python-oslo-context >= 2.9.0
Requires: python-oslo-db >= 4.15.0
Requires: python-oslo-messaging >= 5.14.0
Requires: python-oslo-policy >= 1.17.0
Requires: python-oslo-serialization >= 1.10.0
Requires: python-oslo-service >= 1.10.0
Requires: python-oslo-utils >= 3.18.0
Requires: python-oslo-middleware >= 3.0.0
Requires: python-oslo-vmware >= 2.17.0
Requires: python-oslo-log >= 3.11.0
Requires: python-webob

%description -n python-%{pypi_name}
OpenStack Congress Service is an open policy framework for OpenStack
This package contains the Congress python library.

%package common
Summary:  %{pypi_name} common files
Requires: python-%{pypi_name} = %{version}-%{release}

%description common
OpenStack Congress Service is an open policy framework for OpenStack

This package contains the Congress common files.

%package -n python-%{pypi_name}-tests
Summary:    Congress unit and functional tests
Requires:   python-%{pypi_name} = %{version}-%{release}

Requires:  python-cliff
Requires:  python-coverage
Requires:  python-fixtures
Requires:  python-hacking
Requires:  python-mock
Requires:  python-ordereddict
Requires:  python-oslotest
Requires:  python-os-testr
Requires:  python-subunit
Requires:  python-tenacity
Requires:  python-tempest
Requires:  python-testrepository
Requires:  python-testtools
Requires:  python-webtest

%description -n python-%{pypi_name}-tests
OpenStack Congress Service is an open policy framework for OpenStack.

This package contains the Congress unit test files.

# Documentation package
%package -n python-%{pypi_name}-doc
Summary:        Documentation for OpenStack Congress service

BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme

%description -n python-%{pypi_name}-doc
Documentation for OpenStack Congress service

# antlr3runtime
%package -n python-antlr3runtime
Summary:        Antlr 3 Runtime built buy OpenStack Congress
License: BSD

%description -n python-antlr3runtime
Antlr 3 Runtime built buy OpenStack Congress

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%py2_build

# Generate sample config and add the current directory to PYTHONPATH so
# oslo-config-generator doesn't skip congress entry points.
PYTHONPATH=. oslo-config-generator --config-file=./etc/%{pypi_name}-config-generator.conf --output-file=./etc/%{pypi_name}.conf

# generate html docs
PYTHONPATH=. %{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%py2_install

# Create fake egg-info for the tempest plugin
%global service %{pypi_name}
%py2_entrypoint %{pypi_name} %{pypi_name}

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/%{pypi_name}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{pypi_name}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{pypi_name}

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/%{pypi_name}
install -p -D -m 640 etc/%{pypi_name}.conf %{buildroot}%{_sysconfdir}/%{pypi_name}/%{pypi_name}.conf
install -p -D -m 640 etc/api-paste.ini %{buildroot}%{_sysconfdir}/%{pypi_name}/api-paste.ini
install -p -D -m 640 etc/policy.json %{buildroot}%{_sysconfdir}/%{pypi_name}/policy.json
install -d -m 750 %{buildroot}%{_sysconfdir}/%{pypi_name}/keys

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-%{pypi_name}

# Install systemd units
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/openstack-%{pypi_name}-server.service

#%check
# FIXME: tests are taking too long, investigate if they are hung or simply need more time
#PYTHONPATH=. %{__python2} setup.py testr
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

%files -n python-%{pypi_name}-tests
%license LICENSE
%{python2_sitelib}/%{pypi_name}/tests
%{python2_sitelib}/%{pypi_name}_tempest_tests
%{python2_sitelib}/%{pypi_name}_tests.egg-info

%files -n python-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-*.egg-info
%exclude %{python2_sitelib}/%{pypi_name}/tests
%exclude %{python2_sitelib}/%{pypi_name}_tempest_tests

%files common
%license LICENSE
%doc README.rst
%dir %{_sysconfdir}/%{pypi_name}
%config(noreplace) %attr(0640, root, %{pypi_name}) %{_sysconfdir}/%{pypi_name}/%{pypi_name}.conf
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/%{pypi_name}/api-paste.ini
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/%{pypi_name}/policy.json
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-%{pypi_name}
%dir %attr(0750, root, %{pypi_name}) %{_sysconfdir}/%{pypi_name}/keys
%dir %attr(0750, %{pypi_name}, root) %{_localstatedir}/log/%{pypi_name}
%dir %{_sharedstatedir}/%{pypi_name}
%dir %{_datadir}/%{pypi_name}

%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html

%files -n python-antlr3runtime
%license thirdparty/antlr3-antlr-3.5/LICENSE.txt
%{python2_sitelib}/antlr3runtime
%exclude %{python2_sitelib}/antlr3runtime/Python3

%changelog
