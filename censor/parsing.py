# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,W0212,E0402,W0201,W0613,E1120,R0902,W0105,W0612
# pylint: disable=W0718


"parsers"



def parse(obj, txt=None) -> None:
    args = []
    obj.args = obj.args or []
    obj.cmd = obj.cmd or ""
    obj.gets = obj.gets or {}
    obj.hasmods = obj.hasmod or False
    obj.mod = obj.mod or ""
    obj.opts = obj.opts or ""
    obj.result = obj.reult or []
    obj.sets = obj.sets or {}
    obj.otxt = txt or obj.txt or ""
    _nr = -1
    for spli in obj.otxt.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            if key == "mod":
                obj.hasmods = True
                if obj.mod:
                    obj.mod += f",{value}"
                else:
                    obj.mod = value
                continue
            obj.sets[key] = value
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            obj.gets[key] = value
            continue
        _nr += 1
        if _nr == 0:
            obj.cmd = spli
            continue
        args.append(spli)
    if args:
        obj.args = args
        obj.txt = obj.cmd or ""
        obj.rest = " ".join(obj.args)
        obj.txt = obj.cmd + " " + obj.rest
    else:
        obj.txt = obj.cmd
