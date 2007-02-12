# TODO
# - doesn't build
%define		_modname	blenc
%define		_status		alpha
#
Summary:	%{_modname} - transparent PHP script encryption using Blowfish
Summary(pl.UTF-8):   %{_modname} - transparentne szyfrowanie skryptów algorytmem Blowfish
Name:		php-pecl-%{_modname}
Version:	1.0
%define	_ver	alpha
%define	_rel	1.2
Release:	0.%{_ver}.%{_rel}
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}%{_ver}.tgz
# Source0-md5:	178ea0333257b396cc19dfea8ea0e429
URL:		http://pecl.php.net/package/blenc/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BLENC is an extension which hooks into the Zend Engine, allowing for
transparent encryption and execution of PHP scripts using the blowfish
algorithm. It is not designed for complete security (it is still
possible to disassemble the script into op codes using a package such
as XDebug), however it does keep people out of your code and make
reverse engineering difficult.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
BLENC jest rozszerzeniem przyczepiającym się do silnika Zend,
pozwalając na transparentne szyfrowanie i wykonywanie skryptów PHP
przy użyciu algorytmu blowfish. Nie dostarcza on kompleksowej ochrony
(ciągle możliwe jest disasemblacja skryptu do postaci instrukcji przy
użyciu narzędzi takich jak XDebug), jednakże trzyma ludzi z dala od
kodu i utrudnia jakikolwiek reverse engineering.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c -n %{name}-%{version}%{_ver}

%build
cd %{_modname}-%{version}%{_ver}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}%{_ver}/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
