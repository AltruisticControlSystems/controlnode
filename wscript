#! /usr/bin/env python
# encoding: utf-8
# Thomas Nagy, 2005-2015

"""
to make a custom waf file use the option --tools

To add a tool that does not exist in the folder compat15, pass an absolute path:
./waf-light  --tools=compat15,/comp/waf/aba.py --prelude=$'\tfrom waflib.extras import aba\n\taba.foo()'
"""


VERSION="0.0.1"
APPNAME='controlnode'
REVISION=''

top = '.'
out = 'build'

#from tokenize import *
import tokenize

import os, sys, re, io, optparse

from waflib import Utils, Options, Logs
from hashlib import md5

from waflib import Configure
Configure.autoconfig = 1

def sub_file(fname, lst):

    f = open(fname, 'rU')
    try:
        txt = f.read()
    finally:
        f.close()

    for (key, val) in lst:
        re_pat = re.compile(key, re.M)
        txt = re_pat.sub(val, txt)

    f = open(fname, 'w')
    try:
        f.write(txt)
    finally:
        f.close()

def to_bytes(x):
    if sys.hexversion>0x300000f:
        return x.encode()
    return x

print("------> Executing code from the top-level wscript <-----")
def init(ctx):
    if Options.options.setver: # maintainer only (ita)
        ver = Options.options.setver
        hexver = Utils.num2ver(ver)
        hexver = '0x%x'%hexver
        sub_file('wscript', (('^VERSION=(.*)', 'VERSION="%s"' % ver), ))
        sub_file('waf-light', (('^VERSION=(.*)', 'VERSION="%s"' % ver), ))

        pats = []
        pats.append(('^WAFVERSION=(.*)', 'WAFVERSION="%s"' % ver))
        pats.append(('^HEXVERSION(.*)', 'HEXVERSION=%s' % hexver))

        try:
            rev = ctx.cmd_and_log("git rev-parse HEAD").strip()
            pats.append(('^WAFREVISION(.*)', 'WAFREVISION="%s"' % rev))
        except Exception:
            pass

        sub_file('waflib/Context.py', pats)

        sys.exit(0)

def check(ctx):
    Logs.warn('Nothing to do')

# this function is called before any other for parsing the command-line
def options(opt):

    # generate waf
    opt.add_option('--make-waf', action='store_true', default=True,
        help='creates the waf script', dest='waf')

    opt.add_option('--sign', action='store_true', default=False, help='make a signed file', dest='signed')

    opt.add_option('--zip-type', action='store', default='bz2',
        help='specify the zip type [Allowed values: %s]' % ' '.join(zip_types), dest='zip')

    opt.add_option('--make-batch', action='store_true', default=False,
        help='creates a convenience waf.bat file (done automatically on win32 systems)',
        dest='make_batch')

    opt.add_option('--yes', action='store_true', default=False,
        help=optparse.SUPPRESS_HELP,
        dest='yes')

    # those ones are not too interesting
    opt.add_option('--set-version', default='',
        help='sets the version number for waf releases (for the maintainer)', dest='setver')

    opt.add_option('--strip', action='store_true', default=True,
        help='shrinks waf (strip docstrings, saves 33kb)',
        dest='strip_comments')
    opt.add_option('--nostrip', action='store_false', help='no shrinking',
        dest='strip_comments')
    opt.add_option('--tools', action='store', help='Comma-separated 3rd party tools to add, eg: "compat,ocaml" [Default: "compat15"]',
        dest='add3rdparty', default='compat15')
    opt.add_option('--coretools', action='store', help='Comma-separated core tools to add, eg: "vala,tex" [Default: all of them]',
        dest='coretools', default='default')
    opt.add_option('--prelude', action='store', help='Code to execute before calling waf', dest='prelude', default=PRELUDE)
    opt.load('python')

def configure(conf):
    conf.load('python')
    conf.check_python_version((2,4))

def build(bld):
    #waf = bld.path.make_node('waf') # create the node right here
    #bld(name='create_waf', rule=create_waf, target=waf, always=True, color='PINK', update_outputs=True)

