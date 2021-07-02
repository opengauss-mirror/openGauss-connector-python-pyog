# -*- coding: utf-8 -*-

import hmac
from hashlib import md5, pbkdf2_hmac, sha256
from ..python.structlib import ulong_unpack

PLAIN_PASSWORD = 0
MD5_PASSWORD = 1
SHA256_PASSWORD = 2


def sha256_pw(user, password, salt):
	password_stored_method, salt = ulong_unpack(salt[:4]), salt[4:]
	if password_stored_method in (PLAIN_PASSWORD, SHA256_PASSWORD):
		random64_code_str, salt = salt[:64].decode(), salt[64:]
		token_str, salt = salt[:8].decode(), salt[8:]
		iteration = ulong_unpack(salt[:4])
		return rfc5802_algorithm(password, random64_code_str, token_str, "", iteration)
	elif password_stored_method == 1:
		# MD5
		pw = md5(password + user).hexdigest().encode('ascii')
		return b'md5' + md5(pw + salt[:4]).hexdigest().encode('ascii')
	else:
		raise Exception("pq: the password-stored method is not supported, must be plain, md5 or sha256.")


def rfc5802_algorithm(password, random64_code_str, token_str, server_signature, server_iteration):
	k = generate_k_from_pbkdf2(password, random64_code_str, server_iteration)
	server_key = get_key_from_hmac(k, b'Sever Key')
	client_key = get_key_from_hmac(k, b'Client Key')
	stored_key = get_sha256(client_key)
	token_bytes = hex_string_to_bytes(token_str)
	client_signature = get_key_from_hmac(server_key, token_bytes)
	if server_signature != "" and server_signature != bytes_to_hex_string(client_signature):
		return b''
	hmac_result = get_key_from_hmac(stored_key, token_bytes)
	h = XOR_between_password(hmac_result, client_key, len(client_key))
	return bytes_to_hex(h)


def XOR_between_password(password1, password2, length):
	arr = bytearray()
	for i in range(length):
		arr.append(password1[i] ^ password2[i])
	return bytes(arr)


def bytes_to_hex(bytes_array):
	lookup = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
	res = ""
	for i in range(len(bytes_array)):
		c = bytes_array[i] & 0xFF
		j = c >> 4
		res += (lookup[j])
		j = (c & 0xF)
		res += (lookup[j])
	return res.encode('ascii')


def get_key_from_hmac(k, key):
	h = hmac.new(k, digestmod=sha256)
	h.update(key)
	return h.digest()


def get_sha256(key):
	h = sha256()
	h.update(key)
	return h.digest()


def generate_k_from_pbkdf2(password, random64_code_str, iterations):
	random32_code = hex_string_to_bytes(random64_code_str)
	return pbkdf2_hmac('sha1', password, random32_code, iterations, dklen=32)


def hex_string_to_bytes(s):
	if not s:
		return b''

	arr = bytearray()
	s = s.upper()
	bytes_len = int(len(s) / 2)
	for i in range(bytes_len):
		pos = i * 2
		arr.append(ctoi(s[pos]) << 4 | ctoi(s[pos + 1]))
	return bytes(arr)


def bytes_to_hex_string(bs):
	s = ""
	for b in bs:
		v = b & 0xFF
		hv = "%x" % v
		if len(hv) < 2:
			s += hv
			s += "0"
		else:
			s += hv
	return s


def ctoi(c):
	return "0123456789ABCDEF".index(c)
