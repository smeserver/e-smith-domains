Summary: e-smith server and gateway - domains module
%define name e-smith-domains
Name: %{name}
%define version 1.3.1
%define release 02
Version: %{version}
Release: %{release}
License: GPL
Vendor: Mitel Networks Corporation
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
Patch0: e-smith-domains-1.3.1-02.mitel_patch
Packager: e-smith developers <bugs@e-smith.com>
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
BuildArchitectures: noarch
Requires: e-smith-base >= 4.13.15-76
Requires: perl(HTML::Tabulate) >= 0.23
BuildRequires: perl(Test::Inline) >= 0.12
BuildRequires: perl
BuildRequires: e-smith-devtools >= 1.11.0-03
AutoReqProv: no


%description
e-smith server and gateway software - domains module.

%changelog
* Thu Aug 25 2005 Gordon Rowell <gordonr@gormand.com.au>
- [1.3.1-02]
- Rewrite with CGI::FormMagick and HTML::Tabulate
- Added corporate DNS settings with page to change them
- Update to HTML::Tabulate 0.23 so that the remove link goes
  away when we don't want it - Thanks to Gavin Carr for the 
  immediate patch turnaround.
- Only add "Corporate DNS Servers" to picklist if configured
- Migrate all domains in domains db, defaulting system domain to
  'localhost', and others to 'internet'
- Remove table border, and change stripe colour to match other buttons
- Add calls to signal-event for create/modify/delete
- TODO: Insert name of domain to be deleted on remove page
- Signal the dns-update event when DNS configuration is changed
- Migrate the Nameserver property to the Nameservers 

* Thu Aug 25 2005 Charlie Brady <charlieb@e-smith.com>
- [1.3.1-01]
- Roll new development stream prior to adding support for delegation to
  Corporate Nameservers.

* Wed Jul 27 2005 Charlie Brady <charlieb@e-smith.com>
- [1.3.0-07]
- Remove dangling tinydns-conf symlinks.[SF: 1240099]

* Sat Mar 19 2005 Charlie Brady <charlieb@e-smith.com>
- [1.3.0-06]
- Replace obsolete conf-mod_ssl symlink with fodder for
  generic_expand_template.

* Tue Dec 28 2004 Charlie Brady <charlieb@e-smith.com>
- [1.3.0-05]
- Set non-empty path so domain panel can restart apache.
  [charlieb MN00050181]

* Tue Sep 28 2004 Michael Soulier <msoulier@e-smith.com>
- [1.3.0-04]
- Updated requires with new perl dependencies. [msoulier MN00040240]

* Tue Jul 13 2004 Michael Soulier <msoulier@e-smith.com>
- [1.3.0-03]
- Added big, red reboot warning. [msoulier MN00041156]

* Tue Jul 13 2004 Michael Soulier <msoulier@e-smith.com>
- [1.3.0-02]
- Whitespace fix.

* Wed Feb  4 2004 Michael Soulier <msoulier@e-smith.com>
- [1.3.0-01]
- rolling to dev - 1.3.0

* Wed Feb  4 2004 Michael Soulier <msoulier@e-smith.com>
- [1.2.0-01]
- rolling to stable - 1.2.0

* Mon Oct 20 2003 Michael Soulier <msoulier@e-smith.com>
- [1.1.0-03]
- Fixed the red success message. [msoulier 9265]

* Tue Sep 23 2003 Mark Knox <markk@e-smith.com>
- [1.1.0-02]
- Removed reserved 'secure.domain' name as it is no longer a special
  case [markk 8989]

* Tue Sep 23 2003 Mark Knox <markk@e-smith.com>
- [1.1.0-01]
- Rolling to development stream - 1.1.0

* Sun Sep 14 2003 Charlie Brady <charlieb@e-smith.com>
- [1.0.0-08]
- Remove xinetd-reload from domain-{create,delete,modify} events.
  [charlieb 9804]

* Mon Aug 25 2003 Charlie Brady <charlieb@e-smith.com>
- [1.0.0-07]
- Reconfig tinydns when adding/removing a domain. [charlieb 9642]

* Tue Jun 24 2003 Gordon Rowell <gordonr@e-smith.com>
- [1.0.0-06]
- Spanish nav bar [gordonr 9153]

* Tue Jun 17 2003 Gordon Rowell <gordonr@e-smith.com>
- [1.0.0-05]
- c&p error in change 1.0.0-02 [gordonr 8954]

* Thu Jun 12 2003 Gordon Rowell <gordonr@e-smith.com>
- [1.0.0-04]
- Added order tags to migrate fragments [gordonr 9015]

* Tue Jun 10 2003 Charlie Brady <charlieb@e-smith.com>
- [1.0.0-03]
- Fix wrong DB name in warning message.  [charlieb 8954]

* Tue Jun 10 2003 Charlie Brady <charlieb@e-smith.com>
- [1.0.0-02]
- Force domain names to lower case - DNS is case insensitive. [charlieb 8954]

* Thu May  8 2003 Mark Knox <markk@e-smith.com>
- [1.0.0-01]
- Initial release. This module used to be part of e-smith-base. [markk 8610]

%prep
%setup
%patch0 -p1

%pre
%post

%build
# Force creation of potentially empty directories
mkdir -p root/etc/e-smith/web/{common,functions}
mkdir -p root/etc/e-smith/web/panels/manager/{cgi-bin,common,html}

LEXICONS=$(find root/etc/e-smith/web/{functions,panels/password/cgi-bin} \
	-type f | grep -v CVS | grep -v pleasewait)

for lexicon in $LEXICONS
do
    /sbin/e-smith/validate-lexicon $lexicon
done

/sbin/e-smith/generate-lexicons

perl createlinks

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
/sbin/e-smith/genfilelist $RPM_BUILD_ROOT \
    > %{name}-%{version}-%{release}-filelist
echo "%doc COPYING"          >> %{name}-%{version}-%{release}-filelist

%clean 
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
