Summary:	Radiance 3D Photo-Realistic Renderer
Summary(pl):	Fotorealistyczny program do renderowania scen 3D.
Name:		Radiance
Version:	3r1p8
Release:	1
License:	free use, but non-distributable
Group:		Applications/Graphics
Group(de):	Applikationen/Grafik
Group(pl):	Aplikacje/Grafika
Source0:	http://radsite.lbl.gov/radiance/pub/rad%{version}.tar.Z
Patch0:		%{name}-PLD.patch
Patch1:		%{name}-rview-conflict.patch
NoSource:	0
URL:		http://radsite.lbl.gov/radiance/HOME.html
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Advenced 3D Photo-Realistic Renderer.

%description -l pl
Zaawansowany program do modelowania scen 3D.

%prep
%setup  -q -n ray
%patch0 -p1
%patch1 -p1

(cd doc/man/man1 ; mv -f rview.1 radview.1)

%build
for i in common meta cv gen ot rt px util cal/{ev,calc,rcalc,util}; do
    make -C src/$i -f Rmakefile \
	OPT="%{rpmcflags}" CC="%{__cc}" \
	ARCH="IBMPC" \
	MACH="-DBSD -Dlinux -DSPEED=40 -DDCL_ATOF -DBIGMEM -L/usr/X11R6/lib" \
	MLIBDIR="%{_libdir}/ray/meta" \
	COMPAT="malloc.o erf.o getpagesize.o"
done
	
%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/ray,%{_mandir}/man{1,3,5}}

(cd lib
tar cf - * | tar xf - -C $RPM_BUILD_ROOT%{_libdir}/ray
)

for i in meta cv gen ot rt px util cal/{ev,calc,rcalc,util}; do
    make -C src/$i -f Rmakefile install \
	"DESTDIR=$RPM_BUILD_ROOT" \
	"INSTDIR=%{_bindir}" \
	"LIBDIR=%{_libdir}/ray"
done

for i in 1 3 5; do
	install doc/man/man$i/*.$i $RPM_BUILD_ROOT%{_mandir}/man$i
done

# note: doc/*.1 are ordinary groff files, not manuals
gzip -9nf doc/ps/* doc/notes/* doc/digest/* README doc/*.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_libdir}/ray
%{_mandir}/man?/*
%doc doc/ps doc/notes/* doc/digest doc/*.1.gz README.gz
