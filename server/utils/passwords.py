# encoding:utf-8
from passlib.hash import argon2


def hash(password):
    return argon2.hash(password)


def verify(password, hash):
    return argon2.verify(hash, password)


def check(hash):
    return argon2.check_needs_rehash(hash)