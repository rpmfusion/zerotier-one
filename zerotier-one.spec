Name:           zerotier-one
Version:        1.8.3
Release:        1%{?dist}
Summary:        Smart Ethernet Switch for Earth

# Boost:        README.md
#
# ASL:          controller/
#               debian/copyright
#               include/
#               node/
#               one.cpp
#               osdep/
#               rule-compiler/
#               selftest.cpp
#               service/
#               version.h
#
# ASL 2.0:      LICENSE.txt
#
# BSD:          ext/libnatpmp/
#               ext/miniupnpc/
#
# Boost:        COPYING
#
# MIT           ext/cpp-httplib/
#               ext/http-parser/
#               ext/json/LICENSE.MIT
#               ext/librabbitmq/
#
# GPLv3+:       attic/
#               ext/libnatpmp/
#               java/

License:        BSL and Boost and ASL and ASL 2.0 and MIT
URL:            https://zerotier.com
Source0:        https://github.com/zerotier/ZeroTierOne/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  go-md2man
BuildRequires:  http-parser-devel
BuildRequires:  json-devel
BuildRequires:  libnatpmp-devel
BuildRequires:  systemd-rpm-macros

BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(miniupnpc)
BuildRequires:  pkgconfig(sqlite3)

Provides:       bundled(http-parser)
Provides:       bundled(json) = 3.10.2
Provides:       bundled(salsa2012)

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
%autosetup -n ZeroTierOne-%{version}

## Unbundling (maybe for future, depends on upstream)
# rm -rf ext/http-parser
# rm -rf ext/json


%build
%set_build_flags
%make_build \
    STRIP=%{_bindir}/true


%install
%make_install
install -Dpm0644 debian/%{name}.service %{buildroot}%{_unitdir}/%{name}.service


%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service


%files
%license COPYING
%doc AUTHORS.md README.md RELEASE-NOTES.md OFFICIAL-RELEASE-STEPS.md
%{_mandir}/man{1,8}/*.{1,8}*
%{_sbindir}/zerotier-*
%{_sharedstatedir}/%{name}/
%{_unitdir}/*.service


%changelog
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
