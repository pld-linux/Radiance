Summary:	Radiance 3D Photo-Realistic Renderer
Summary(pl):	Fotorealistyczny program do renderowania scen 3D
Name:		Radiance
Version:	3R5
Release:	3
Epoch:		1
License:	BSD-like (see included license.txt)
Group:		Applications/Graphics
Source0:	http://radsite.lbl.gov/radiance/dist/rad%{version}.tar.gz
# Source0-md5:	7b4eea2658704b08cbb775c071985bf0
Source1:	http://radsite.lbl.gov/radiance/misc/license.txt
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

mv -f doc/man/man1/{rview.1,radview.1}

# patches from gentoo
# patch to not build libtiff that comes with Radiance
mv src/px/Rmakefile src/px/Rmakefile.orig
sed -e "s/\.\.\/lib\/libtiff\.a$//g" \
	src/px/Rmakefile.orig > src/px/Rmakefile

	# fix syntax error in standard.h
mv src/common/standard.h src/common/standard.h.orig
sed -e "s/error(et,em) else$/error(et,em); else/g" \
	src/common/standard.h.orig > src/common/standard.h

# fix incorrect use of errno.h
mv src/cal/ev.c src/cal/ev.c.orig
sed -e "s/extern int  errno;/#include <errno.h>/g" \
	src/cal/ev.c.orig > src/cal/ev.c

install -d src/lib bin/{bin/dev,lib}

%build
wd=`pwd`
for i in common meta cv gen ot rt px hd util cal; do
    %{__make} -C src/$i -f Rmakefile  install \
	OPT="%{rpmcflags} -DSPEED=200" CC="%{__cc}" \
	ARCH="IBMPC" \
	MACH="-DBSD -Dlinux -Dtracktime=0 -DDCL_ATOF -DBIGMEM -DNOSTEREO -L/usr/X11R6/%{_lib} -I/usr/include/X11" \
	MLIBDIR="%{_datadir}/ray/meta" \
	COMPAT="bmalloc.o erf.o getpagesize.o" \
	LIBDIR=$wd/bin/lib \
	INSTDIR=$wd/bin/bin \
	SPECIAL=""
done

mv bin/bin/r{,ad}view
mv bin/bin/dev/* bin/bin

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/ray,%{_mandir}/man{1,3,5}}
rm -rf bin/bin/dev

tar cf - -C lib . | tar xf - -C $RPM_BUILD_ROOT%{_datadir}/ray
tar cf - -C bin/lib . | tar xf - -C $RPM_BUILD_ROOT%{_datadir}/ray
tar cf - -C bin/bin . | tar xf - -C $RPM_BUILD_ROOT%{_bindir}

# remove links to libtiff manuals
cd doc/man
rm -f man1/{fax2ps,*2tiff,pal2rgb,rgb2ycbcr,thumbnail,tiff*}.1
rm -f man3/{TIFF*,libtiff*}.3

for i in 1 3 5; do
	install man$i/*.$i $RPM_BUILD_ROOT%{_mandir}/man$i
done

cd ../..

find $RPM_BUILD_ROOT%{_libdir} doc -name CVS |xargs rm -rf
install %{SOURCE1} .

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_datadir}/ray
%{_mandir}/man?/*
%doc doc/ps doc/notes/* doc/*.1* README* license.txt
