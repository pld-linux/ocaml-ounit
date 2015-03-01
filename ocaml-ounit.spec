#
# Conditional build:
%bcond_without	ocaml_opt		# build opt

%ifarch x32
%undefine	with_ocaml_opt
%endif

Summary:	OUnit: unit tests for OCaml
Summary(pl.UTF-8):	OUnit - testy jednostkowe dla OCamla
Name:		ocaml-ounit
Version:	2.0.0
Release:	3
License:	MIT
Group:		Libraries
Source0:	http://forge.ocamlcore.org/frs/download.php/1258/ounit-%{version}.tar.gz
# Source0-md5:	2e0a24648c55005978d4923eb4925b28
URL:		http://ounit.forge.ocamlcore.org/
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-findlib
%requires_eq	ocaml
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OUnit is a unit testing framework for OCaml, inspired by the JUnit
tool for Java, and the HUnit tool for Haskell.

%description -l pl.UTF-8
OUnit to szkielet testów jednostkowych dla OCamla, zainspirowany
narzędziami JUnit dla Javy oraz HUnit dla Haskella.

%prep
%setup -q -n ounit-%{version}

%build
# not autoconf configure
./configure \
	--prefix=%{_prefix} \
	--override bytecomp_c_compiler "%{__cc} %{rpmcflags} -D_FILE_OFFSET_BITS=64 -D_REENTRANT -fPIC" \
	--override native_c_compiler "%{__cc} %{rpmcflags} -D_FILE_OFFSET_BITS=64 -D_REENTRANT"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{site-lib/oUnit,stublibs}

%{__make} install \
	OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml

mv $RPM_BUILD_ROOT%{_libdir}/ocaml/oUnit/META $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/oUnit
cat >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/oUnit/META <<EOF
directory = "+oUnit"
EOF

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/oUnit/oUnit*.mli

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.txt LICENSE.txt README.txt doc/manual.txt src/oUnit*.mli
%dir %{_libdir}/ocaml/oUnit
%if %{with ocaml_opt}
%{_libdir}/ocaml/oUnit/oUnit.a
%{_libdir}/ocaml/oUnit/oUnitAdvanced.a
%{_libdir}/ocaml/oUnit/oUnitThreads.a
%endif
%{_libdir}/ocaml/oUnit/oUnit*.cm[ixa]*
%{_libdir}/ocaml/oUnit/oUnit*.ml
%{_libdir}/ocaml/site-lib/oUnit
%{_examplesdir}/%{name}-%{version}
