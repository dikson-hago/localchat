#!/usr/bin/env python3
from random import randint
class RSA:
    own_e = 0
    own_n = 0
    alien_e = 0
    alien_n = 0
    ph = 0
    p = 0
    q = 0
    d = 0

    def get_random_simple(self, RandomNum: int):
        i = 1000 + randint(0, 1000)
        while 1:
            k = 2
            simple = True
            while k * k <= i and simple:
                if i % k == 0:
                    simple = False
            if simple:
                RandomNum = i
                break
            i = i + 1

    def get_e(self):
        self.own_e = 5
        while 1:
            k = 2
            can_ans = True
            while k * k <= self.own_e:
                if self.own_e % k == 0 and self.ph % k == 0:
                    can_ans = False
                    break
            if can_ans:
                return

    def get_d(self):
        self.d = 1
        while 1:
            if (self.d * self.own_e) % self.ph == 1:
                return
            self.d = self.d + 1

    def __init__(self):
        self.get_random_simple(self.p)
        self.get_random_simple(self.q)
        self.own_n = self.p * self.q
        self.ph = (self.p - 1) * (self.q - 1)
        self.get_e()
        self.get_d()

    def encrypt(self, data: str):
        result = ''
        for i in range(0, len(data)):
            c = (ord(data[i]) ** self.alien_e) % self.alien_n
            result = str(c) + '|'
        return result

    def decrypt(self, data: str):
        symbol = ''
        c = 0
        message = ''
        for i in range(0, len(data)):
            if data[i] == '|':
                c = int(symbol)
                message = message + str((c ** self.d) % self.own_n)
                symbol = ''
            else:
                symbol = symbol + data[i]
        return message

    def get_open_key(self, e: int, n: int):
        self.alien_e = e
        self.alien_n = n