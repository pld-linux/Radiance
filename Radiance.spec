Summary:	Radiance 3D Photo-Realistic Renderer
Summary(pl):	Fotorealistyczny program do renderowania scen 3D
Name:		Radiance
Version:	3R4
Release:	1
Epoch:		1
License:	free use, but non-distributable
Group:		Applications/Graphics
Source0:	http://radsite.lbl.gov/radiance/pub/rad%{version}.tar.gz
Source1:	http://radsite.lbl.gov/radiance/pub/patch%{version}p1.tar.gz
Patch0:		%{name}-PLD.patch
Patch1:		%{name}-rview-conflict.patch
Patch2:		%{name}-shared-libtiff.patch
NoSource:	0
NoSource:	1
URL:		http://radsite.lbl.gov/radiance/HOME.html
BuildRequires:	libtiff-devel
BuildRequires:	tk
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Advenced 3D Photo-Realistic Renderer.

%description -l pl
Zaawansowany program do modelowania scen 3D.

%prep
%setup  -q -n ray
tar xvfz %{SOURCE1}
%patch0 -p1
%patch1 -p1
%patch2 -p1

mv -f doc/man/man1/{rview.1,radview.1}
install -d src/lib

%build
for i in common meta cv gen ot rt px hd util cal/{ev,calc,rcalc,util}; do
    %{__make} -C src/$i -f Rmakefile \
	OPT="%{rpmcflags} -DSPEED=200" CC="%{__cc}" \
	ARCH="IBMPC" \
	MACH="-DBSD -Dlinux -Dtracktime=0 -DDCL_ATOF -DBIGMEM -DNOSTEREO -L/usr/X11R6/lib -I/usr/include/X11" \
	MLIBDIR="%{_libdir}/ray/meta" \
	COMPAT="bmalloc.o erf.o getpagesize.o"
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/ray,%{_mandir}/man{1,3,5}}

tar cf - -C lib * | tar xf - -C $RPM_BUILD_ROOT%{_libdir}/ray

for i in meta cv gen ot rt px hd util cal/{ev,calc,rcalc,util}; do
    %{__make} -C src/$i -f Rmakefile install \
	"DESTDIR=$RPM_BUILD_ROOT" \
	"INSTDIR=%{_bindir}" \
	"LIBDIR=%{_libdir}/ray"
done

# remove links to libtiff manuals
cd doc/man/man1
for i in fax2ps.1 fax2tiff.1 gif2tiff.1 pal2rgb.1 ppm2tiff.1 ras2tiff.1 \
	rgb2ycbcr.1 sgi2tiff.1 thumbnail.1 tiff*.1 ; do
	rm -f $i
done
cd ..
rm -f man3/TIFF* man3/libtiff*

for i in 1 3 5; do
	install man$i/*.$i $RPM_BUILD_ROOT%{_mandir}/man$i
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_libdir}/ray
%{_mandir}/man?/*
%doc doc/ps doc/notes/* doc/*.1* README*
