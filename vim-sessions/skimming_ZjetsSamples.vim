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
badd +104 Notes/skimming_ZjetsSamples.md
badd +123 Notes/skimming_MoreSignals.md
badd +2 scripts/calculateAllPileupHistograms.sh
badd +130 scripts/computeAllPUWeights.sh
badd +55 scripts/computeZjetsPUWeights.sh
badd +1 scripts/computeMoreSignalsPUWeights.sh
badd +1 MoreSignals/MX650/NMSSM_XToYHTo4B_MX-650_MY-100_2016.txt
badd +1 nanoaod_zjets/2016_Zjets.json
badd +30 scripts/GetZjetsfiles.sh
badd +16 scripts/submitAllSkimsOnTier3_Zjets.sh
badd +1 scripts/submitAllSkimsOnTier3_moreSignals_mX650.sh
badd +28 config/Resonant_NMSSM_bbbb/skim_2016Resonant_NMSSM_XYH_bbbb.cfg
badd +4 config/Resonant_NMSSM_bbbb/skim_2016Resonant_NMSSM_XYH_bbbb_UL_preVFP.cfg
badd +66 scripts/submitSkimOnTier3.py
badd +55 scripts/submitSkimOnTier3_el9part.py
badd +68 scripts/t3el7submit
badd +841 CondorJobs/skimming/jobs_Zjets_2017_HT200to400/SKIM_ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/job_1.sh_3452690.stdout
badd +904 CondorJobs/skimming/jobs_Zjets_2017_HT200to400/SKIM_ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/job_1.sh_33028607.stdout
badd +476 CondorJobs/skimming/jobs_Zjets_2016_HT400to600/SKIM_ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/job_1.sh_33028601.stdout
badd +1 inputFiles/Zjets/2016
badd +1 inputFiles/Zjets/2016/ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8.txt
badd +1 inputFiles/Zjets/2016preVFP
badd +1 inputFiles/Zjets/2016preVFP/ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8.txt
badd +496 CondorJobs/skimming/jobs_Zjets_2016_HT400to600/SKIM_ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/job_1.sh_3452688.stdout
argglobal
%argdel
$argadd Notes/skimming_ZjetsSamples.md
edit Notes/skimming_ZjetsSamples.md
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
balt scripts/submitAllSkimsOnTier3_Zjets.sh
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
let s:l = 104 - ((27 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 104
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
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
