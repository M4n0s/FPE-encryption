#import hmac, hashlib
import string
from Crypto.Cipher import AES
#from libffx import pyffx
from Crypto.Random import random
from Crypto.Util.number import long_to_bytes, bytes_to_long

ccn = input('Insert 16-digit card number')
while (len(str(ccn)) != 16):
    ccn = input('Insert 16-digit card number')
#ccn = 4755682435349974
binary = '{0:054b}'.format(ccn)
print ('Card number in binary is: ', binary)
rounds = 4
result = []
keys = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
print ('Key is:', keys)
#key = ([bytes(k) for k in keys])[:4]
length = len(binary)
R0 = bytes(binary)[:length//2]
L0 = bytes(binary)[length//2:]

for i in range(rounds):
    result = R0
    func_res = nonlin_func(R0, keys, i)
    L0, R0 = R0, '{0:b}'.format( myXOR(int(L0, 2), int(func_res, 2)) )
    print('Right and left part of round', i, R0, L0)

result += R0
result = int(result, 2)

while (len(str(result)) != 16):
    i = i + 1
    result = R0
    func_res = nonlin_func(R0, keys, i)
    L0, R0 = R0, '{0:b}'.format( myXOR(int(L0, 2), int(func_res, 2)) )
    result += R0
    print('Right and left part of round', i, R0, L0)


print ('Encrypted number of card: ', result)



#Non linear function
def nonlin_func(r, key, lap):
    encrypter = AES.new(key, AES.MODE_ECB)
    block = int(r, 2) + lap
    block = '{0:032b}'.format(block)
    out = encrypter.encrypt(block)
    out = ''.join([str(x) for x in out])
    out = bytes_to_long(out)
    out = bin(int(out))
    out = out[2:29]
    return out


#XORfunction
def myXOR(x, y):
    return ((x or y) and  (~x or ~y))