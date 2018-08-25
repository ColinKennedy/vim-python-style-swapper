if !has('python')
    echoerr "python-style-swapper requires Python. Cannot continue loading this plugin"
    finish
endif

if get(g:, 'style_swapper_loaded', '0') == '1'
    finish
endif

command! -nargs=0 PythonFunctionStyleToggle call s:PythonFunctionStyleToggle()

" Plugin mappings
nnoremap <silent> <Plug>(python-style-swapper-mapping) :PythonFunctionStyleToggle<CR>


" Create default mappings if they are not defined
if !hasmapto('<Plug>(python-style-swapper-mapping)')
    nmap <leader>sa <Plug>(python-style-swapper-mapping)
endif


function! s:PythonFunctionStyleToggle()
python << EOF
from python_style_swapper import swapper
from python_style_swapper import vim_swapper
# TODO : Remove this reload
reload(swapper)
reload(vim_swapper)

vim_swapper.toggle()
EOF
endfunction


let g:style_swapper_loaded = 1
