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
# .protocol.version
##
"""
PQ version class used by startup messages.
"""
from struct import Struct
version_struct = Struct('!HH')

class Version(tuple):
	"""
	Version((major, minor)) -> Version

	Version serializer and parser.
	"""
	major = property(fget = lambda s: s[0])
	minor = property(fget = lambda s: s[1])

	def __new__(subtype, major_minor):
		(major, minor) = major_minor
		major = int(major)
		minor = int(minor)
		# If it can't be packed like this, it's not a valid version.
		try:
			version_struct.pack(major, minor)
		except Exception as e:
			raise ValueError("unpackable major and minor") from e

		return tuple.__new__(subtype, (major, minor))

	def __int__(self):
		return (self[0] << 16) | self[1]

	def bytes(self):
		return version_struct.pack(self[0], self[1])

	def __repr__(self):
		return '%d.%d' %(self[0], self[1])

	def parse(self, data):
		return self(version_struct.unpack(data))
	parse = classmethod(parse)

CancelRequestCode = Version((1234, 5678))
NegotiateSSLCode = Version((1234, 5679))
V2_0 = Version((2, 0))
V3_0 = Version((3, 0))
V3_51 = Version((3, 51)) # add for openGauss
