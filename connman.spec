%define _disable_ld_no_undefined 1

Summary:	Connection Manager
Name:		connman
Version:	1.41
Release:	3
License:	GPLv2+
Group:		Networking/Other
Url:		http://www.moblin.org
Source0:	http://www.kernel.org/pub/linux/network/%{name}/%{name}-%{version}.tar.xz
BuildRequires:	gtk-doc
BuildRequires:	dhcp-client
BuildRequires:	pkgconfig(xtables)
BuildRequires:	ppp-devel
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(libmnl)
BuildRequires:	pkgconfig(openconnect)
BuildRequires:	openvpn
BuildRequires:	openconnect
BuildRequires:	vpnc
Requires:	openvpn
Requires:	openconnect
Requires:	vpnc
Requires:	dbus
Requires:	dhcp-client >= 3.0.2
Requires:	iwd
Requires:	bluez

%description
Connection Manager provides a daemon for managing Internet connections
within embedded devices running the Linux operating system.

%files
%doc AUTHORS COPYING INSTALL ChangeLog NEWS README
%{_bindir}/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/plugins-vpn
%dir %{_libdir}/%{name}/scripts/
%{_libdir}/%{name}/plugins/*.so
%{_libdir}/%{name}/plugins-vpn/*.so
%config %{_datadir}/dbus-1/system.d/connman*
%{_datadir}/dbus-1/system-services/net.connman.vpn.service
%{_datadir}/dbus-1/system-services/org.moblin.connman.service
%{_datadir}/polkit-1/actions/net.connman.policy
%{_datadir}/polkit-1/actions/net.connman.vpn.policy
%{_libdir}/%{name}/scripts/*.so*
%{_libdir}/%{name}/scripts/open*-script
%{_libdir}/connman/scripts/vpn-script
%{_tmpfilesdir}/connman_resolvconf.conf
%{_presetdir}/86-%{name}.preset
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-vpn.service
%{_unitdir}/%{name}-wait-online.service
%doc %{_mandir}/man1/connmanctl.1.*
%doc %{_mandir}/man5/connman.conf.5.*
%doc %{_mandir}/man5/connman-service.config.5.*
%doc %{_mandir}/man5/connman-vpn.conf.5.*
%doc %{_mandir}/man5/connman-vpn-provider.config.5.*
%doc %{_mandir}/man8/connman.8.*
%doc %{_mandir}/man8/connman-vpn.8.*

#----------------------------------------------------------------------------

%package devel
Summary:	Development files for Connection Manager
Group:		Development/C
Requires:	%{name} = %{version}

%description devel
connman-devel contains development files for use with connman.

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc

#----------------------------------------------------------------------------

%prep
%setup -q

%build
autoreconf -fi
%configure \
	--disable-static \
	--enable-ethernet \
	--enable-wifi \
	--enable-bluetooth \
	--enable-datafiles \
	--enable-loopback \
	--enable-client \
	--enable-threads \
	--enable-gtk-doc \
	--enable-hh2serial-gps \
	--enable-openvpn \
	--enable-openconnect \
	--enable-vpnc \
	--enable-l2tp \
	--enable-iospm \
	--enable-tist \
	--enable-nmcompat \
	--enable-polkit \
	--enable-iwd

%make_build

%install
%make_install

install -d %{buildroot}%{_datadir}/dbus-1/system-services/
install -m644 src/connman.service %{buildroot}%{_datadir}/dbus-1/system-services/org.moblin.connman.service

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-%{name}.preset << EOF
enable %{name}.service
EOF


%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
