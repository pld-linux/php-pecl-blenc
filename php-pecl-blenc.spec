# TODO
# - doesn't build for php > 5.2
%define		php_name	php%{?php_suffix}
%define		modname	blenc
%define		status		alpha
Summary:	%{modname} - transparent PHP script encryption using Blowfish
Summary(pl.UTF-8):	%{modname} - transparentne szyfrowanie skryptów algorytmem Blowfish
%define	_ver	alpha
%define	_rel	1.2
Name:		%{php_name}-pecl-%{modname}
Version:	1.0
Release:	0.%{_ver}.%{_rel}
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}%{_ver}.tgz
# Source0-md5:	178ea0333257b396cc19dfea8ea0e429
URL:		http://pecl.php.net/package/blenc/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
Obsoletes:	php-pear-%{modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BLENC is an extension which hooks into the Zend Engine, allowing for
transparent encryption and execution of PHP scripts using the blowfish
algorithm. It is not designed for complete security (it is still
possible to disassemble the script into op codes using a package such
as XDebug), however it does keep people out of your code and make
reverse engineering difficult.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
BLENC jest rozszerzeniem przyczepiającym się do silnika Zend,
pozwalając na transparentne szyfrowanie i wykonywanie skryptów PHP
przy użyciu algorytmu blowfish. Nie dostarcza on kompleksowej ochrony
(ciągle możliwe jest disasemblacja skryptu do postaci instrukcji przy
użyciu narzędzi takich jak XDebug), jednakże trzyma ludzi z dala od
kodu i utrudnia jakikolwiek reverse engineering.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}%{?_ver}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
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
%doc CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
