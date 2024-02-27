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
badd +11699 CondorJobs/jobsLimits_2023Dec7_binMYx2_addMX650_10ev_unblind_SR/job_sig_NMSSM_bbbb_MX_700_MY_400.sh_79818311.stdout
badd +11680 CondorJobs/jobsLimits_2023Dec7_binMYx2_addMX650_10ev_unblind_repeat_SR/job_sig_NMSSM_bbbb_MX_700_MY_400.sh_30274045.stdout
badd +11700 CondorJobs/jobsLimits_2024Jan26_psuedoData_checkExcessLimits_mx700_my400_2_unblind_SR/job_sig_NMSSM_bbbb_MX_700_MY_400.sh_30274098.stdout
badd +11699 CondorJobs/jobsLimits_2024Jan26_psuedoData_checkExcessLimits_mx700_my400_2_unblind_sigX10_SR/job_sig_NMSSM_bbbb_MX_700_MY_400.sh_30274263.stdout
badd +11701 CondorJobs/jobsLimits_2023Dec7_binMYx2_addMX650_10ev_unblind_SR/job_sig_NMSSM_bbbb_MX_650_MY_350.sh_79818297.stdout
badd +11709 CondorJobs/jobsLimits_2024Jan26_psuedoData_checkExcessLimits_mx650_my350_2_unblind_sigX10_SR/job_sig_NMSSM_bbbb_MX_650_MY_350.sh_60366087.stdout
argglobal
%argdel
$argadd CondorJobs/jobsLimits_2024Jan26_psuedoData_checkExcessLimits_mx700_my400_sigX10_unblind_SR/job_sig_NMSSM_bbbb_MX_700_MY_400.sh_30273147.stdout
edit CondorJobs/jobsLimits_2023Dec7_binMYx2_addMX650_10ev_unblind_SR/job_sig_NMSSM_bbbb_MX_650_MY_350.sh_79818297.stdout
argglobal
balt CondorJobs/jobsLimits_2024Jan26_psuedoData_checkExcessLimits_mx650_my350_2_unblind_sigX10_SR/job_sig_NMSSM_bbbb_MX_650_MY_350.sh_60366087.stdout
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
let s:l = 11687 - ((16 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 11687
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
nohlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
