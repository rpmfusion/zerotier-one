%global toolchain clang
# /usr/bin/debugedit: Cannot handle 8-byte build ID
%ifarch %{arm}
%global debug_package %{nil}
%endif

Name:           zerotier-one
Version:        1.4.0
Release:        1%{?dist}
Summary:        Smart Ethernet Switch for Earth

#
# GPLv3+:       attic/   
#               controller/
#               debian/copyright
#               include/
#               java/  
#               node/
#               one.cpp
#               osdep/
#               rule-compiler/
#               selftest.cpp
#               service/
#               version.h
#               COPYING
#               LICENSE.txt
#               README.md
#
# BSD:          ext/libnatpmp/
#               ext/miniupnpc/
#
#
# MIT           ext/cpp-httplib/
#               ext/http-parser/
#               ext/json/LICENSE.MIT
#               ext/librabbitmq/
#

License:        BSD and GPLv3+ and MIT
URL:            https://zerotier.com
Source0:        https://github.com/zerotier/ZeroTierOne/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        zerotier-one-sysusers

BuildRequires:  clang
BuildRequires:  libnatpmp-devel
BuildRequires:  miniupnpc-devel
BuildRequires:  systemd-rpm-macros

Provides:       bundled(http-parser)
Provides:       bundled(json) = 3.10.2
Provides:       bundled(salsa2012)

Requires:       iproute
Requires:       /sbin/nologin
%{?systemd_requires}
%{?sysusers_requires_compat}

%description
ZeroTier is a smart programmable Ethernet switch for planet Earth. It allows all
networked devices, VMs, containers, and applications to communicate as if they
all reside in the same physical data center or cloud region.

This is accomplished by combining a cryptographically addressed and secure peer
to peer network (termed VL1) with an Ethernet emulation layer somewhat similar
to VXLAN (termed VL2). Our VL2 Ethernet virtualization layer includes advanced
enterprise SDN features like fine grained access control rules for network
micro-segmentation and security monitoring.

All ZeroTier traffic is encrypted end-to-end using secret keys that only you
control. Most traffic flows peer to peer, though we offer free (but slow)
relaying for users who cannot establish peer to peer connections.

The goals and design principles of ZeroTier are inspired by among other things
the original Google BeyondCorp paper and the Jericho Forum with its notion of
"deperimeterization."


%prep
%autosetup -p 1 -n ZeroTierOne-%{version}

## Unbundling (maybe for future, depends on upstream)
# rm -rf ext/http-parser
# rm -rf ext/json

%build
%make_build STRIP=%{_bindir}/true

%install
%make_install
install -D -m0644 debian/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -D -m0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf

%pre
%sysusers_create_compat %{SOURCE1}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service


%files
%license COPYING LICENSE.GPL-2 LICENSE.GPL-3 LICENSE.txt
%doc AUTHORS.md README.md RELEASE-NOTES.md OFFICIAL-RELEASE-STEPS.md
%{_mandir}/man{1,8}/*.{1,8}*
%{_sbindir}/zerotier-*
%{_sharedstatedir}/%{name}/
%{_sysusersdir}/%{name}.conf
%{_unitdir}/*.service


%changelog
* Fri Apr 19 2024 Leigh Scott <leigh123linux@gmail.com> - 1.4.0-1
- Update to 1.4.0

* Sun Apr 07 2024 Leigh Scott <leigh123linux@gmail.com> - 1.12.2-3
- Rebuild against standard openssl

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Oct 22 2023 Leigh Scott <leigh123linux@gmail.com> - 1.12.2-1
- rebuilt

* Thu Aug 24 2023 Leigh Scott <leigh123linux@gmail.com> - 1.12.0-1
- chore(update): 1.12.0

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.10.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jun 24 2023 Leigh Scott <leigh123linux@gmail.com> - 1.10.6-2
- Fix rfbz#6714

* Sun May 21 2023 Leigh Scott <leigh123linux@gmail.com> - 1.10.6-1
- chore(update): 1.10.6

* Fri Feb 17 2023 Leigh Scott <leigh123linux@gmail.com> - 1.10.3-1
- chore(update): 1.10.3

* Wed Nov 02 2022 Leigh Scott <leigh123linux@gmail.com> - 1.10.2-1
- chore(update): 1.10.2
- Switch to clang to match upstream spec file.
- Bundle everything to match upstream spec file.

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.8.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Jun 22 2022 Leigh Scott <leigh123linux@gmail.com> - 1.8.9-2
- The official package is built against openssl1.1

* Mon Jun 13 2022 Leigh Scott <leigh123linux@gmail.com> - 1.8.9-1
- chore(update): 1.8.9

* Fri Mar 04 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.8.5-1
- chore(update): 1.8.5

* Thu Feb 10 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 03 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.8.4-1
- chore(update): 1.8.4

* Fri Nov 19 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.8.3-1
- chore(update): 1.8.3

* Thu Nov 11 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.8.2-1
- chore(update): 1.8.2

* Fri Oct 29 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.8.1-1
- chore(update): 1.8.1

* Thu Sep 23 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.6.6-1
- build(update): 1.6.6

* Wed Aug 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Apr 30 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.6.5-1
- build(update): 1.6.5

* Wed Feb 17 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.6.4-1
- build(update): 1.6.4

* Thu Feb 04 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.6.3-1
- build(update): 1.6.3

* Fri Jan 15 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.6.2-2
- build: build debuginfo package

* Tue Dec  1 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 1.6.2-1
- build(update): 1.6.2

* Thu Nov 26 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 1.6.1-1
- build(update): 1.6.1

* Sat Nov 21 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 1.6.0-1
- build(update): 1.6.0

* Sun Nov 03 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 1.4.6-4
- Update to 1.4.6

* Thu Apr 25 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 1.2.12-2
- Update to 1.2.12
- .spec file "fixes" :)

* Sat Mar 18 2017 François Kooman <fkooman@tuxed.net> - 1.2.2-1
- update to 1.2.2

* Mon Jul 25 2016 François Kooman <fkooman@tuxed.net> - 1.1.14-1
- update to 1.1.14

* Tue Jul 19 2016 François Kooman <fkooman@tuxed.net> - 1.1.12-2
- allow override of LDFLAGS by rpmbuild

* Wed Jul 13 2016 François Kooman <fkooman@tuxed.net> - 1.1.12-1
- update to 1.1.12
- remove fix for selftest when controller is enabled

* Mon Jul 04 2016 François Kooman <fkooman@tuxed.net> - 1.1.6-2
- use go-md2man to generate the manpages

* Mon Jul 04 2016 François Kooman <fkooman@tuxed.net> - 1.1.6-1
- initial package
