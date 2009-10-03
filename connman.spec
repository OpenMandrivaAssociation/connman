%define ver 0.42

Name: connman
Summary: Connection Manager
Group: Applications/System
Version: %{ver}
License: GPLv2
URL: http://www.moblin.org
Release: %mkrel 1
Source0: http://www.kernel.org/pub/linux/network/%{name}/%{name}-%{ver}.tar.gz
Source1: mandriva-connman-init
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: glib2-devel
BuildRequires: dbus-devel
BuildRequires: udev-devel
BuildRequires: dhcp-client
BuildRequires: ppp-devel
BuildRequires: gtk-doc

Requires: dbus
Requires: dhcp-client >= 3.0.2
Requires: wpa_supplicant >= 0.5.7
Requires: bluez

Requires(pre): rpm-helper

%description
Connection Manager provides a daemon for managing Internet connections
within embedded devices running the Linux operating system.

%package devel

Summary: Development files for Connection Manager
Group: Development/Libraries

Requires: %{name} >= %{version}

%description devel
connman-devel contains development files for use with connman.

%prep
%setup -q -n connman-%{version}

%build
autoreconf -fi
%configure	--disable-static \
		--enable-ethernet \
		--enable-wifi \
		--enable-dhclient \
		--enable-bluetooth \
		--enable-loopback \
		--enable-dnsproxy \
		--enable-ppp \
		--enable-udev \
		--enable-modemmgr \
		--enable-client \
		--enable-threads \
		--enable-gtk-doc

%make

%install
rm -rf %{buildroot}
%makeinstall_std
mkdir -p %{buildroot}/%{_initrddir}
cp -f %{SOURCE1} %{buildroot}/%{_initrddir}/%{name}
chmod +x %{buildroot}/%{_initrddir}/%{name}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL ChangeLog NEWS README
%{_sbindir}/*
%{_libdir}/%{name}/scripts/*
%{_libdir}/%{name}/plugins/*.so
%{_initrddir}/%{name}
%config %{_sysconfdir}/dbus-1/system.d/*.conf

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/%{name}/plugins/*.la
