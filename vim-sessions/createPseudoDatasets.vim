let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd /uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_14_0_8/src/bbbbAnalysis
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
if &shortmess =~ 'A'
  set shortmess=aoOA
else
  set shortmess=aoO
endif
badd +45 scripts/createPsuedoDataset_localExcess_2024Jan.cpp
badd +15 studies/pseudoDatasets_2024Jan/Makefile
badd +22 hourglassUnc/Makefile
badd +239 scripts/add_hourglass_unc.C
badd +4 studies/pseudoDatasets_2024Jan/runPseudoDatasets.sh
badd +17 Notes/createPseudoDatasets.md
badd +1 studies/pseudoDatasets_2024Jan/bin/createPsuedoDataset_localExcess_2024Jan
argglobal
%argdel
$argadd scripts/createPsuedoDataset_localExcess_2024Jan.cpp
edit Notes/createPseudoDatasets.md
argglobal
balt studies/pseudoDatasets_2024Jan/runPseudoDatasets.sh
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
let s:l = 19 - ((18 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 19
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
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
