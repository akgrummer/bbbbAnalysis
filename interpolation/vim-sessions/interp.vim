let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/interpolation
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
if &shortmess =~ 'A'
  set shortmess=aoOA
else
  set shortmess=aoO
endif
badd +100 TestInterpolatorHist_2023Apr.C
badd +0 TestInterpolator2.C
badd +79 TestInterpolatorHist2D.C
badd +44 TestInterpolatorHist2D2DReal.C
badd +53 TestInterpolatorHist2D2D.cc
badd +1 Makefile
badd +48 TestInterpolatorHist.C
badd +85 2023Apr26/InterpolateSignals.cc
badd +286 Interpolator.cc
badd +414 ../scripts/Unroll2DplotsSubRange.cc
badd +85 unroll2Dinterp.cc
argglobal
%argdel
$argadd TestInterpolatorHist_2023Apr.C
$argadd TestInterpolator2.C
$argadd TestInterpolatorHist_2023Apr.C
$argadd TestInterpolatorHist2D.C
$argadd TestInterpolatorHist2D2DReal.C
$argadd TestInterpolatorHist2D2D.cc
edit unroll2Dinterp.cc
argglobal
if bufexists(fnamemodify("unroll2Dinterp.cc", ":p")) | buffer unroll2Dinterp.cc | else | edit unroll2Dinterp.cc | endif
if &buftype ==# 'terminal'
  silent file unroll2Dinterp.cc
endif
balt ../scripts/Unroll2DplotsSubRange.cc
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 101 - ((29 * winheight(0) + 24) / 48)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 101
normal! 0
tabnext 1
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0 && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20
let &shortmess = s:shortmess_save
let s:sx = expand("<sfile>:p:r")."x.vim"
if filereadable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &g:so = s:so_save | let &g:siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
