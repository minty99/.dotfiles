#
# Defines environment variables.
#
# See also: ~/.zsh/zsh.d/envs.zsh
#
#
# Authors:
#   Sorin Ionescu <sorin.ionescu@gmail.com>
#   Jongwook Choi <wookayin@gmail.com>
#

#
# Browser
#

if [[ "$OSTYPE" == darwin* ]]; then
  export BROWSER='open'
fi

export TERM="xterm-256color"

#
# Editors
#

export EDITOR='kak'
export VISUAL='kak'
export PAGER='less'

#
# Language
#

if [[ -z "$LANG" ]]; then
  export LANG='en_US.UTF-8'
fi

# Fix broken, wrong LC variables (e.g. kitty)
if [[ "$LC_CTYPE" == "UTF-8" ]]; then
  export LC_CTYPE='en_US.UTF-8'
fi


# dotfiles-populated bin.
if [ -d $HOME/.dotfiles/bin/ ]; then
  path=( $path $HOME/.dotfiles/bin )
fi

# rust (cargo)
if [ -d $HOME/.cargo/bin/ ]; then
  path=( $path $HOME/.cargo/bin )
fi
if [ -f "$HOME/.cargo/env" ]; then
  source "$HOME/.cargo/env"
fi

if [ -f "$HOME/.zshenv.local" ]; then
  source "$HOME/.zshenv.local"
fi
