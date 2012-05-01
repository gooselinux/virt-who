Name:           virt-who
Version:        0.3
Release:        3%{?dist}
Summary:        Agent for reporting virtual guest IDs to subscription-manager

Group:          System Environment/Base
License:        GPLv2+
URL:            https://fedorahosted.org/virt-who/
Source0:        https://fedorahosted.org/releases/v/i/virt-who/%{name}-%{version}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:      noarch
BuildRequires:  python2-devel
Requires:       libvirt-python
Requires:       libvirt
Requires:       python-rhsm >= 0.96.13
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts

# Candlepin server sometime doesn't support /status/ query. This causes virt-who
# to fail even if the rest functionality works. This patch fixes the failure.
Patch0:         virt-who-0.3-ping-exception.patch
# Use updateConsumer API instead of updateConsumerFact (fixes limit 255 chars of uuid list)
# Resolves: rhbz#743823
Patch1:         virt-who-0.3-use-update-consumer-API.patch

%description
Agent that collects information about virtual guests present in the system and
report them to the subscription manager.

%prep
%setup -q

%patch0 -p1
%patch1 -p1


%build


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

# Don't run test suite in check section, because it need the system to be
# registered to subscription-manager server

%clean
rm -rf $RPM_BUILD_ROOT

%post
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add virt-who

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service virt-who stop >/dev/null 2>&1
    /sbin/chkconfig --del virt-who
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service virt-who condrestart >/dev/null 2>&1 || :
fi


%files
%doc README LICENSE
%{_bindir}/virt-who
%{_datadir}/virt-who/
%{_sysconfdir}/rc.d/init.d/virt-who
%config(noreplace) %{_sysconfdir}/sysconfig/virt-who


%changelog
* Wed Oct 12 2011 Radek Novacek <rnovacek@redhat.com> 0.3-3
- Use updateConsumer API instead of updateConsumerFact (fixes limit 255 chars of uuid list)
- Requires python-rhsm >= 0.96.13 
- Resolves: rhbz#743823

* Wed Sep 07 2011 Radek Novacek <rnovacek@redhat.com> - 0.3-2
- Add upstream patch that prevents failure when server not implements /status/ command
- Resolves: rhbz#735793

* Thu Sep 01 2011 Radek Novacek <rnovacek@redhat.com> - 0.3-1
- Add initscript and configuration file

* Mon Aug 22 2011 Radek Novacek <rnovacek@redhat.com> - 0.2-2
- Bump release because of tagging in wrong branch

* Mon Aug 22 2011 Radek Novacek <rnovacek@redhat.com> - 0.2-1
- Update to upstream version 0.2
- Add Requires: libvirt

* Fri Aug 19 2011 Radek Novacek <rnovacek@redhat.com> - 0.1-2
- Add BuildRoot tag (the package will be in RHEL5)

* Wed Aug 10 2011 Radek Novacek <rnovacek@redhat.com> - 0.1-1
- initial import
