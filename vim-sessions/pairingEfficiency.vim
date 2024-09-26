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
badd +398 privateTools/GetGenMatch_higgsPair_2024Aug.C
badd +390 privateTools/GetGenMatch_higgsPair_2024Aug_tree.C
badd +34 Notes/GetHiggPairEfficiencies.md
badd +1 privateTools/GetGenMatch.C
badd +1 studies/BranchNames/BranchNamesMacro_withType.cpp
badd +1 studies/BranchNames/73604338-57D0-0144-8089-C23BB6168001_Events.txt
badd +1 studies/BranchNames/bbbbNtuple_0_bbbbTree.txt
argglobal
%argdel
$argadd privateTools/GetGenMatch_higgsPair_2024Aug.C
edit Notes/GetHiggPairEfficiencies.md
argglobal
balt studies/BranchNames/BranchNamesMacro_withType.cpp
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
let s:l = 1 - ((0 * winheight(0) + 19) / 38)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 1
normal! 025|
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
