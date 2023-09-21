NAME

::

   CENSOR - basis to prosecute (OTP-CR-117/19)


DESCRIPTION

::

    CENSOR is a python3 IRC bot is intended to be programmable in a
    static, only code, no popen, no user imports and no reading
    modules from a directory, way. 

    CENSOR provides some functionality, it can connect to IRC, fetch
    and display RSS feeds, take todo notes, keep a shopping list and
    log text.

    CENSOR provides basis to prosecute (OTP-CR-117/19) king netherlands
    for the crime of genocide at the ICC.

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

    start a console

    $ censor -c
    >

    start additional modules

    $ censor mod=<mod1,mod2> -c
    >

    list of modules

    $ censor mod
    bsc,err,flt,irc,log,mod,rss,shp,
    sts,tdo,thr,udp

    to start irc, add mod=irc when
    starting

    $ censor mod=irc -c

    to start rss, also add mod=rss
    when starting

    $ censor mod=irc,rss -c

    start as daemon

    $ censor mod=irc,rss -d
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

    cmd - commands
    cfg - irc configuration
    dlt - remove a user
    dpl - sets display items
    ftc - runs a fetching batch
    fnd - find objects 
    flt - instances registered
    log - log some text
    met - add a user
    mre - displays cached output
    nck - changes nick on irc
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    rss - add a feed
    slg - slogan
    thr - show the running threads


SYSTEMD

::

    change <name> to the user running pipx

    [Unit]
    Description=basis to prosecute (OTP-CR-117/19)
    Requires=network.target
    After=network.target

    [Service]
    DynamicUser=True
    Type=forking
    User=<name>
    Group=<name>
    PIDFile=censor.pid
    WorkingDirectory=/home/<name>/.censor
    ExecStart=/home/<name>/.local/pipx/venvs/censor/bin/censor -d
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
