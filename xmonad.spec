Summary:	Tiling window manager
Name:		xmonad
Version:	0.11.1
Release:	1
License:	BSD
Group:		X11/Window Managers
Source0:	http://hackage.haskell.org/package/%{name}-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	20792f4e428db24e6c0dbecbd77f69e0
Source1:	%{name}.desktop
Patch0:		%{name}-border.patch
URL:		http://www.xmonad.org
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-X11 >= 1.6
BuildRequires:	ghc-extensible-exceptions
BuildRequires:	ghc-mtl
BuildRequires:	ghc-utf8-string
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
%requires_releq	ghc-extensible-exceptions
%requires_releq	ghc-mtl
%requires_releq	ghc-utf8-string
%requires_releq	ghc-X11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0
%define		_xdeskdir	%{_datadir}/xsessions

%description
xmonad is a tiling window manager for X. Windows are arranged
automatically to tile the screen without gaps or overlap, maximising
screen use. All features of the window manager are accessible from the
keyboard: a mouse is strictly optional. xmonad is written and
extensible in Haskell. Custom layout algorithms, and other extensions,
may be written by the user in config files. Layouts are applied
dynamically, and different layouts may be used on each workspace.
Xinerama is fully supported, allowing windows to be tiled on several
screens.

%package doc
Summary:	HTML documentation for %{name}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{name}
Group:		Documentation

%description doc
HTML documentation for %{name}.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{name}.

%prep
%setup -q
%patch0 -p1

%build
runhaskell Setup.lhs configure -v2 \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_deskdir},%{_xdeskdir}}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_xdeskdir}/%{name}.desktop

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/man
%{__rmdir} $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp -p man/xmonad.1 $RPM_BUILD_ROOT%{_mandir}/man1

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc man/xmonad.hs
%attr(755,root,root) %{_bindir}/xmonad
%{_libdir}/%{ghcdir}/package.conf.d/%{name}.conf
%{_libdir}/%{ghcdir}/%{name}-%{version}
%{_mandir}/man1/xmonad.1*
%{_xdeskdir}/%{name}.desktop

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
