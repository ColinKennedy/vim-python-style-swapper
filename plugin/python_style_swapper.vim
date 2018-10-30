if !has('python')
    echoerr "vim-python-style-swapper requires Python. Cannot continue loading this plugin"
    finish
endif

if get(g:, 'style_swapper_loaded', '0') == '1'
    finish
endif

command! -nargs=0 PythonFunctionStyleToggle call s:PythonFunctionStyleToggle()

if !hasmapto('<Plug>(vim-python-style-swapper-mapping)')
    nmap <leader>sa <Plug>(vim-python-style-swapper-mapping)
endif

" Plugin mappings
try
    " If [tpope/vim-repeat](https://github.com/tpope/vim-repeat) is installed, use it
    nnoremap <silent> <Plug>(vim-python-style-swapper-mapping) :PythonFunctionStyleToggle<CR>:call repeat#set("\<Plug>(vim-python-style-swapper-mapping)")<CR>
catch /\VUnknown function/
    " The plugin wasn't installed so just use a normal mapping
    nnoremap <silent> <Plug>(vim-python-style-swapper-mapping) :PythonFunctionStyleToggle<CR>
endtry


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
