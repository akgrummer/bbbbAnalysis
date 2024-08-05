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
badd +248 Notes/fillHists.md
badd +70 Notes/skimming_ZjetsSamples.md
badd +8 Notes/Reminders.md
badd +60 vim-sessions/fillHists.vim
badd +100 scripts/submitAllFillOnTier3_RunII.sh
badd +98 scripts/submitAllFillOnTier3_RunII_el9part.sh
badd +280 scripts/submitFillOnTier3.py
badd +84 scripts/submitFillOnTier3_el9part.py
badd +222 scripts/submitFillOnTier3_old.py
badd +68 scripts/t3submit
badd +8 scripts/t3el7submit
badd +26 scripts/checkBkgCompJobs.sh
badd +8 scripts/mergeHistograms.sh
badd +34 scripts/renameFullSubmissions.sh
badd +16 scripts/mergeHistograms.py
badd +12 scripts/copyFilelists_Zjets.sh
badd +28 config/Resonant_NMSSM_bbbb/plotter_2016Resonant_NMSSM_XYH_bbbb_vars_mY90_Zjets_preVFP.cfg
badd +20 config/Resonant_NMSSM_bbbb/plotter_2016Resonant_NMSSM_XYH_bbbb_vars_mY90_Zjets.cfg
badd +32 config/Resonant_NMSSM_bbbb/plotter_2017Resonant_NMSSM_XYH_bbbb_vars_mY90_Zjets.cfg
badd +29 config/Resonant_NMSSM_bbbb/plotter_2018Resonant_NMSSM_XYH_bbbb_vars_mY90_Zjets.cfg
badd +1698 config/Resonant_NMSSM_bbbb/selectionCfg_2016Resonant_NMSSM_XYH_bbbb_TrigCut_2023Feb27_ULpreVFP.cfg
badd +1698 config/Resonant_NMSSM_bbbb/selectionCfg_2016Resonant_NMSSM_XYH_bbbb_TrigCut_2023Feb27_UL.cfg
badd +1676 config/Resonant_NMSSM_bbbb/selectionCfg_2017Resonant_NMSSM_XYH_bbbb_TrigCut_2023Feb27_UL.cfg
badd +1652 config/Resonant_NMSSM_bbbb/selectionCfg_2018Resonant_NMSSM_XYH_bbbb_TrigCut_2023Feb27_UL.cfg
badd +57 config/Resonant_NMSSM_bbbb/sampleCfg_2018Resonant_NMSSM_XYH_bbbb_all.cfg
badd +73 config/Resonant_NMSSM_bbbb/sampleCfg_2016Resonant_NMSSM_XYH_bbbb_all.cfg
badd +61 config/Resonant_NMSSM_bbbb/sampleCfg_2017Resonant_NMSSM_XYH_bbbb_all.cfg
badd +1 config/Resonant_NMSSM_bbbb/plotter_2016Resonant_NMSSM_XYH_bbbb_vars_mY90.cfg
badd +1 config/Resonant_NMSSM_bbbb/plotter_2017Resonant_NMSSM_XYH_bbbb_vars_mY90.cfg
badd +1 config/Resonant_NMSSM_bbbb/plotter_2018Resonant_NMSSM_XYH_bbbb_vars_mY90.cfg
badd +31 config/Resonant_NMSSM_bbbb/plotter_2016Resonant_NMSSM_XYH_bbbb_Full.cfg
badd +1 config/Resonant_NMSSM_bbbb/plotter_2017Resonant_NMSSM_XYH_bbbb_Full.cfg
badd +1 config/Resonant_NMSSM_bbbb/plotter_2018Resonant_NMSSM_XYH_bbbb_Full.cfg
badd +1 config/Resonant_NMSSM_bbbb/plotter_2016Resonant_NMSSM_XYH_bbbb_vars.cfg
badd +1 config/Resonant_NMSSM_bbbb/plotter_2017Resonant_NMSSM_XYH_bbbb_vars.cfg
badd +1 config/Resonant_NMSSM_bbbb/plotter_2018Resonant_NMSSM_XYH_bbbb_vars.cfg
badd +1 config/Resonant_NMSSM_bbbb/selectionCfg_2016Resonant_NMSSM_XYH_bbbb_TrigCut_2023Feb27.cfg
badd +1 config/Resonant_NMSSM_bbbb/selectionCfg_2017Resonant_NMSSM_XYH_bbbb_TrigCut_2023Feb27.cfg
badd +1 config/Resonant_NMSSM_bbbb/selectionCfg_2018Resonant_NMSSM_XYH_bbbb_TrigCut_2023Feb27.cfg
badd +68 config/Resonant_NMSSM_bbbb/plotter_2016Resonant_NMSSM_XYH_bbbb_Full_offShell.cfg
badd +68 config/Resonant_NMSSM_bbbb/plotter_2017Resonant_NMSSM_XYH_bbbb_Full_offShell.cfg
badd +68 config/Resonant_NMSSM_bbbb/plotter_2018Resonant_NMSSM_XYH_bbbb_Full_offShell.cfg
argglobal
%argdel
edit Notes/fillHists.md
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
balt Notes/skimming_ZjetsSamples.md
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
let s:l = 248 - ((27 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 248
normal! 0
lcd /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis
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
