from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto import Random


# Instantiate a crypto object first for encryptio
    #text : string
def encrypt(text):
# Set up the counter with a nonce.
# 64 bit nonce + 64 bit counter = 128 bit output
    nonce = Random.get_random_bytes(8)
    countf = Counter.new(64, nonce)
    key = Random.get_random_bytes(32) # 256 bits key
    encrypto = AES.new(key, AES.MODE_CTR, counter=countf)
    encrypted = encrypto.encrypt(text.encode('utf8'))
    return encrypted,key,nonce
# Reset counter and instantiate a new crypto object for decryption
def decrypt(encrypted,key,nonce):
    countf = Counter.new(64, nonce)
    decrypto = AES.new(key, AES.MODE_CTR, counter=countf)
    return  decrypto.decrypt(encrypted) # prints"asdk"
