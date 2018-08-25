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
    nmap <leader>ta <Plug>(python-style-swapper-mapping)
endif


function! s:PythonFunctionStyleToggle()
python << EOF
# from python_style_swapper import swapper
# # TODO : Remove this reload
# reload(swapper)
# 
# code = vim.current.window.buffer[:]
# (row, _) = vim.current.window.cursor
# row += 1
# 
# swapper.toggle(code, row)
EOF
endfunction


let g:style_swapper_loaded = 1
