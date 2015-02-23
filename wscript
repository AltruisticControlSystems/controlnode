#! /usr/bin/env python
# encoding: utf-8
#
# Altruistic Control Systems
# Control Node base wscript
# Kenneth Wells, 2015

import os, sys, re

from waflib import Options, Logs
from waflib import Configure

Configure.autoconfig = 1

# declaring the platforms that we build for
UNKNOWN     = -1
PI          = 0
LINUX       = 1
MAC         = 2
WINDOWS     = 3

CROSS_PLATFORMS = { 'pi' : PI,
    'linux' : LINUX,
    'mac' : MAC,
    'windows' : WINDOWS
    }

C_COMPILERS = { PI : 'gcc',
    LINUX : 'gcc',
    MAC : 'gcc',
    WINDOWS : 'cl'
    }

CXX_COMPILERS = { PI : 'g++',
    LINUX : 'g++',
    MAC : 'g++',
    WINDOWS : 'cl'
    }

def get_git_sha():
    version = 'UNDEFINED'
    if os.path.exists('.git'):
        try:
            version = os.popen('git describe --dirty --always').read.strip()
        except Exception, e:
            Logs.warn(e)

    return version

def pi_version():
    with open('/proc/cpuinfo','r') as infile:
        cpuinfo = infile.read()
    match = re.search(
        '^Hardware\s+:\s+(\w+)$',
        cpuinfo,
        flags=re.MULTILINE|re.IGNORECASE
        )

    if not match:
        return None
    elif match.group(1) == 'BCM2708':
        return 1
    elif match.group(1) == 'BCM2709':
        return 2
    else:
        # Unknown as of this file's creation
        return None

def get_platform():
    platform = sys.platform.lower()

    if platform == 'win32' or platform == 'cygwin':
        platform = WINDOWS
    elif platform == 'darwin' or platform == 'os2' or platform == 'os2emx':
        platform = MAC
    elif platform.startswith('linux'):
        if pi_version() is not None:
            platform = PI
        else:
            platform = LINUX
    else:
        platform = UNKNOWN

    return platform

top = '.'
out = 'build'

VERSION="0.0.1"
APPNAME='controlnode'
REVISION=''
GIT_SHA = get_git_sha()
PLATFORM = get_platform()
PI_VERSION = pi_version()

# this function is called before any other for parsing the command-line
def options(opt):
    opt.add_option(
        '--cross_compile',
        action='store_true',
        dest='CROSS_COMPILE',
        default=False,
        help='Build for another platform.'
        )

    opt.add_option(
        '--platform',
        action='store',
        dest='CROSS_COMPILE_PLATFORM',
        default='pi',
        help='Platform to build for when cross compiling. pi, linux, windows, mac'
        )

    opt.add_option(
        '--mode',
        action='store',
        dest='MODE',
        default='release',
        help='Options are test, debug, and release. Test only builds the unit tests'
        )

    opt.add_option(
        '--unit-tests',
        action='store_true',
        dest='UNIT_TESTS',
        default=False,
        help='build the unit tests'
        )

    opt.add_option(
        '--smoke-tests',
        action='store_true',
        dest='SMOKE_TESTS',
        default=False,
        help='Build the smoke tests. The smoke tests will test the integrated product'
        )

def configure(conf):
    print('-> configuring the project in ' + conf.path.abspath())

    if PLATFORM == UNKNOWN and not conf.options.CROSS_COMPILE:
        Logs.error('Platform is unknown. Did you mean to cross compile?')
    elif not conf.options.CROSS_COMPILE:
        # Compile for the native platform
        conf.env.PLATFORM = PLATFORM
    elif conf.options.CROSS_PLATFORM in CROSS_PLATFORMS:
        # Compile for the specified platform
        conf.env.PLATFORM = CROSS_PLATFORMS[conf.options.CROSS_PLATFORM]
    else:
        Logs.error('Build platform unknown')

    conf.env.VERSION = VERSION
    conf.env.GIT_SHA = GIT_SHA

    conf.env.UNIT_TESTS = conf.options.UNIT_TESTS
    conf.env.SMOKE_TESTS = conf.options.SMOKE_TESTS

    conf.find_program(C_COMPILERS[conf.env.PLATFORM], var='CC')
    conf.find_program(CXX_COMPILERS[conf.env.PLATFORM], var='CXX')

    conf.env.CXXFLAGS = ['-pipe','-Wall']
    conf.env.CXXFLAGS += ['-msse','-msse2','-mfpmath=sse']
    conf.env.CXXFLAGS += ['-Werror']

    if conf.options.MODE == 'debug':
        Logs.pprint('WHITE','-> building for debug mode')
        conf.env.CXXFLAGS += ['-g']
    elif conf.options.MODE == 'test':
        Logs.pprint('WHITE','-> building tests')
        conf.env.CXXFLAGS += ['-g']
    elif conf.options.Mode == 'release':
        Logs.pprint('WHITE','-> building release software')
        conf.env.CXXFLAGS += ['-O2']
    else:
        Logs.error('INVALID MODE SPECIFIED. Use test, debug, or release')

    conf.recurse('libraries')
    conf.recurse('source')

def build(bld):
    Logs.pprint('WHITE', '-> building from ' + bld.path.abspath())

    bld.recurse('libraries')
    bld.recurse('source')

    if bld.env.UNIT_TESTS:
        bld.recurse('unitTests')

    if bld.env.SMOKE_TESTS:
        bld.recurse('smokeTests')
