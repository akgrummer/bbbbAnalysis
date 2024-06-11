let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd /uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_14_0_8/src/bbbbAnalysis/limits
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
if &shortmess =~ 'A'
  set shortmess=aoOA
else
  set shortmess=aoO
endif
badd +193 Notes/LEE.md
badd +26 prepareModels/make_biastest.sh
badd +106 Notes/GoF.md
badd +39 prepareModels/SubmitAllWorkspaces_fullPlane.sh
badd +239 prepareModels/SubmitWorkspaces_fullPlane.py
badd +36 prepareModels/addPDFSystematic.py
badd +82 prepareModels/prepareHistos.py
badd +257 prepareModels/makeDatacardsAndWorkspaces.py
badd +315 prepareModels/SubmitWorkspaces.py
badd +1 prepareModels/SubmitAllWorkspaces.sh
badd +1 prepareModels/listOfSamples_genToys.txt
badd +1 prepareModels/listOfSamples_10points.txt
badd +36 prepareModels/config/LimitsConfig_2016.cfg
badd +47 prepareModels/config/LimitsConfig_2017.cfg
badd +36 prepareModels/config/LimitsConfig_2018.cfg
badd +68 /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/t3submit
badd +4 prepareModels/SubmitAllLEEsignificance.sh
badd +222 prepareModels/SubmitLEEsignificance.py
badd +307 prepareModels/SubmitGoF.py
badd +1 prepareModels/SubmitAllGoF.sh
badd +1 prepareModels/listOfSamples.txt
badd +1 an-scripts/LEE_addInfoToSignifTree.cc
badd +299 an-scripts/Plot2DLimitMap.C
badd +331 an-scripts/PlotLimitsFromCondor.cc
badd +1 prepareModels/SubmitGenerateToys.py
badd +16 prepareModels/SubmitAllGenerateOnly.sh
badd +1 prepareModels/listOfSamples_LEE.txt
badd +181 prepareModels/SubmitFullRunIILimits_fullPlane.py
badd +6 prepareModels/SubmitAllLimits_fullPlane.sh
badd +57 an-scripts/LEE_getMaxSigma.cc
argglobal
%argdel
$argadd Notes/LEE.md
edit Notes/LEE.md
argglobal
balt an-scripts/LEE_getMaxSigma.cc
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
let s:l = 193 - ((24 * winheight(0) + 23) / 46)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 193
normal! 010|
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
