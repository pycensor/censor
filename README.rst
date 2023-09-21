NAME

::

   CENSOR - basis to prosecute 


DESCRIPTION

::

    CENSOR is a python3 IRC bot is intended to be programmable in a
    static, only code, no popen, no user imports and no reading
    modules from a directory, way. 

    CENSOR provides some functionality, it can connect to IRC, fetch
    and display RSS feeds, take todo notes, keep a shopping list and
    log text.

    CENSOR provides basis to prosecute (OTP-CR-117/19)

    CENSOR is here to be some kind of backup in case of censorship.


SYNOPSIS


::

    censor <cmd> [key=val] 
    censor <cmd> [key==val]
    censor [-c] [-d] [-v]


INSTALL


::

    $ pipx install censor


USAGE


::

    list of commands

    $ censor cmd
    cmd,err,flt,sts,thr,upt

    $ censor -a cmd

    cfg,cmd,dpl,err,flt,met,mod,mre,
    nme,pwd,rem,req,rss,sts,thr

    start a console

    $ censor -c
    >

    start additional modules

    $ censor mod=<mod1,mod2> -c
    >

    list of modules

    $ censor mod
    bsc,err,flt,irc,mod,req,rss,sts,thr

    to start irc, add mod=irc when
    starting

    $ censor -c mod=irc

    to start rss, also add mod=rss
    when starting

    $ censor -c mod=irc,rss

    start as daemon

    $ censor -d mod=irc,rss
    $ 


CONFIGURATION


::

    irc

    $ censor cfg server=<server>
    $ censor cfg channel=<channel>
    $ censor cfg nick=<nick>

    sasl

    $ censor pwd <nsvnick> <nspass>
    $ censor cfg password=<frompwd>

    rss

    $ censor rss <url>
    $ censor dpl <url> <item1,item2>
    $ censor rem <url>
    $ censor nme <url< <name>


COMMANDS


::

    cfg - irc configuration
    cmd - commands
    dpl - items of the feed to display
    err - show errors
    flt - instances registered
    met - add a user
    mod - show available modules
    mre - displays cached output
    nme - display name of a feed
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    req - request to the prosecutor
    rss - add a feed
    sts - status
    thr - show running threads


SYSTEMD

::

    change <name> to the user running pipx

    [Unit]
    Description=CENSOR
    Requires=network.target
    After=network.target

    [Service]
    DynamicUser=True
    Type=forking
    User=<name>
    Group=<name>
    PIDFile=censor.pid
    WorkingDirectory=/home/<name>/.censor
    ExecStart=/home/<name>/.local/pipx/venvs/censor/bin/censor -d mod=irc,rss
    RemainAfterExit=yes

    [Install]
    WantedBy=multi-user.target


FILES

::

    ~/.local/bin/censor
    ~/.local/pipx/venvs/censor/


AUTHOR

::

    Censor <pycensor@gmail.com>


COPYRIGHT

::

    CENSOR is placed in the Public Domain.
