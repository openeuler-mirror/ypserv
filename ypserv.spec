Name:		ypserv
Version:	4.1
Release:        2
Summary:	The NIS server
License:	GPLv2
URL:		http://www.linux-nis.org/nis/ypserv/index.html
Source0:	https://github.com/thkukuk/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1: 	ypserv.service
Source2: 	yppasswdd.service
Source3: 	ypxfrd.service
Source4: 	rpc.yppasswdd.env
Source5: 	yppasswdd-pre-setdomain
Source6:	yppasswdd
Patch0: 	ypserv-2.5-redhat.patch
Patch1: 	ypserv-2.5-nfsnobody2.patch
Patch2: 	ypserv-2.13-ypxfr-zeroresp.patch
Patch3: 	ypserv-2.13-nonedomain.patch
Patch4: 	ypserv-2.19-slp-warning.patch
Patch5: 	ypserv-4.0-manfix.patch
Patch6: 	ypserv-2.24-aliases.patch 
Patch7: 	ypserv-2.27-confpost.patch 
Patch8: 	ypserv-2.31-netgrprecur.patch 
Patch9: 	ypserv-4.0-headers.patch 
Patch10: 	ypserv-4.0-selinux-context.patch 

BuildRequires:	gcc git systemd libxslt autoconf automake 
BuildRequires:	docbook-style-xsl tokyocabinet-devel libnsl2-devel
BuildRequires:	libtirpc-devel systemd-devel libselinux-devel
Requires: 	 tokyocabinet gawk make portmap bash >= 2.0
Requires(pre): 	hostname
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
The ypserv distributes NIS databases to client systems.The client
must run ypbind.The databases are stored in /var/yp/[domainname].
The domainname is the name of the domain being served.

%package	help
Summary: 	Doc files for ypserv
BuildArch:	noarch

%description 	help
The help package contains doc files for ypserv.

%prep
%autosetup -n %{name}-%{version} -p1 -S git
rm -f etc/netgroup.5 etc/ypserv.conf.5 makedbm/makedbm.8 mknetid/mknetid.8
autoreconf -i

%build
cp etc/README etc/README.etc
export CFLAGS="$RPM_OPT_FLAGS -fpic"

%configure --enable-checkroot --enable-fqdn --libexecdir=%{_libdir}/yp \
           --with-dbmliborder=tokyocabinet --localstatedir=%{_localstatedir} --with-selinux
%make_build

%install
%make_install
mkdir -p %{buildroot}/%{_libexecdir}
mkdir -p %{buildroot}/%{_sysconfdir}
mkdir -p %{buildroot}/%{_unitdir}
mkdir -p %{buildroot}/etc/sysconfig
install -m 644 %{SOURCE1} %{buildroot}/%{_unitdir}/ypserv.service
install -m 644 %{SOURCE2} %{buildroot}/%{_unitdir}/yppasswdd.service
install -m 644 %{SOURCE3} %{buildroot}/%{_unitdir}/ypxfrd.service
install -m 755 %{SOURCE4} %{buildroot}/%{_libexecdir}/rpc.yppasswdd.env
install -m 755 %{SOURCE5} %{buildroot}/%{_libexecdir}/yppasswdd-pre-setdomain
install -m 644 %{SOURCE6} %{buildroot}/etc/sysconfig/yppasswdd
install -m 644 etc/ypserv.conf %{buildroot}/%{_sysconfdir}

%pre

%preun
%systemd_preun ypserv.service
%systemd_preun ypxfrd.service
%systemd_preun yppasswdd.service

%post
%systemd_post ypserv.service
%systemd_post ypxfrd.service
%systemd_post yppasswdd.service

%postun
%systemd_postun_with_restart ypserv.service
%systemd_postun_with_restart ypxfrd.service
%systemd_postun_with_restart yppasswdd.service

%files
%doc COPYING AUTHORS
%doc etc/ypserv.conf etc/README.etc etc/securenets
%doc etc/netgroup etc/timezone etc/locale etc/netmasks
%config(noreplace) %{_sysconfdir}/ypserv.conf
%config(noreplace) %{_sysconfdir}/sysconfig/yppasswdd
%{_unitdir}/*.service
%{_includedir}/rpcsvc/ypxfrd.x
%{_libdir}/yp/*
%{_sbindir}/*
%{_libexecdir}/*
%config(noreplace) /var/yp/*

%files help
%doc README INSTALL TODO NEWS ChangeLog
%{_mandir}/*/*

%changelog
* Thu Nov 7 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.1-2
- Type:enhancement
- Id:NA
- SUG:NA
- DESC:modify the release

* Mon Sep 9 2019 luhuaxin <luhuaxin@huawei.com> - 4.1-1
- Package init
