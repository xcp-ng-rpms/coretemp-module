%define uname  %{kernel_version}
%define module_dir override

Summary: Driver for coretemp
Name: coretemp-module
Version: 1.0
Release: %{?release}%{!?release:1}
License: GPL
Source: %{name}-%{version}.tar.gz

Patch0: coretemp-1.0-disable-cpuid-check.patch

BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
coretemp Linux Device Driver source.

%prep
%autosetup -p1

%build
%{__make} -C /lib/modules/%{uname}/build M=$(pwd) modules

%install
%{__make} -C /lib/modules/%{uname}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# remove extra files modules_install copies in
rm -f %{buildroot}/lib/modules/%{uname}/modules.*

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{uname} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
%defattr(-,root,root,-)
/lib/modules/%{uname}/*/*.ko
%doc

%changelog
* Wed Dec 4 2019 Rushikesh Jadhav <rushikesh7@gmail.com> - 1.0
- Added driver coretemp-module-1.0
- Removed cpuid checking from driver
