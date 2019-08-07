Note
----

This repository is deprecated in-favor of https://github.com/FooSoft/vim-argwrap. 
It's an overall better tool and works with all filetypes, not just Python.

Summary
-------

A Python tool that converts multi-line and single-line callable objects.

For example, convert this line:

```python
some.long(function, that, has, many arguments={'that': 'just'}, go='on', and_on=True)
```

To this line:

```python
some.long(
	function,
	that,
	has,
	many,
	arguments={'that': 'just'},
	go='on',
	and_on=True,
)
```

And back with just a single, reversible mapping.


Usage
-----
Once installed, all you need to do to swap from single-line and multi-line is
to type `<leader>sa`. See [Customizations](#Customizations) if you'd like 
to change the default mapping.


Requirements
------------

This plugin uses [astroid](https://pypi.org/project/astroid).
vim-python-style-swapper comes with its own copy of astroid but it's
recommended to install it yourself.

```python
pip install astroid
```


Installation
------------

Install everything in the [Requirements](#Requirements) section and then install
vim-textobj-block-party using a plugin manager or manually.


Plugin Manager Installation
---------------------------

I use [vim-plug](https://github.com/junegunn/vim-plug) to install
all of my plugins. The code to add it below looks like this:

```vim
Plug 'ColinKennedy/vim-python-style-swapper'
```

However this plugin should work with any plugin manager.


Manual Installation
-------------------

Clone this repository:

```bash
git clone https://github.com/ColinKennedy/vim-python-style-swapper
```

Move the files to their respective folders in your `~/.vim` directory
(or your `$HOME\vimfiles` directory if you're on Windows)


Customizations
--------------

Repeatable Mappings
-------------------

If you install [tpope/vim-repeat](https://github.com/tpope/vim-repeat) then
this plugin's mappings become repeatable. it's not required though.


Mapping Customization
---------------------

Also, `<leader>sa` is the default mapping for vim-python-style-swapper but it
can be overwritten. Just add this line to your .vimrc:

```vim
Plug 'ColinKennedy/vim-python-style-swapper'  " or whatever plugin installation lines you use
nmap <leader>ga <Plug>(vim-python-style-swapper-mapping)
```

Indentation
-----------

When vim-python-style-swapper changes a single line to a multi-line call, it
uses spaces `"    "` to add indentation. If you want to change indentation
then use `g:vim_python_style_swapper_indent`

3 Spaces:
`let g:vim_python_style_swapper_indent = "   "`

Tabs:
`let g:vim_python_style_swapper_indent = "\t"`
