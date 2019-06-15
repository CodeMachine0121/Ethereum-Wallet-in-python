from pybleno import Characteristic
import array
import struct
import sys
import traceback
from builtins import str
import Ctr
import random
import Wallet as wt
from Wallet import makeTxn as mt

def Seeds(): #產生亂數
    n=0
    while True:
        n =  random.randint(1,99999999) #sharekey
        if n/10000000 >1 :
            break
    return str(n)
class EchoCharacteristic(Characteristic):
    global key , nonce , seed,enseed #show key nonce to Qrcode
    def __init__(self, uuid):
        Characteristic.__init__(self, {
            'uuid': uuid,
            'properties': ['read', 'write', 'notify'],
            'value': None
          })
        self._value = array.array('B', [0] * 0)
        self._updateValueCallback = None
        self.seed = Seeds()
        self.enseed , self.key , self.nonce = Ctr.encrypt(self.seed)
        print("seed:",self.seed,"\nkey: ",self.key,"\nnonce: ",self.nonce)
        self._value = bytearray(self.enseed)

    def onReadRequest(self, offset, callback):
        print('EchoCharacteristic - %s - onReadRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        callback(Characteristic.RESULT_SUCCESS, self._value[offset:])

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        #資料寫入點
        #d = Ctr.decrypt(,self.key,self.nonce)  # data [seed+1][index][toAddr][Value][nonce][GasPrice][Gas]
        print(data,type(data))
        d = bytes(data)
        #解密後的seed+1
        dstr = Ctr.decrypt(d,self.key,self.nonce)
        d = dstr.decode()
        d = d.split(',')
        AuthenticationSeed , index , toAddr , Value , gethNonce , GasPrice , Gas = d[0],d[1],d[2],d[3],d[4],d[5],d[6]
        print("AuthenticationSeed: ",AuthenticationSeed)
        print("index: ",index)
        print("toAddr: ",toAddr)
        print("Value: ",Value)
        print("gethNonce: ",gethNonce)
        print("GasPrice: ",GasPrice)
        print("Gas: ", Gas)
        if int(self.seed)+1 == int(AuthenticationSeed):
            try:
                if index== "Txn":
                    txn = mt.EtherTxn(toAddr , int(Value) , int(gethNonce) , int(GasPrice) , int(Gas))
                    self._value = txn
            except:
                self._value = bytearray("args are wrong".encode('utf8'))
        else:
            self._value = bytearray("you're not the user")
        #self._value=bytearray(test_value.encode('utf8'))
        print('EchoCharacteristic - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        if self._updateValueCallback:
            print('EchoCharacteristic - onWriteRequest: notifying');
            self._updateValueCallback(self._value)
        callback(Characteristic.RESULT_SUCCESS)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        print('EchoCharacteristic - onSubscribe')
        self._updateValueCallback = updateValueCallback

    def onUnsubscribe(self):
        print('EchoCharacteristic - onUnsubscribe');
        self._updateValueCallback = None
