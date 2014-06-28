#!/usr/bin/env python

from Crypto.Cipher import AES
from Crypto import Random
from urllib2 import quote
from urllib2 import unquote
import base64
import string
import random

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(s[-1])]
DEFAULT_NUMB = lambda ran_key_range:''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(ran_key_range))

class EncryptionUtil:
    '''
       This class is helpful to encrypt and decrypt the text.
    '''
    CHAR_SET = 'utf8'
    def __init__( self, key = 'thistarathanyaga' ):
        self.key = key
    
    def encryptText( self, raw =  DEFAULT_NUMB(4)):
        raw = pad(str(raw))
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return quote(base64.urlsafe_b64encode( iv + cipher.encrypt( raw ) ).encode(self.CHAR_SET)) 

    def decryptText( self, enc ):
        enc = base64.urlsafe_b64decode(unquote(enc.encode(self.CHAR_SET)))
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))
    
    def getRandomToken(self, token_size = 4):
        '''
           This will get the random token based on the size specified.
           default is 4
        '''
        return DEFAULT_NUMB(4)
    
def gen_secret_key(raw):
    raw = pad(str(raw))
    iv = Random.new().read( AES.block_size )
    cipher = AES.new( 'thistarathanyaga', AES.MODE_CBC, iv )
    return quote(base64.urlsafe_b64encode( iv + cipher.encrypt( raw ) ).encode('utf8'))
    
if __name__ == '__main__':
    pass