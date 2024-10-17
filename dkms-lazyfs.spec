%define module lazyfs
%define vname lazyfs-linux
%define LAZYFS_VERSION 0d1d26

Summary: Dkms module for the lazyfs module
Name: dkms-lazyfs
Version: 0.1.26
Release: %mkrel 6
Source0: http://prdownloads.sourceforge.net/zero-install/%{vname}-%{version}.tgz.gpg
Source1: lazyfs-dkms.conf
License: GPL
Group: System/Kernel and hardware
URL: https://0install.net/
BuildArchitectures: noarch
Requires(post): dkms
Requires(preun): dkms
Provides: lazyfs = %{LAZYFS_VERSION}
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
BuildRequires: gnupg
%description
Lazyfs is a kernel module needed by the Zero Install system.

%prep
%setup -c -T -n %vname-%version
cd ..
gpg -o %{vname}.tar.gz %{SOURCE0} || echo Ignoring GPG error
tar --no-same-owner -xzf %{vname}.tar.gz
rm %{vname}.tar.gz
cd %vname-%version
perl -p -i -e 's/\@VERSION@/%version/; s/\@LAZYFS_VERSION@/%{LAZYFS_VERSION}/' < %{SOURCE1} > dkms.conf

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/src/%module-%version.%release/
install -m 644 dkms.conf $RPM_BUILD_ROOT/usr/src/%module-%version.%release/dkms.conf
tar c . | tar x -C $RPM_BUILD_ROOT/usr/src/%module-%version.%release/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(0755,root,root) /usr/src/%module-%version.%release/

%post
set -x
/usr/sbin/dkms --rpm_safe_upgrade add -m %module -v %version.%release
/usr/sbin/dkms --rpm_safe_upgrade build -m %module -v %version.%release
/usr/sbin/dkms --rpm_safe_upgrade install -m %module -v %version.%release

%preun
set -x
/usr/sbin/dkms --rpm_safe_upgrade remove -m %module -v %version.%release --all

