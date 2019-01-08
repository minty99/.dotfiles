" Systax Highlight
syntax on

" Auto Indent
set autoindent
set cindent

" Show Line Numbers
set nu

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'
Plugin 'scrooloose/nerdtree'
Plugin 'vim-airline/vim-airline'
Plugin 'scrooloose/syntastic'
Plugin 'tpope/vim-fugitive'
Plugin 'connorholyday/vim-snazzy'
call vundle#end()            " required
filetype plugin indent on    " required

colorscheme snazzy
set ts=4
set shiftwidth=4
set laststatus=2 " Always show status bar
set statusline=\ %<%l:%v\ [%P]%=%a\ %h%m%r\ %F\
set backspace=indent,eol,start
