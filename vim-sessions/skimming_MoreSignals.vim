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
badd +2 scripts/computeMoreSignalsPUWeights.sh
badd +28 MoreSignals/NMSSM_XYH_bbbb_MX_1000_MY_150_NANOAOD_v7_2017.txt
badd +123 Notes/skimming_MoreSignals.md
badd +68 config/Resonant_NMSSM_bbbb/skim_2016Resonant_NMSSM_XYH_bbbb_Fast.cfg
badd +178 config/Resonant_NMSSM_bbbb/skim_2017Resonant_NMSSM_XYH_bbbb.cfg
badd +1 JECfiles/Fall17_17Nov2017_V32_MC_UncertaintySources_AK4PFchs.txt
badd +1 scripts/skimMoreSignals.sh
badd +59 looseFiles/FromFabio/test/skim_ntuple.cpp
badd +9 privateTools/usefullCommands.txt
badd +125 scripts/computeAllPUWeights.sh
badd +143 scripts/submitAllSkimsOnTier3_2016.sh
badd +147 scripts/submitAllSkimsOnTier3_2017.sh
badd +252 scripts/submitSkimOnTier3.py
badd +1 scripts/submitAllSkimsOnTier3_2017_moreSignals.sh
badd +1 ./scripts/submitAllSkimsOnTier3_moreSignals_mX650.sh
argglobal
%argdel
$argadd scripts/computeMoreSignalsPUWeights.sh
edit Notes/skimming_MoreSignals.md
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
balt ./scripts/submitAllSkimsOnTier3_moreSignals_mX650.sh
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
let s:l = 120 - ((29 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 120
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
