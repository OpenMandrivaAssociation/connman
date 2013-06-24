Summary:	Connection Manager
Name:		connman
Version:	1.15
Release:	1
License:	GPLv2
Group:		Networking/Other
Url:		http://www.moblin.org
Source0:	http://www.kernel.org/pub/linux/network/%{name}/%{name}-%{version}.tar.xz
BuildRequires:	gtk-doc
BuildRequires:	dhcp-client
BuildRequires:	iptables-devel
BuildRequires:	ppp-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	openvpn openconnect vpnc
Requires:	openvpn openconnect vpnc
Requires:	dbus
Requires:	dhcp-client >= 3.0.2
Requires:	wpa_supplicant >= 0.5.7
Requires:	bluez

%description
Connection Manager provides a daemon for managing Internet connections
within embedded devices running the Linux operating system.

%package devel
Summary:	Development files for Connection Manager
Group:		Development/C
Requires:	%{name} = %{version}

%description devel
connman-devel contains development files for use with connman.

%prep
%setup -q

%build
%setup_compile_flags
autoreconf -fi
./configure	--disable-static \
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
		--prefix=%{_prefix} \
		--libdir=%{_libdir}
%make

%install
%makeinstall_std

install -d %{buildroot}%{_datadir}/dbus-1/system-services/
install -m644 src/connman.service %{buildroot}%{_datadir}/dbus-1/system-services/org.moblin.connman.service

%files
%doc AUTHORS COPYING INSTALL ChangeLog NEWS README
%{_sbindir}/*
%dir %{_libdir}/%{name}/scripts/
%{_libdir}/%{name}/plugins/*.so
%{_libdir}/%{name}/plugins-vpn/*.so
%config %{_sysconfdir}/dbus-1/system.d/*.conf
%{_datadir}/dbus-1/system-services/net.connman.vpn.service
%{_datadir}/dbus-1/system-services/org.moblin.connman.service
%{_datadir}/polkit-1/actions/net.connman.policy
%{_datadir}/polkit-1/actions/net.connman.vpn.policy
%{_libdir}/%{name}/scripts/*.so*
%{_libdir}/%{name}/scripts/open*-script
%{_mandir}/man5/connman.conf.5.*
%{_mandir}/man8/connman.8.*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
