Name:		connman
Summary:	Connection Manager
Group:		Networking/Other
Version:	1.0
License:	GPLv2
URL:		http://www.moblin.org
Release:	1
Source0:	http://www.kernel.org/pub/linux/network/%{name}/%{name}-%{version}.tar.gz
BuildRequires:	glib2-devel
BuildRequires:	dbus-devel
BuildRequires:	udev-devel
BuildRequires:	dhcp-client
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	ppp-devel
BuildRequires:	gtk-doc
BuildRequires:	iptables-devel
BuildRequires:	openvpn openconnect vpnc
Requires:	openvpn openconnect vpnc
Requires:	dbus
Requires:	dhcp-client >= 3.0.2
Requires:	wpa_supplicant >= 0.5.7
Requires:	bluez
Requires(pre):	rpm-helper

%description
Connection Manager provides a daemon for managing Internet connections
within embedded devices running the Linux operating system.

%package devel

Summary: Development files for Connection Manager
Group: Development/C

Requires: %{name} >= %{version}

%description devel
connman-devel contains development files for use with connman.

%prep
%setup -q -n connman-%{version}

%build
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
		--enable-polkit	\
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
%config %{_sysconfdir}/dbus-1/system.d/*.conf
%{_datadir}/dbus-1/system-services/org.moblin.connman.service
%{_datadir}/polkit-1/actions/net.%{name}.policy
%{_libdir}/%{name}/scripts/*.so*
%{_libdir}/%{name}/scripts/open*-script

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
