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
badd +1 localCombineRuns/FitDiagnostics_2022Oct24
badd +142 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/PlotFitDiagnosticsSHAPES_NumEvents.py
badd +12 localCombineRuns/FitDiagnostics_2022Oct24/plotFits.py
badd +23 prepareModels/SubmitAllFitDiagnostic.sh
badd +70 prepareModels/SubmitFitDiagnostics.py
badd +7 FitDiagnostics/copyFilesLocal.sh
badd +18 prepareModels/SubmitAllGoF.sh
badd +59 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/RerollEvents.py
badd +64 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/GOF_2d_plots.py
badd +233 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/PlotFitDiagnostics.py
badd +12 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/runAllFitDiag2Dpull_LocalSignfPoints.sh
badd +9 FitDiagnostics/covQual/getVals.sh
badd +139 Notes/fitDiag.md
badd +1 FitDiagnostics/covQual
badd +457 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/PlotFitDiagnosticsSHAPES_LocalSignfPoints.py
badd +180 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/PlotFitDiagnosticsSHAPES_NumEvents_comp.py
badd +1 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/FitDiag_EventDist_compare3.py
badd +156 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/FitDiag_EventDist_compare3_5ev.py
badd +163 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/PlotFitDiagnosticsSHAPES_NumEvents_comp_5ev.py
badd +142 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/FitDiag2Dpull_LocalSignfPoints.py
badd +2 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/Reroll.sh
badd +1 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/FitDiag_EventDist_compare3_mxx2.py
badd +1 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/PlotFitDiagnosticsSHAPES_NumEvents_comp_mxx2.py
badd +1 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/compareEventDist3_5ev.sh
badd +1 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/compareEventDist3_mxx2.sh
badd +6 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/comparePulls_2024Jan24.sh
badd +1 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/PlotFitDiagnosticsSHAPES.py
badd +349 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/FitDiag2Dpull.py
badd +1 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/runAllFitDiag2Dpull.sh
argglobal
%argdel
$argadd localCombineRuns/FitDiagnostics_2022Oct24
edit Notes/fitDiag.md
argglobal
balt /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/runAllFitDiag2Dpull_LocalSignfPoints.sh
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
let s:l = 139 - ((35 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 139
normal! 055|
lcd /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/limits
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
