let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd /uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_14_0_8/src/bbbbAnalysis
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
if &shortmess =~ 'A'
  set shortmess=aoOA
else
  set shortmess=aoO
endif
badd +1 scripts/UnrollAllSubdir_FullPlane.sh
badd +264 scripts/Unroll2DplotsSubRange_dev.cc
badd +134 Notes/Unroll.md
badd +109 scripts/calculateAllBKGshape_fullPlane.C
badd +690 scripts/MeasureBackgroundSystematic.C
badd +426 scripts/Unroll2DplotsSubRange.cc
badd +1 scripts/Unroll2DplotsSubRange_dev_saveLocation.cc
badd +189 scripts/Unroll2DplotsSubRange_dev_doubleMCStats.cc
badd +108 scripts/Unroll2DplotsSubRange_dev_hourglassMCStats_lowStatsCuts.cc
badd +50 Notes/Unroll-FullPlane.md
badd +187 scripts/Unroll2DplotsSubRange_dev_hourglassMCStats_lowStatsCuts_fullPlane.cc
badd +63 scripts/UnrollAllSubdir.sh
badd +125 scripts/calculateAllBKGshape.C
badd +118 ./scripts/modifyAllPlotForValidationTest_fullPlane.C
badd +1 ./scripts/modifyAllPlotForValidationTest.C
badd +12 ./scripts/Unroll_addTag.sh
argglobal
%argdel
$argadd scripts/UnrollAllSubdir_FullPlane.sh
edit Notes/Unroll-FullPlane.md
argglobal
balt ./scripts/modifyAllPlotForValidationTest_fullPlane.C
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
let s:l = 45 - ((32 * winheight(0) + 20) / 41)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 45
normal! 013|
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
set hlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
