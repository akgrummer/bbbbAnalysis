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
badd +51 Notes/bkgComposition.md
badd +27 vim-sessions/bkgComposition.vim
badd +1 scripts/privateScript/StackPlots.C
badd +1 scripts/privateScript/StackPlots_mY90GeV.C
badd +401 scripts/privateScript/StackPlots_mY90GeV_Zjets.C
badd +1 scripts/runBkgCompPlots_Zjets.sh
badd +1 scripts/runBkgCompPlots.sh
badd +8 scripts/cleanBkgCompVals.sh
badd +1 bkgCompValues/2024Jun11_vars.txt
badd +1 bkgCompValues/2024Jun11_vars_3b.txt
argglobal
%argdel
$argadd Notes/bkgComposition.md
edit Notes/bkgComposition.md
argglobal
balt scripts/runBkgCompPlots_Zjets.sh
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
let s:l = 51 - ((43 * winheight(0) + 22) / 44)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 51
normal! 031|
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
