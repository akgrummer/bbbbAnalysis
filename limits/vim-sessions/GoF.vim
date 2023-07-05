let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/limits
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
if &shortmess =~ 'A'
  set shortmess=aoOA
else
  set shortmess=aoO
endif
badd +58 Notes/GoF.md
badd +16 an-scripts/GoFsubmit2018.sh
badd +5 an-scripts/copyDatacards.sh
badd +9 test.sh
badd +1 an-scripts/GoFsubmit2016.sh
badd +1 an-scripts/GoFsubmit2017.sh
badd +289 an-scripts/plotGOF_aidan.py
badd +1 an-scripts/plotGOF.sh
badd +79 prepareModels/SubmitGoF.py
badd +28 prepareModels/addPDFSystematic.py
badd +23 Notes/limits.md
badd +28 prepareModels/listOfSamples.txt
badd +8 prepareModels/GoFcheckStatus.sh
badd +38 prepareModels/mergeGOFs.py
badd +26 prepareModels/SubmitAllGoF.sh
badd +9 prepareModels/mergeAllGOFs.sh
badd +98 scripts/plotting/GOF_2d_plots.py
badd +11 prepareModels/SubmitWorkspaces.py
badd +1 prepareModels/SubmitFullRunIILimits.py
badd +1 prepareModels/config/LimitsConfig_2016.cfg
badd +1 prepareModels/config/LimitsConfig_2017.cfg
badd +1 prepareModels/config/LimitsConfig_2018.cfg
badd +6 prepareModels/SubmitAllWorkspaces.sh
badd +1 ~/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/t3submit
argglobal
%argdel
$argadd Notes/GoF.md
$argadd an-scripts/GoFsubmit2018.sh
$argadd an-scripts/copyDatacards.sh
edit Notes/GoF.md
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
balt ~/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/t3submit
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
let s:l = 58 - ((32 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 58
normal! 0
tabnext 1
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0 && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20
let &shortmess = s:shortmess_save
let &winminheight = s:save_winminheight
let &winminwidth = s:save_winminwidth
let s:sx = expand("<sfile>:p:r")."x.vim"
if filereadable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &g:so = s:so_save | let &g:siso = s:siso_save
nohlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
