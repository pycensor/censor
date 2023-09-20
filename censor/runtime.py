# This file is placed in the Public Domain.
#
# pylint: disable=E0611,E0402,C0301,C0413,C0116,W0212


"main"


import os
import sys
import termios
import time
import traceback


sys.path.insert(0, os.getcwd())


from .command import command
from .command import scan as scancmd
from .console import CLI, Console
from .excepts import debug, errors
from .message import wait
from .objects import Object
from .parsing import parse
from .storage import workdir
from .storage import scan as scanstore
from .threads import launch
from .utility import mods, spl


from . import excepts


TIME = time.ctime(time.time()).replace("  ", " ")


Cfg = Object()
Cfg.cmd = ""
Cfg.gets = Object()
Cfg.mod = "bsc,err,flt,irc,rss,sts,thr,ver"
Cfg.name = "censor"
Cfg.opts = ""
Cfg.result = []
Cfg.sets = Object()
Cfg.slogan = "reinforcement degrades performance"
Cfg.version = "4"
Cfg.description = f"{Cfg.name.upper()} {Cfg.version} {Cfg.mod.upper()} {Cfg.slogan}"


from . import modules


def daemon():
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    os.umask(0)
    with open('/dev/null', 'r', encoding="utf-8") as sis:
        os.dup2(sis.fileno(), sys.stdin.fileno())
    with open('/dev/null', 'a+', encoding="utf-8") as sos:
        os.dup2(sos.fileno(), sys.stdout.fileno())
    with open('/dev/null', 'a+', encoding="utf-8") as ses:
        os.dup2(ses.fileno(), sys.stderr.fileno())


def scan(pkg, modnames="", initer=False, dowait=False) -> []:
    if not pkg:
        return []
    inited = []
    scanned = []
    threads = []
    #if not modnames:
    #    modnames = ",".join(mods(pkg.__path__[0]))
    for modname in spl(modnames):
        module = getattr(pkg, modname, None)
        if not module:
            continue
        scanned.append(modname)
        scancmd(module)
        scanstore(module)
        if initer:
            try:
                module.init
            except AttributeError:
                continue
            inited.append(modname)
            threads.append(launch(module.init, name=f"init {modname}"))
    if dowait:
        for thread in threads:
            thread.join()
    return inited


def wrap(func) -> None:
    if "d" in Cfg.opts:
        debug("terminal disabled!")
        return
    old = None
    try:
        old = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (EOFError, KeyboardInterrupt):
        print("")
        sys.stdout.flush()
    finally:
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)
    for exc in errors:
        traceback.print_exception(
                                  type(exc),
                                  exc,
                                  exc.__traceback__
                                 )


def main():
    parse(Cfg, " ".join(sys.argv[1:]))
    if "a" in Cfg.opts:
        Cfg.mod = ",".join(mods(modules.__path__[0]))
    if "d" in Cfg.opts:
        daemon()
        with open(os.path.join(workdir, "censor.pid", "w")) as pid:
            pid.write(os.getpid())
            pid.close()
        scan(modules, Cfg.mod, True)
        while 1:
            time.sleep(1.0)
        return
    if "v" in Cfg.opts:
        excepts.output = print
        Cfg.description = f"{Cfg.name.upper()} {Cfg.version} {Cfg.mod.upper()} {Cfg.opts.upper()} {Cfg.slogan} !!"
        debug(Cfg.description)
    if "c" in Cfg.opts:
        scan(modules, Cfg.mod, True, True)
        csl = Console()
        csl.start()
        csl.forever()
    else:
        scan(modules, Cfg.mod)
        cli = CLI()
        evt = Object()
        evt.orig = object.__repr__(cli)
        evt.txt = Cfg.otxt
        command(evt)
        wait(evt)



def wrapped():
    wrap(main)


if __name__ == "__main__":
    wrapped()
