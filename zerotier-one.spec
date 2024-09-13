%global toolchain clang
# /usr/bin/debugedit: Cannot handle 8-byte build ID
%ifarch %{arm}
%global debug_package %{nil}
%endif

Name:           zerotier-one
Version:        1.14.1
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
# make with command: 'cd rustybits and  mkdir .cargo 
# cargo vendor > .cargo/config.toml' and tar cvf vendor-%%{version}.tar.xz vendor/ .cargo/
Source1:        vendor-%{version}.tar.xz
Source2:        zerotier-one-sysusers

BuildRequires:  cargo
BuildRequires:  clang
BuildRequires:  openssl-devel openssl
BuildRequires:  systemd-rpm-macros

Provides:       bundled(http-parser)
Provides:       bundled(json) = 3.10.2
Provides:       bundled(salsa2012)

Requires:       openssl
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
%autosetup -p1 -n ZeroTierOne-%{version}

pushd rustybits
tar -xf %{SOURCE1}
sed -i -e '1d' vendor/ipnet/src/lib.rs
sed -i -e 's@54cb3178bd183149cd9db26f0134fa9d31b305d8a29ab75c320408d5fb0b3ed0@9f114797d36b74da607ba52fe38f050593b0b8e046ea7cbe9075d87f8007aed4@g' \
 vendor/ipnet/.cargo-checksum.json
popd

%build
%make_build \
 ZT_USE_MINIUPNPC=1 \
 STRIP=%{_bindir}/true \
 one


%install
%make_install
install -D -m0644 debian/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -D -m0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf

%pre
%sysusers_create_compat %{SOURCE2}

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
%{_sysusersdir}/%{name}.conf
%{_unitdir}/*.service


%changelog
* Fri Sep 13 2024 Leigh Scott <leigh123linux@gmail.com> - 1.14.1-1
- Update to 1.14.1

* Sat Aug 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu May 09 2024 Leigh Scott <leigh123linux@gmail.com> - 1.14.0-1
- Update to 1.14.0

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
