%define		_modname	blenc
%define		_status		alpha
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

# TODO
# - doesn't build
Summary:	%{_modname} - transparent PHP script encryption using Blowfish
Summary(pl):	%{_modname} - transparentne szyfrowanie skryptów algorytmem Blowfish
Name:		php-pecl-%{_modname}
Version:	1.0
%define	_ver	alpha
Release:	0.%{_ver}.1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}%{_ver}.tgz
# Source0-md5:	178ea0333257b396cc19dfea8ea0e429
URL:		http://pecl.php.net/package/blenc/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.230
%requires_eq_to php-common php-devel
Requires:	%{_sysconfdir}/conf.d
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

%description -l pl
BLENC jest rozszerzeniem przyczepiaj±cym siê do silnika Zend,
pozwalaj±c na transparentne szyfrowanie i wykonywanie skryptów PHP
przy u¿yciu algorytmu blowfish. Nie dostarcza on kompleksowej ochrony
(ci±gle mo¿liwe jest disasemblacja skryptu do postaci instrukcji przy
u¿yciu narzêdzi takich jak XDebug), jednak¿e trzyma ludzi z dala od
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
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_modname}-%{version}%{_ver}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}%{_ver}/CREDITS
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
