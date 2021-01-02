%define __spec_install_post %{nil}
%define __os_install_post %{_dbpath}/brp-compress
%define debug_package %{nil}

Name: pisugar-server
Summary: PiSugar Power Manager
Version: @@VERSION@@
Release: @@RELEASE@@%{?dist}
License: GPLv3
Group: Applications/System
Source0: %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
%{summary}

%prep
%setup -q

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -a * %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
/etc/default/pisugar-server
/etc/pisugar-server/config.json
/lib/systemd/system/pisugar-server.service
/usr/share/pisugar-server/*

%config(noreplace)
/etc/default/pisugar-server
/etc/pisugar-server/config.json

%post
systemctl daemon-reload

%preun
systemctl stop pisugar-server || true

%postun
systemctl daemon-reload