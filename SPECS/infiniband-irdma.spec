%define vendor_name Intel
%define vendor_label intel
%define driver_name irdma
%define module_dir extra

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{driver_name}-module
Version: 1.12.55
Release: 1%{?dist}
License: GPLv2

# Source extracted from intel.com
# URL: https://downloadmirror.intel.com/786088/irdma-1.12.55.tgz
Source0: irdma-%{version}.tgz
Source1: modprobe-irdma.conf

BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n irdma-%{version}

%build
%{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src/irdma KSRC=/lib/modules/%{kernel_version}/build CFLAGS_MODULE="-DMODULE -DSLE_LOCALVERSION_CODE=0 -DOFED_VERSION_CODE=" W=1 C=0 CF= modules

%install
%{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src/irdma INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install
install -D -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/modprobe.d/irdma.conf

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+wx

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko
%{_sysconfdir}/modprobe.d/irdma.conf

%changelog
* Thu Dec 14 2023 Thierry Escande <thierry.escande@vates.tech> - 1.12.55-1
- Initial package: version 1.12.55
- Synced from intel.com
