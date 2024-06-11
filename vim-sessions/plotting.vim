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
badd +51 scripts/plotting/plotVars_2023Feb_mX_allUncertainties_maxShape.py
badd +1 scripts/plotting/VariableDicts.py
badd +176 scripts/plotting/plotVars_2023Feb_mX_allUncertainties_maxShape_beforeWeights.py
badd +5 scripts/plotting/plotVars_2023Feb_mX_allUncertainties_maxShape_hourglass.py
badd +39 scripts/plotting/plotVars_2023Feb_mX_signals.py
badd +140 Notes/Unroll.md
badd +1 scripts/plotting/plotVars_2023Feb_mH_signals.py
badd +134 Notes/fillHists.md
argglobal
%argdel
$argadd scripts/plotting/plotVars_2023Feb_mX_allUncertainties_maxShape.py
$argadd scripts/plotting/VariableDicts.py
edit scripts/plotting/plotVars_2023Feb_mX_signals.py
argglobal
if bufexists(fnamemodify("scripts/plotting/plotVars_2023Feb_mX_signals.py", ":p")) | buffer scripts/plotting/plotVars_2023Feb_mX_signals.py | else | edit scripts/plotting/plotVars_2023Feb_mX_signals.py | endif
if &buftype ==# 'terminal'
  silent file scripts/plotting/plotVars_2023Feb_mX_signals.py
endif
balt scripts/plotting/plotVars_2023Feb_mH_signals.py
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
let s:l = 39 - ((29 * winheight(0) + 28) / 56)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 39
normal! 034|
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
