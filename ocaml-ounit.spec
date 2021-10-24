#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	OUnit: unit tests for OCaml
Summary(pl.UTF-8):	OUnit - testy jednostkowe dla OCamla
Name:		ocaml-ounit
Version:	2.2.4
Release:	1
License:	MIT
Group:		Development/Libraries
#Source0Download: https://github.com/gildor478/ounit/releases
Source0:	https://github.com/gildor478/ounit/releases/download/v%{version}/ounit-v%{version}.tbz
# Source0-md5:	7cc70da6eb7a69bc18936ade68dfae61
Patch0:		%{name}-remove-stdlib-shims.patch
Patch1:		%{name}-remove-Thread-kill.patch
URL:		https://github.com/gildor478/ounit
BuildRequires:	ocaml >= 1:4.04.0
BuildRequires:	ocaml-dune >= 1.11.0
BuildRequires:	ocaml-findlib
BuildRequires:	ocaml-lwt-devel
%requires_eq	ocaml
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OUnit is a unit testing framework for OCaml, inspired by the JUnit
tool for Java, and the HUnit tool for Haskell.

%description -l pl.UTF-8
OUnit to szkielet testów jednostkowych dla OCamla, zainspirowany
narzędziami JUnit dla Javy oraz HUnit dla Haskella.

%package lwt
Summary:	Helper functions for building Lwt tests using OUnit
Summary(pl.UTF-8):	Funkcje pomocnicze do tworzenia testów Lwt przy użyciu biblioteki OUnit
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ocaml-lwt-devel

%description lwt
This library contains helper functions for building Lwt tests using
OUnit.

%description lwt -l pl.UTF-8
Biblioteka zawierająca funkcje pomocnicze do tworzenia testów Lwt przy
użyciu biblioteki OUnit.

%prep
%setup -q -n ounit-v%{version}
%patch0 -p1
%patch1 -p1

%build
dune build @all --verbose

%install
rm -rf $RPM_BUILD_ROOT

dune install --destdir=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -pr examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# sources
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/{ounit2,ounit2-lwt}/*.ml
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/ounit2/*/*.ml
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc/{ounit,ounit-lwt,ounit2,ounit2-lwt}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE.txt README.md
%dir %{_libdir}/ocaml/ounit
%{_libdir}/ocaml/ounit/META
%{_libdir}/ocaml/ounit/dune-package
%{_libdir}/ocaml/ounit/opam
%dir %{_libdir}/ocaml/ounit2
%{_libdir}/ocaml/ounit2/META
%{_libdir}/ocaml/ounit2/*.cma
%{_libdir}/ocaml/ounit2/*.cmi
%{_libdir}/ocaml/ounit2/*.cmt
%{_libdir}/ocaml/ounit2/*.cmti
%{_libdir}/ocaml/ounit2/*.mli
%dir %{_libdir}/ocaml/ounit2/advanced
%{_libdir}/ocaml/ounit2/advanced/*.cma
%{_libdir}/ocaml/ounit2/advanced/*.cmi
%{_libdir}/ocaml/ounit2/advanced/*.cmt
%{_libdir}/ocaml/ounit2/advanced/*.cmti
%{_libdir}/ocaml/ounit2/advanced/*.mli
%dir %{_libdir}/ocaml/ounit2/threads
%{_libdir}/ocaml/ounit2/threads/*.cma
%{_libdir}/ocaml/ounit2/threads/*.cmi
%{_libdir}/ocaml/ounit2/threads/*.cmt
%dir %{_libdir}/ocaml/ounit2/threads/.private
%{_libdir}/ocaml/ounit2/threads/.private/*.cmi
%{_libdir}/ocaml/ounit2/threads/.private/*.cmt
%if %{with ocaml_opt}
%{_libdir}/ocaml/ounit2/*.a
%{_libdir}/ocaml/ounit2/*.cmx
%{_libdir}/ocaml/ounit2/*.cmxa
%attr(755,root,root) %{_libdir}/ocaml/ounit2/*.cmxs
%{_libdir}/ocaml/ounit2/advanced/*.a
%{_libdir}/ocaml/ounit2/advanced/*.cmx
%{_libdir}/ocaml/ounit2/advanced/*.cmxa
%attr(755,root,root) %{_libdir}/ocaml/ounit2/advanced/*.cmxs
%{_libdir}/ocaml/ounit2/threads/*.a
%{_libdir}/ocaml/ounit2/threads/*.cmx
%{_libdir}/ocaml/ounit2/threads/*.cmxa
%attr(755,root,root) %{_libdir}/ocaml/ounit2/threads/*.cmxs
%endif
%{_libdir}/ocaml/ounit2/dune-package
%{_libdir}/ocaml/ounit2/opam
%{_examplesdir}/%{name}-%{version}

%files lwt
%defattr(644,root,root,755)
%dir %{_libdir}/ocaml/ounit-lwt
%{_libdir}/ocaml/ounit-lwt/META
%{_libdir}/ocaml/ounit-lwt/dune-package
%{_libdir}/ocaml/ounit-lwt/opam
%dir %{_libdir}/ocaml/ounit2-lwt
%{_libdir}/ocaml/ounit2-lwt/META
%{_libdir}/ocaml/ounit2-lwt/*.cma
%{_libdir}/ocaml/ounit2-lwt/*.cmi
%{_libdir}/ocaml/ounit2-lwt/*.cmt
%if %{with ocaml_opt}
%{_libdir}/ocaml/ounit2-lwt/*.a
%{_libdir}/ocaml/ounit2-lwt/*.cmx
%{_libdir}/ocaml/ounit2-lwt/*.cmxa
%attr(755,root,root) %{_libdir}/ocaml/ounit2-lwt/*.cmxs
%endif
%{_libdir}/ocaml/ounit2-lwt/dune-package
%{_libdir}/ocaml/ounit2-lwt/opam
