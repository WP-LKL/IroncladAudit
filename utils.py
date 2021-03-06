from Crypto.Cipher import AES
from Crypto import Random
import base64
import os
import sys
import json

#import option debug from config 
with open('config.json','r') as x:
    config = json.load(x)
debug        = config["DEBUG"]



def obfuscate(txt : str):
    """ 
    Over-shoulder "attack" protection.
    Customize in utils.py and here.
    """
    obfuscated = base64.b64encode(txt.encode("utf-8"))
    if debug : print(f"obfuscate()   input: {txt}. Output: {obfuscated}")
    return obfuscated

def deObfuscate(txt : str):
    deObf = base64.b64decode(txt)
    if debug : print(f"deObfuscate() input: {txt}. Output: {deObf}")
    return deObf.decode("utf-8")

def verifyKey(txt) -> bool:
    obf = obfuscate(txt)
    deObf = deObfuscate(obf)
    if debug : print(f"verifyKey()   input: {txt}. Output: {deObf}")
    return txt == deObf 

class AESCipher:
    def __init__( self, key ):
        self.key = key

    def encrypt( self, s ):
        s = s[:-ord(s[len(s)-1:])]  # pad(s)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( s.encode("utf8") ) ) 

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        s = (cipher.decrypt( enc[16:] ))
        return s  # unpad(s)
    
random_key = os.urandom(16)
enc = AESCipher(random_key)
encrypted = enc.encrypt("0xabcMyKey")


if __name__ == "__main__":
    key = sys.argv[1]
    assert verifyKey(key), "ERROR: Could not verify base64-pair"
    print(obfuscate(key))