#!/usr/bin/env python
# Copyright (c) 2021 Huawei Technologies Co., Ltd.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list
# of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# Neither the name of James William Pye nor the names of its contributors may be
# used to endorse or promote products derived from this software without specific
# prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

##
# setup.py - .release.distutils
##
import sys
import os

if sys.version_info[:2] < (3,3):
	sys.stderr.write(
		"ERROR: py-postgresql is for Python 3.3 and greater." + os.linesep
	)
	sys.stderr.write(
		"HINT: setup.py was ran using Python " + \
		'.'.join([str(x) for x in sys.version_info[:3]]) +
		': ' + sys.executable + os.linesep
	)
	sys.exit(1)

# distutils data is kept in `postgresql.release.distutils`
sys.path.insert(0, '')

sys.dont_write_bytecode = True
import py_opengauss.release.distutils as dist
defaults = dist.standard_setup_keywords()
sys.dont_write_bytecode = False

if __name__ == '__main__':
	try:
		from setuptools import setup
	except ImportError as e:
		from distutils.core import setup
	setup(**defaults)
