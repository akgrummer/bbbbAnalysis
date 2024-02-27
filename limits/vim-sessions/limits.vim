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
badd +244 prepareModels/SubmitFullRunIILimits.py
badd +163 Notes/limits.md
badd +31 prepareModels/config/LimitsConfig_2016.cfg
badd +30 prepareModels/config/LimitsConfig_2017.cfg
badd +30 prepareModels/config/LimitsConfig_2018.cfg
badd +18 datacardExamples/datacard_2016_sig_NMSSM_bbbb_MX_300_MY_150.txt
badd +6 datacardExamples/datacard_RunII_sig_NMSSM_bbbb_MX_300_MY_150.txt
badd +1 prepareModels/listOfSamples.txt
badd +1 an-scripts/produceAllResults.sh
badd +1 an-scripts/PlotLimitsFromCondor.cc
badd +1 an-scripts/PlotLimitsFromCondor_allyears.cc
badd +68 ~/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/t3submit
badd +2 prepareModels/listOfSamples_10points.txt
argglobal
%argdel
$argadd prepareModels/SubmitFullRunIILimits.py
edit Notes/limits.md
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
balt prepareModels/config/LimitsConfig_2016.cfg
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
let s:l = 185 - ((18 * winheight(0) + 19) / 38)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 185
normal! 020|
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
set hlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
