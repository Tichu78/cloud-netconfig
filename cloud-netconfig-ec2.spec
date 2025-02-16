#
# spec file for package cloud-netconfig
#
# Copyright (c) 2017 SUSE Linux GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

%define base_name cloud-netconfig

Name:           %{base_name}-ec2
Version:        1.0
Release:        0
License:        GPL-3.0+
Summary:        Network configuration scripts for Amazon EC2
Url:            https://github.com/SUSE/Enceladus
Group:          System/Management
Source0:        %{base_name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
%if 0%{?suse_version} == 1110
BuildRequires:  sysconfig
Requires:       sysconfig
%define _udevrulesdir %{_sysconfdir}/udev/rules.d
%else
BuildRequires:  sysconfig-netconfig
Requires:       sysconfig-netconfig
%endif
BuildRequires:  udev
Requires:       udev
Requires:       curl
Provides:       cloud-netconfig
Conflicts:      cloud-netconfig
%{?systemd_requires}

%description
This package contains scripts for automatically configuring network interfaces
in Amazon EC2 with full support for hotplug.

%prep
%setup -q -n %{base_name}-%{version}

%build

%install
make install-ec2 \
  DESTDIR=%{buildroot} \
  PREFIX=%{_usr} \
  SYSCONFDIR=%{_sysconfdir} \
  UDEVRULESDIR=%{_udevrulesdir} \
  UNITDIR=%{_unitdir}

# Disable persistent net generator from udev-persistent-ifnames as
# it does not work for xen interfaces. This will likely produce a warning.
%if 0%{?suse_version} >= 1315
mkdir -p %{buildroot}/%{_sysconfdir}/udev/rules.d
ln -s /dev/null %{buildroot}/%{_sysconfdir}/udev/rules.d/75-persistent-net-generator.rules
%endif

%files
%defattr(-,root,root)
%{_sysconfdir}/netconfig.d/cloud-netconfig
%{_sysconfdir}/sysconfig/network/scripts/*
%if 0%{?suse_version} >= 1315
%{_sysconfdir}/udev/rules.d
%endif
%{_udevrulesdir}/51-cloud-netconfig-hotplug.rules
%{_udevrulesdir}/75-cloud-persistent-net-generator.rules
%doc README.md
%license LICENSE

%pre
%service_add_pre %{base_name}.service %{base_name}.timer

%post
%service_add_post %{base_name}.service %{base_name}.timer

%preun
%service_del_preun %{base_name}.service %{base_name}.timer

%postun
%service_del_postun %{base_name}.service %{base_name}.timer

%changelog
