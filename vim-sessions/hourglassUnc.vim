let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
if &shortmess =~ 'A'
  set shortmess=aoOA
else
  set shortmess=aoO
endif
badd +189 scripts/add_hourglass_unc.C
badd +1 createhists
badd +9 createhists/HistFileClass.cpp
badd +33 createhists/HistFileClass.h
badd +1 interpolation/2023Apr26/InterpolateSignals.cc
badd +423 scripts/plotting/plotVars_2022Feb.py
badd +72 scripts/calculateAllBKGshape.C
badd +13 hourglassUnc/Makefile
badd +1 createhists/Makefile
badd +330 scripts/Unroll2DplotsSubRange.cc
badd +18 scripts/calculateHourglassUnc.C
badd +1 scripts/add_hourglass_unc_VR.C
badd +25 Notes/hourglassUnc.md
badd +228 scripts/add_hourglass_unc_VR_forLimits.C
argglobal
%argdel
$argadd scripts/add_hourglass_unc.C
edit Notes/hourglassUnc.md
argglobal
balt scripts/add_hourglass_unc_VR_forLimits.C
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
let s:l = 25 - ((24 * winheight(0) + 19) / 38)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 25
normal! 049|
lcd /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis
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
nohlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
