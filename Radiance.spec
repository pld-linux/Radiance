Summary:	Radiance 3D Photo-Realistic Renderer.
Summary(pl):	3D fotorealistyczny program do renderowania scen.
Name:		Radiance
%define filename rad
Version:	3r1p8
Release:	1
Group:		Applications/Graphics
Group(pl):	Aplikacje/Grafika
License:	distributable
Source0:	http://radsite.lbl.gov/radiance/pub/%{filename}%{version}.tar.Z
Patch0:		%{name}-PLD.patch
URL:		http://radsite.lbl.gov/radiance/HOME.html
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Advenced 3D Photo-Realistic Renderer.

%description -l pl
Zaawansowany program do 3D modelowania scen.

%prep
%setup  -q -n ray
%patch0 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/ray,%{_mandir}/man{1,3,5}}
(cd lib; tar cf - * )|(cd $RPM_BUILD_ROOT%{_libdir}/ray ; tar xf -)
cd src
KAT=`pwd`
for i in common meta cv gen ot rt px util cal/{ev,calc,rcalc,util};
do
 cd $i
 make \
 	"OPT=%{?debug:-O -g}%{!?debug:$RPM_OPT_FLAGS}" \
	"DESTDIR=$RPM_BUILD_ROOT" \
"MACH=-DBSD -Dlinux -DSPEED=40 -DDCL_ATOF -DBIGMEM -L%{_prefix}/X11R6/lib" \
    "ARCH=IBMPC" \
	"COMPAT=malloc.o erf.o getpagesize.o" \
    "INSTDIR=%{_bindir}" \
    "LIBDIR=%{_libdir}/ray" \
	"CC=gcc" \
    -f Rmakefile install
 cd $KAT
done
cd ..
for i in 1 3 5; do
 install doc/man/man$i/*.$i $RPM_BUILD_ROOT%{_mandir}/man$i/;
done;
install doc/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/
gzip -9nf doc/ps/* doc/notes/* doc/digest/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_libdir}/ray/
%{_mandir}/man?/*
%doc doc/ps doc/notes/* doc/digest README
