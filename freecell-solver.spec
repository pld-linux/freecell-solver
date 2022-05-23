Summary:	Library for solving several variants of card Solitaire / Patience games
Name:		freecell-solver
Version:	6.6.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://fc-solve.shlomifish.org/downloads/fc-solve/%{name}-%{version}.tar.xz
# Source0-md5:	4bae74866d1279f6c09d68fa55c9405e
URL:		https://fc-solve.shlomifish.org/
BuildRequires:	cmake >= 3.5
BuildRequires:	gperf
BuildRequires:	perl-Moo
BuildRequires:	perl-Path-Tiny
BuildRequires:	perl-Template-Toolkit
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	python3
BuildRequires:	python3-pysol_cards
BuildRequires:	python3-random2
BuildRequires:	python3-six
BuildRequires:	rinutils-devel
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Library that automatically solves layouts of Freecell and similar
variants of Card Solitaire such as Eight Off, Forecell, and Seahaven
Towers, as well as Simple Simon boards.

%package devel
Summary:	Header files for freecell-solver library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for freecell-solver library.

%package static
Summary:	Static freecell-solver library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static freecell-solver library.

%prep
%setup -q

grep -r -l 'env python' board_gen | xargs %{__sed} -i -e '1s,#!.*env python.*,#!%{__python3},'

%build
%cmake -B build \
	-DFCS_WITH_TEST_SUITE:BOOL=OFF

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

for b in $RPM_BUILD_ROOT%{_bindir}/*.py; do
	%{__mv} $b ${b%.py}
done

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc {AUTHORS,HACKING,NEWS,README,TODO,USAGE}.asciidoc
%attr(755,root,root) %{_bindir}/dbm-fc-solver
%attr(755,root,root) %{_bindir}/depth-dbm-fc-solver
%attr(755,root,root) %{_bindir}/fc-solve
%attr(755,root,root) %{_bindir}/fc_solve_find_index_s2ints
%attr(755,root,root) %{_bindir}/find-freecell-deal-index
%attr(755,root,root) %{_bindir}/freecell-solver-fc-pro-range-solve
%attr(755,root,root) %{_bindir}/freecell-solver-multi-thread-solve
%attr(755,root,root) %{_bindir}/freecell-solver-range-parallel-solve
%attr(755,root,root) %{_bindir}/gen-multiple-pysol-layouts
%attr(755,root,root) %{_bindir}/make_pysol_freecell_board
%attr(755,root,root) %{_bindir}/pi-make-microsoft-freecell-board
%attr(755,root,root) %{_bindir}/transpose-freecell-board
%attr(755,root,root) %{_libdir}/libfreecell-solver.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreecell-solver.so.0
%{_datadir}/freecell-solver
%{_mandir}/man6/dbm-fc-solver.6*
%{_mandir}/man6/fc-solve-board_gen.6*
%{_mandir}/man6/fc-solve.6*
%{_mandir}/man6/freecell-solver-range-parallel-solve.6*
%{_mandir}/man6/gen-multiple-pysol-layouts.6*
%{_mandir}/man6/make_pysol_freecell_board.py.6*
%{_mandir}/man6/pi-make-microsoft-freecell-board.6*
%{_mandir}/man6/transpose-freecell-board.py.6*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfreecell-solver.so
%{_includedir}/freecell-solver
%{_pkgconfigdir}/libfreecell-solver.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libfreecell-solver.a
