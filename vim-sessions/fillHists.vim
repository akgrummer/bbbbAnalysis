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
badd +38 scripts/submitAllFillOnTier3_RunII.sh
badd +19 config/Resonant_NMSSM_bbbb/plotter_2016Resonant_NMSSM_XYH_bbbb_vars.cfg
badd +19 config/Resonant_NMSSM_bbbb/plotter_2017Resonant_NMSSM_XYH_bbbb_vars.cfg
badd +19 config/Resonant_NMSSM_bbbb/plotter_2018Resonant_NMSSM_XYH_bbbb_vars.cfg
badd +3260 config/Resonant_NMSSM_bbbb/selectionCfg_2016Resonant_NMSSM_XYH_bbbb_TrigCut_2023Feb27.cfg
badd +3242 config/Resonant_NMSSM_bbbb/selectionCfg_2017Resonant_NMSSM_XYH_bbbb_TrigCut_2023Feb27.cfg
badd +3245 config/Resonant_NMSSM_bbbb/selectionCfg_2018Resonant_NMSSM_XYH_bbbb_TrigCut_2023Feb27.cfg
badd +12 scripts/mergeHistograms.sh
badd +28 scripts/renameFullSubmissions.sh
badd +16 scripts/mergeHistograms.py
badd +6 testpy.py
badd +64 vim-sessions/fillHists.vim
badd +79 Notes/fillHists.md
badd +247 scripts/submitFillOnTier3.py
badd +68 config/Resonant_NMSSM_bbbb/plotter_2016Resonant_NMSSM_XYH_bbbb_Full_offShell.cfg
badd +68 config/Resonant_NMSSM_bbbb/plotter_2017Resonant_NMSSM_XYH_bbbb_Full_offShell.cfg
badd +68 config/Resonant_NMSSM_bbbb/plotter_2018Resonant_NMSSM_XYH_bbbb_Full_offShell.cfg
badd +8 Notes/Reminders.md
badd +40 config/Resonant_NMSSM_bbbb/plotter_2016Resonant_NMSSM_XYH_bbbb_Full.cfg
badd +1 config/Resonant_NMSSM_bbbb/plotter_2017Resonant_NMSSM_XYH_bbbb_Full.cfg
badd +1 config/Resonant_NMSSM_bbbb/plotter_2018Resonant_NMSSM_XYH_bbbb_Full.cfg
badd +68 scripts/t3submit
argglobal
%argdel
$argadd config/Resonant_NMSSM_bbbb/plotter_2016Resonant_NMSSM_XYH_bbbb_vars.cfg
edit Notes/fillHists.md
argglobal
balt scripts/submitAllFillOnTier3_RunII.sh
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
let s:l = 74 - ((32 * winheight(0) + 20) / 41)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 74
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
