%global pypi_name congress

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
OpenStack Congress Service is an open policy framework for OpenStack

Name:           openstack-%{pypi_name}
Version:        7.0.2
Release:        1%{?dist}
Summary:        OpenStack Congress Service

License:        ASL 2.0
URL:            https://launchpad.net/%{pypi_name}
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{name}-%{upstream_version}.tar.gz
#

Source1:        openstack-congress-server.service
Source2:        congress.logrotate

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-aodhclient
BuildRequires:  python2-cinderclient
BuildRequires:  python-django-horizon
BuildRequires:  python2-eventlet
BuildRequires:  python2-futurist
BuildRequires:  python2-glanceclient
BuildRequires:  python2-heatclient
BuildRequires:  python2-ironicclient
BuildRequires:  python2-keystoneauth1
BuildRequires:  python2-keystonemiddleware
BuildRequires:  python2-mock
BuildRequires:  python2-monascaclient
BuildRequires:  python2-mox3
BuildRequires:  python2-muranoclient
BuildRequires:  python2-neutronclient
BuildRequires:  python2-novaclient
BuildRequires:  python2-os-testr
BuildRequires:  python2-oslo-db
BuildRequires:  python2-oslo-config
BuildRequires:  python2-oslo-concurrency
BuildRequires:  python2-oslo-log
BuildRequires:  python2-oslo-messaging
BuildRequires:  python2-oslo-middleware
BuildRequires:  python2-oslo-policy
BuildRequires:  python2-oslo-vmware
BuildRequires:  python2-PuLP
BuildRequires:  python2-swiftclient
BuildRequires:  python2-tenacity
BuildRequires:  systemd
BuildRequires:  openstack-macros

Requires:  python2-congressclient
Requires:  python2-heat-translator
Requires:  python2-paramiko
Requires:  python2-tosca-parser
Requires:  python-antlr3runtime

Requires: openstack-%{pypi_name}-common = %{version}-%{release}

Requires(pre): shadow-utils
%{?systemd_requires}

%description
OpenStack Congress is Policy Management for OpenStack.

%package -n     python-%{pypi_name}
Summary:        OpenStack Congress Service
%{?python_provide:%python_provide python2-%{pypi_name}}


Requires: python2-aodhclient >= 0.9.0
Requires: python2-babel
Requires: python2-eventlet
Requires: python-PuLP
Requires: python2-keystoneauth1 >= 3.3.0
Requires: python2-keystonemiddleware >= 4.17.0
Requires: python-paste
Requires: python-paste-deploy
Requires: python2-pbr
Requires: python2-keystoneclient >= 1:3.8.0
Requires: python2-heatclient >= 1.10.0
Requires: python2-mistralclient >= 3.1.0
Requires: python2-muranoclient >= 0.8.2
Requires: python2-novaclient >= 1:9.1.0
Requires: python2-neutronclient >= 6.3.0
Requires: python2-cinderclient >= 3.3.0
Requires: python2-swiftclient >= 3.2.0
Requires: python2-ironicclient >= 2.2.0
Requires: python2-alembic
Requires: python-dateutil
Requires: python2-glanceclient  >= 1:2.8.0
Requires: python2-routes
Requires: python2-six
Requires: python2-oslo-concurrency >= 3.25.0
Requires: python2-oslo-config >= 2:5.1.0
Requires: python2-oslo-context >= 2.19.2
Requires: python2-oslo-db >= 4.27.0
Requires: python2-oslo-messaging >= 5.29.0
Requires: python2-oslo-policy >= 1.30.0
Requires: python2-oslo-serialization >= 2.18.0
Requires: python2-oslo-service >= 1.24.0
Requires: python2-oslo-utils >= 3.33.0
Requires: python2-oslo-middleware >= 3.31.0
Requires: python2-oslo-vmware >= 2.17.0
Requires: python2-oslo-log >= 3.36.0
Requires: python-webob
Requires: python2-cryptography >= 1.7.2
Requires: python2-jsonschema >= 2.6.0
Requires: python2-monascaclient >= 1.7.0

%description -n python-%{pypi_name}
%{common_desc}
This package contains the Congress python library.

%package common
Summary:  %{pypi_name} common files
Requires: python-%{pypi_name} = %{version}-%{release}

%description common
%{common_desc}

This package contains the Congress common files.

%package -n python-%{pypi_name}-tests
Summary:    Congress unit and functional tests
Requires:   python-%{pypi_name} = %{version}-%{release}

Requires:  python-cliff
Requires:  python2-fixtures
Requires:  python2-hacking
Requires:  python2-mock
Requires:  python2-oslotest
Requires:  python2-os-testr
Requires:  python2-subunit
Requires:  python2-tenacity
Requires:  python2-testrepository
Requires:  python2-testtools
Requires:  python-webtest

%description -n python-%{pypi_name}-tests
%{common_desc}.

This package contains the Congress unit test files.

# Documentation package
%package -n python-%{pypi_name}-doc
Summary:        Documentation for OpenStack Congress service

BuildRequires:  python2-sphinx
BuildRequires:  python2-openstackdocstheme

%description -n python-%{pypi_name}-doc
Documentation for OpenStack Congress service

# antlr3runtime
%package -n python-antlr3runtime
Summary:        Antlr 3 Runtime built buy OpenStack Congress
License: BSD

%description -n python-antlr3runtime
Antlr 3 Runtime built buy OpenStack Congress

%prep
%autosetup -n openstack-%{pypi_name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

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

%files -n python-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/openstack_%{pypi_name}-*.egg-info
%exclude %{python2_sitelib}/%{pypi_name}/tests

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

%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html

%files -n python-antlr3runtime
%license thirdparty/antlr3-antlr-3.5/LICENSE.txt
%{python2_sitelib}/antlr3runtime
%exclude %{python2_sitelib}/antlr3runtime/Python3

%changelog
* Fri Apr 12 2019 RDO <dev@lists.rdoproject.org> 7.0.2-1
- Update to 7.0.2

* Mon Sep 24 2018 RDO <dev@lists.rdoproject.org> 7.0.1-1
- Update to 7.0.1

* Wed Feb 28 2018 RDO <dev@lists.rdoproject.org> 7.0.0-1
- Update to 7.0.0

* Thu Feb 22 2018 RDO <dev@lists.rdoproject.org> 7.0.0-0.2.0rc1
- Update to 7.0.0.0rc2

* Thu Feb 15 2018 RDO <dev@lists.rdoproject.org> 7.0.0-0.1.0rc1
- Update to 7.0.0.0rc1

