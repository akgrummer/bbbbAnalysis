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
badd +23 an-scripts/produceAllResults.sh
badd +30 an-scripts/PlotLimitVsMy_orig.py
badd +35 Notes/produceResults.md
badd +181 ../privateTools/ProduceLimitTable.C
badd +123 Notes/limits.md
badd +214 an-scripts/PlotSignificanceFromCondor.cc
badd +125 Notes/fitDiag.md
badd +288 scripts/plotting/FitDiag2Dpull.py
badd +138 an-scripts/Plot2DSignificanceMap.C
badd +183 scripts/plotting/PlotFitDiagnosticsSHAPES.py
badd +111 an-scripts/PlotLimitVsMy_orig_twoLimits.py
badd +10 an-scripts/unblindingLimits_2023Dec14.sh
badd +13 an-scripts/produceMeanLimitPlots.sh
badd +75 an-scripts/PlotSignficanceDist.py
badd +96 prepareModels/config/LimitsConfig_2018.cfg
badd +4 an-scripts/produce2DlimitMap.sh
badd +159 an-scripts/PlotLimitsFromCondor.cc
badd +1 an-scripts/Plot2DLimitMap.C
badd +98 an-scripts/PlotLimitMean.py
argglobal
%argdel
$argadd an-scripts/produceAllResults.sh
edit Notes/produceResults.md
argglobal
balt an-scripts/Plot2DSignificanceMap.C
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
let s:l = 37 - ((36 * winheight(0) + 34) / 68)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 37
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
set hlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
