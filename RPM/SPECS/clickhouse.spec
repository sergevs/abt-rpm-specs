%global dbdatadir /var/lib/clickhouse

Summary:  Yandex ClickHouse DBMS
Name:     clickhouse
Version:  1.1.54304
Release:  1%{?dist}
License:  Apache License 2.0
Group:    Applications/Databases
Source:   https://github.com/yandex/ClickHouse/archive/v%{version}-stable.tar.gz
Source1:  https://raw.githubusercontent.com/sergevs/abt-rpm-specs/master/RPM/SOURCES/clickhouse-server.service
Url:      https://clickhouse.yandex
BuildRoot:%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires: make cmake python-devel mariadb-devel openssl-devel centos-release-scl devtoolset-6-gcc-c++

%description
ClickHouse is an open-source column-oriented database management system (DBMS) for online analytical processing (OLAP).

%package common
Summary: The package provides the essential shared files for %{name} server and client

%description common
ClickHouse is an open-source column-oriented database management system (DBMS) for online analytical processing (OLAP).

%package server
Summary: %{name} server and configuration files
Requires: %{name}-common = %{version}-%{release}

%description server
ClickHouse is an open-source column-oriented database management system (DBMS) for online analytical processing (OLAP).

%package client
Summary: %{name} client and configuration files
Requires: %{name}-common = %{version}-%{release}

%description client
ClickHouse is an open-source column-oriented database management system (DBMS) for online analytical processing (OLAP).

%package utils
Summary: %{name} utility tools, including compressor
Requires: %{name}-common = %{version}-%{release}

%description utils
ClickHouse is an open-source column-oriented database management system (DBMS) for online analytical processing (OLAP).

%prep
%setup -q -n ClickHouse-%{version}-stable

%build
%__mkdir_p build
pushd build
scl enable devtoolset-6 "cmake .. -DCMAKE_BUILD_TYPE:STRING=Release -DCMAKE_INSTALL_PREFIX:PATH=%_prefix"
%__make %{?_smp_mflags}

%install
%__rm -rf %{buildroot}
pushd build
%__make install DESTDIR=%{buildroot}
popd

%__rm -rf %buildroot/{%_includedir,%_datadir,/usr/lib}

for d in %_sysconfdir/clickhouse-server %_sysconfdir/clickhouse-client %_sysconfdir/cron.d %_sysconfdir/security/limits.d %_unitdir %dbdatadir
do
  %__install -d %buildroot/$d
done

%__install debian/clickhouse.limits %buildroot/%_sysconfdir/security/limits.d/clickhouse.conf
%__install %SOURCE1 %buildroot/%_unitdir

%__install -d %buildroot/%dbdatadir/{data,metadata/{system,stat,default},cores,flags}
%__install -d %buildroot/var/{log/clickhouse-server,run/clickhouse}

%__mv  %buildroot%_sysconfdir/clickhouse-client/config.xml  %buildroot%_sysconfdir/clickhouse-client/config.xml.dist
# clickhouse server does not start when ipv6 disabled
sed -i -e '/listen_host.::1/d' %buildroot%_sysconfdir/clickhouse-server/config.xml

%clean
%__rm -rf %{buildroot}

%pre common
/usr/sbin/groupadd -g 331 -o -r clickhouse >/dev/null 2>&1 || :
/usr/sbin/useradd -u 331 -M -N -g clickhouse -o -r -d %dbdatadir -s /sbin/nologin -c "ClickHouse Server" clickhouse >/dev/null 2>&1 || :

%post server
%systemd_post clickhouse-server.service

%preun server
%systemd_preun clickhouse-server.service

%postun server
%systemd_postun_with_restart clickhouse-server.service

%files common
%doc AUTHORS CHANGELOG* LICENSE README.md CONTRIBUTING.md
%_bindir/clickhouse

%files server
%defattr(755,root,root,755)
%config(noreplace) %_sysconfdir/security/limits.d/clickhouse.conf
%_bindir/clickhouse-server
%_unitdir/*
%defattr(755,clickhouse,clickhouse,755)
%dir %_sysconfdir/clickhouse-server
%config(noreplace) %_sysconfdir/clickhouse-server/*
%dir %dbdatadir
%dir /var/log/clickhouse-server
%dir /var/run/clickhouse

%files client
%defattr(755,root,root,755)
%dir %_sysconfdir/clickhouse-client
%config(noreplace) %_sysconfdir/clickhouse-client/*
%_bindir/clickhouse-client

%files utils
%defattr(755,root,root)
%_bindir/clickhouse-compressor
%_bindir/clickhouse-local
%_bindir/clickhouse-benchmark
%_bindir/clickhouse-performance-test
%_bindir/clickhouse-zookeeper-cli
%_bindir/config-processor
%_bindir/corrector_utf8

%changelog
* Wed Dec 06 2017 Serge Sergeev abrikus@gmail.com - 1.1.54304-1.el7.centos
- Initial release
