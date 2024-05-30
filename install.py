# Ref: https://github.com/wookayin/dotfiles/blob/master/install.py

"""
@minty99's                ███████╗██╗██╗     ███████╗███████╗
██████╗  █████╗ ████████╗██╔════╝██║██║     ██╔════╝██╔════╝
██╔══██╗██╔══██╗╚══██╔══╝█████╗  ██║██║     █████╗  ███████╗
██║  ██║██║  ██║   ██║   ██╔══╝  ██║██║     ██╔══╝  ╚════██║
██████╔╝╚█████╔╝   ██║   ██║     ██║███████╗███████╗███████║
╚═════╝  ╚════╝    ╚═╝   ╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝

"""

print(__doc__)  # print logo.


import argparse
import json
import os
import sys
import subprocess

from sys import stderr


def _wrap_colors(ansicode):
    return lambda msg: ansicode + str(msg) + "\033[0m"


GRAY = _wrap_colors("\033[0;37m")
WHITE = _wrap_colors("\033[1;37m")
RED = _wrap_colors("\033[0;31m")
GREEN = _wrap_colors("\033[0;32m")
YELLOW = _wrap_colors("\033[0;33m")
CYAN = _wrap_colors("\033[0;36m")
BLUE = _wrap_colors("\033[0;34m")

unicode = lambda s, _: str(s)


def get_post_actions(args):
    post_actions = []

    post_actions += [
        """#!/bin/bash
        # Check whether and ~/.zsh are well-configured
        for f in ~/.zshrc; do
            if ! readlink $f >/dev/null; then
                echo -e "\033[0;31m\
    WARNING: $f is not a symbolic link to ~/.dotfiles.
    Please remove your local folder/file $f and try again.\033[0m"
                echo -n "(Press any key to continue) "; read user_confirm
                exit 1;
            else
                echo "$f --> $(readlink $f)"
            fi
        done """
    ]

    return post_actions


def parsing_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--force", action="store_true", default=False, help="If set, it will override existing symbolic links"
    )
    parser.add_argument("--symlink", action="store_true", help="If set, only create symlinks.")

    args = parser.parse_args()

    return args


def log(msg, cr=True):
    stderr.write(msg)
    if cr:
        stderr.write("\n")


def log_boxed(msg, color_fn=WHITE, use_bold=False, len_adjust=0):
    import unicodedata

    pad_msg = " " + msg + "  "
    l = sum(not unicodedata.combining(ch) for ch in unicode(pad_msg, "utf-8")) + len_adjust
    if use_bold:
        log(color_fn("┏" + ("━" * l) + "┓\n" + "┃" + pad_msg + "┃\n" + "┗" + ("━" * l) + "┛\n"), cr=False)
    else:
        log(color_fn("┌" + ("─" * l) + "┐\n" + "│" + pad_msg + "│\n" + "└" + ("─" * l) + "┘\n"), cr=False)


def makedirs(target, mode=511, exist_ok=False):
    os.makedirs(target, mode=mode, exist_ok=exist_ok)


def create_symlink(args):
    log_boxed("Creating symbolic links", color_fn=CYAN)
    with open("file_mappings.json", "r") as file:
        tasks = json.load(file)
    for target, source in sorted(tasks.items()):
        # normalize paths
        source = os.path.join(current_dir, os.path.expanduser(source))
        target = os.path.expanduser(target)

        # bad entry if source does not exists...
        if not os.path.lexists(source):
            log(RED("source %s : does not exist" % source))
            continue

        # if --force option is given, delete and override the previous symlink
        if os.path.lexists(target):
            is_broken_link = os.path.islink(target) and not os.path.exists(os.readlink(target))

            if args.force or is_broken_link:
                if os.path.islink(target):
                    os.unlink(target)
                else:
                    log(
                        "{:50s} : {}".format(
                            BLUE(target), YELLOW("already exists but not a symbolic link; --force option ignored")
                        )
                    )
            else:
                log(
                    "{:50s} : {}".format(
                        BLUE(target),
                        GRAY("already exists, skipped")
                        if os.path.islink(target)
                        else YELLOW("exists, but not a symbolic link. Check by yourself!!"),
                    )
                )

        # make a symbolic link if available
        if not os.path.lexists(target):
            mkdir_target = os.path.split(target)[0]
            makedirs(mkdir_target, exist_ok=True)
            log(GREEN("Created directory : %s" % mkdir_target))
            os.symlink(source, target)
            log("{:50s} : {}".format(BLUE(target), GREEN("symlink created from '%s'" % source)))


def run_post_actions(args):
    from signal import signal, SIGPIPE, SIG_DFL

    post_actions = get_post_actions(args)
    errors = []
    for action in post_actions:
        if not action:
            continue

        action_title = action.strip().split("\n")[0].strip()
        if action_title == "#!/bin/bash":
            action_title = action.strip().split("\n")[1].strip()

        log("\n", cr=False)
        log_boxed("Executing: " + action_title, color_fn=CYAN)
        ret = subprocess.call(["bash", "-c", action], preexec_fn=lambda: signal(SIGPIPE, SIG_DFL))

        if ret:
            errors.append(action_title)

    log("\n")
    if errors:
        log_boxed("You have %3d warnings or errors -- check the logs!" % len(errors), color_fn=YELLOW, use_bold=True)
        for e in errors:
            log("   " + YELLOW(e))
        log("\n")
    else:
        log_boxed("✔  You are all set! ", color_fn=GREEN, use_bold=True)

    return len(errors)


def main():
    global current_dir
    current_dir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(current_dir)

    os.system("git submodule update --init --recursive")

    args = parsing_args()
    create_symlink(args)
    if args.symlink:
        sys.exit()

    exit_code = run_post_actions(args)

    log("- Please restart shell (e.g. " + CYAN("`exec zsh`") + ") if necessary.")
    log("\n\n", cr=False)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
