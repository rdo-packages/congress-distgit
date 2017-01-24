%global pypi_name congress

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack Congress Service

License:        ASL 2.0
URL:            https://launchpad.net/%{pypi_name}
Source0:        http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source1:        openstack-congress-server.service
Source2:        congress.logrotate

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-eventlet
BuildRequires:  python-futurist
BuildRequires:  python-oslo-db
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-concurrency
BuildRequires:  python-oslo-log
BuildRequires:  python-oslo-messaging
BuildRequires:  python-oslo-middleware
BuildRequires:  python-oslo-policy
BuildRequires:  python-tenacity

Requires:  python-eventlet
Requires:  python-heatclient
Requires:  python-heat-translator
Requires:  python-neutronclient
Requires:  python-oslo-log
Requires:  python-oslo-db
Requires:  python-oslo-policy
Requires:  python-oslo-service
Requires:  python-oslo-messaging
Requires:  python-oslo-sphinx
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


Requires: python-babel
Requires: python-eventlet
Requires: python-PuLP
Requires: python-keystoneauth1
Requires: python-keystonemiddleware
Requires: python-paste
Requires: python-paste-deploy
Requires: python-pbr
Requires: python-keystoneclient
Requires: python-heatclient
Requires: python-muranoclient
Requires: python-novaclient
Requires: python-neutronclient
Requires: python-ceilometerclient
Requires: python-cinderclient
Requires: python-swiftclient
Requires: python-ironicclient
Requires: python-alembic
Requires: python-dateutil
Requires: python-glanceclient
Requires: python-routes
Requires: python-six
Requires: python-oslo-concurrency
Requires: python-oslo-config
Requires: python-oslo-context
Requires: python-oslo-db
Requires: python-oslo-messaging
Requires: python-oslo-policy
Requires: python-oslo-serialization
Requires: python-oslo-service
Requires: python-oslo-utils
Requires: python-oslo-middleware
Requires: python-oslo-vmware
Requires: python-oslo-log
Requires: python-webob

%description -n python-%{pypi_name}
OpenStack Congress Service is an open policy framework for OpenStack
This package contains the Tacker python library.

%package common
Summary:  %{pypi_name} common files
Requires: python-%{pypi_name} = %{version}-%{release}

%description common
OpenStack Congress Service is an open policy framework for OpenStack
OpenStack Tacker Service is an NFV Orchestrator for OpenStack.

This package contains the Congress common files.

%package -n python-%{pypi_name}-tests
Summary:    Tacker unit and functional tests
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
Requires:  python-tackerclient
Requires:  python-tenacity
Requires:  python-tempest
Requires:  python-testrepository
Requires:  python-testtools
Requires:  python-webtest

%description -n python-%{pypi_name}-tests
OpenStack Tacker Service is an NFV Orchestrator for OpenStack.

This package contains the Tacker unit test files.

# Dashboard package
%package -n python-%{pypi_name}-dashboard
Summary:        Dashboard for OpenStack Congress service

%description -n python-%{pypi_name}-dashboard
Dashboard for OpenStack Congress service

# Documentation package
%package -n python-%{pypi_name}-doc
Summary:        Documentation for OpenStack Congress service

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx

%description -n python-%{pypi_name}-doc
Documentation for OpenStack Congress service

# antlr3runtime
%package -n python-antlr3runtime
Summary:        Antlr 3 Runtime built buy OpenStack Congress

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
%{__python2} setup.py build_sphinx
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
#mv %{buildroot}/usr/etc/%{pypi_name}/* %{buildroot}%{_sysconfdir}/%{pypi_name}
#mv %{buildroot}/usr/etc/rootwrap.d %{buildroot}%{_sysconfdir}
install -p -D -m 640 etc/%{pypi_name}.conf %{buildroot}%{_sysconfdir}/%{pypi_name}/%{pypi_name}.conf

# Move config to horizon
mkdir -p  %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled
mkdir -p  %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled
mkdir -p  %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.d

mv %{pypi_name}_dashboard/enabled/_50_policy.py %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/_50_policy.py
mv %{pypi_name}_dashboard/enabled/_60_policies.py %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/_60_policies.py
mv %{pypi_name}_dashboard/enabled/_70_datasources.py %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/_70_datasources.py
ln -s %{_sysconfdir}/openstack-dashboard/enabled/_50_policy.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_50_policy.py
ln -s %{_sysconfdir}/openstack-dashboard/enabled/_60_policies.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_60_policies.py
ln -s %{_sysconfdir}/openstack-dashboard/enabled/_70_datasources.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_70_datasources.py

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-%{pypi_name}

# remove /usr/etc, it's not needed
# and the init.d script is in it, which is not needed
# because a systemd script is being included
rm -rf %{buildroot}/usr/etc/

# Install systemd units
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/openstack-%{pypi_name}-server.service

%check
%{__python2} setup.py testr
%if 0%{with tests}
PYTHONPATH=/usr/share/openstack-dashboard/ ./run_tests.sh -N -P
%endif

%pre common
getent group %{pypi_name} >/dev/null || groupadd -r %{pypi_name}
getent passwd %{pypi_name} >/dev/null || \
    useradd -r -g %{pypi_name} -d %{_sharedstatedir}/%{pypi_name} -s /sbin/nologin \
    -c "OpenStack Tacker Daemons" %{pypi_name}
exit 0

%post
%systemd_post openstack-%{pypi_name}-server.service

%preun
%systemd_preun openstack-%{pypi_name}-server.service

%postun
%systemd_postun_with_restart openstack-%{pypi_name}-server.service

%files -n python-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/congress*

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
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-*.egg-info
%exclude %{python2_sitelib}/%{pypi_name}/tests
%exclude %{python2_sitelib}/%{pypi_name}_tempest_tests

%files -n python-%{pypi_name}-dashboard
%license LICENSE
%{python2_sitelib}/%{pypi_name}_dashboard
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_50_policy.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_60_policies.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_70_datasources.py*
%{_sysconfdir}/openstack-dashboard/enabled/_50_policy.py*
%{_sysconfdir}/openstack-dashboard/enabled/_60_policies.py*
%{_sysconfdir}/openstack-dashboard/enabled/_70_datasources.py*

%files common
%license LICENSE
%doc README.rst
%dir %{_sysconfdir}/%{pypi_name}
%config(noreplace) %attr(0640, root, %{pypi_name}) %{_sysconfdir}/%{pypi_name}/%{pypi_name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-%{pypi_name}
%dir %attr(0750, %{pypi_name}, root) %{_localstatedir}/log/%{pypi_name}
%dir %{_sharedstatedir}/%{pypi_name}
%dir %{_datadir}/%{pypi_name}

%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html

%files -n python-antlr3runtime
%license LICENSE
%{python2_sitelib}/antlr3runtime
%exclude %{python2_sitelib}/antlr3runtime/Python3

%changelog
* Thu Jan 12 2017 Dan Radez <dradez@redhat.com> - 5.0.0.0b2-1
- Initial Packaging
