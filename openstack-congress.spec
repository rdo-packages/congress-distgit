%global pypi_name congress

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-%{pypi_name}
Version:        5.0.0.0b2
Release:        1%{?dist}
Summary:        OpenStack Congress Service

License:        ASL 2.0
URL:            https://launchpad.net/%{pypi_name}
Source0:        http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source1:        openstack-congress-server.service
Source2:        congress.logrotate

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-oslo-db
BuildRequires:  python-oslo-config

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

Requires: python-%{pypi_name} = %{version}-%{release}
Requires: python-%{pypi_name}-doc = %{version}-%{release}

Requires(pre): shadow-utils

%description
Support of Congress for OpenStack.

%package -n     python-%{pypi_name}
Summary:        OpenStack Congress Service
%{?python_provide:%python_provide python2-%{pypi_name}}


Requires: python-babel
Requires: python-eventlet
Requires: python-pulp
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

# Documentation package
%package -n python-%{pypi_name}-doc
Summary:        Documentation for OpenStack Congress service

BuildRequires:  python-sphinx

%description -n python-%{pypi_name}-doc
Documentation for OpenStack Congress service

# Documentation package
%package -n python-antlr3runtime
Summary:        Antlr 3 Runtime built buy OpenStack Congress

%description -n python-antlr3runtime
Antlr 3 Runtime built buy OpenStack Congress

%prep
%autosetup -n %{pypi_name}-%{upstream_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%py2_build

# Generate sample config and add the current directory to PYTHONPATH so
# oslo-config-generator doesn't skip congress entry points.
PYTHONPATH=. oslo-config-generator --config-file=./etc/congress-config-generator.conf --output-file=./etc/congress.conf

# generate html docs
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%py2_install


# Install config files
install -p -D -m 640 etc/congress.conf %{buildroot}%{_sysconfdir}/congress/congress.conf

# Install systemd script
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/openstack-congress-server.service

# Install log file
install -d -m 755 %{buildroot}%{_localstatedir}/log/congress

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-congress


%pre
# Origin: http://fedoraproject.org/wiki/Packaging:UsersAndGroups#Dynamic_allocation
USERNAME=%{congress_user}
GROUPNAME=%{congress_group}
HOMEDIR=%{_sharedstatedir}/congress
getent group $GROUPNAME >/dev/null || groupadd -r $GROUPNAME
getent passwd $USERNAME >/dev/null || \
  useradd -r -g $GROUPNAME -G $GROUPNAME -d $HOMEDIR -s /sbin/nologin \
  -c "Congress Daemons" $USERNAME
exit 0

%post
%systemd_post openstack-congress-server.service

%preun
%systemd_preun openstack-congress-server.service

%postun
%systemd_postun_with_restart openstack-congress-server.service

%files -n python-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/congress*

%files
%{_bindir}/%{pypi_name}*
#config(noreplace) %attr(0644, root, root) %{_sysconfdir}/congress/api-paste.ini
#config(noreplace) %attr(0644, root, root) %{_sysconfdir}/congress/policy.json
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/congress/congress.conf
#config(noreplace) %attr(0644, root, root) %{_sysconfdir}/congress/rootwrap.conf
#config(noreplace) %attr(0644, root, root) %{_sysconfdir}/rootwrap.d/congress.filters
%{_unitdir}/openstack-congress-server.service
%dir %attr(0755, congress, congress) %{_localstatedir}/log/congress
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-congress

%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html

%files -n python-antlr3runtime
%license LICENSE
%{python2_sitelib}/antlr3runtime*

%changelog
* Thu Jan 12 2017 Dan Radez <dradez@redhat.com> - 5.0.0.0b2-1
- Initial Packaging
