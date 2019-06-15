from web3.auto import w3
import sys
from mnemonic import *
import binascii
import subprocess
import os
from os import path
import json

class wallet:
    def __init__(self):
        pass
    def PrivateKey(self):#私鑰
        keyfile =open("./keystore/"+os.listdir("./keystore")[0])
        encrypted_key = keyfile.read()
        private_key = w3.eth.account.decrypt(encrypted_key,self.password())
        return w3.toHex(private_key)
    def PublicKey(self):#公鑰
        keyfile =open("./keystore/"+os.listdir("./keystore")[0])
        encrypted_key = keyfile.read()
        return  w3.toChecksumAddress(encrypted_key.split(',')[0].split(':')[1].strip('"'))

    def password(self): #取得使用的當時輸入的密碼
        try:
            fp = open("./password/passwd.txt",'r')
            passwd = fp.read()
            fp.close()
            return passwd
        except:
            print("No accounts")

    def newAccount(self,passwd):# 新增錢包 Only one times
        if not path.exists("./password"): #確認存放password的資料夾是否存在
            os.makedirs("password")
        if not path.exists("./password/passwd.txt"): #確認存放password的文件是否存在
            os.mknod("./password/passwd.txt")
        fp = open("./password/passwd.txt",'w') #開啟文建檔 存起來
        fp.writelines(passwd)
        fp.close()
        subprocess.call(['sudo', 'geth', '--datadir', './' ,'account','new','--password','./password/passwd.txt'])

    # user input their password
    def Mnemonics(self):#轉24助憶詞
        data = binascii.unhexlify(self.PrivateKey().split('x')[1])
        m = Mnemonic("english")
        return m.to_mnemonic(data)

class makeTxn:
        import json
        from Wallet import wallet
        wt = wallet()
        def EtherTxn(to_Address ,value , nonce ,gasPrice,gas):#乙太幣交易
                privateKey = wt.PrivateKey()
                address = w3.toChecksumAddress(wt.PublicKey())
                to_Address = w3.toChecksumAddress(to_Address)
                txn = {#gas * price + value really means MAXGas * price.
                 'from':address,
                 'to':to_Address,
                 'value':int(value),
                 'gas':int(gas),
                 'gasPrice':int(gasPrice),  # = gas*price+value
                 'nonce':int(nonce),
                }
                # 簽名 送tmp回去給手機
                signed_txn = w3.eth.account.signTransaction(txn,private_key=privateKey)
                tmp  =signed_txn.rawTransaction
                # 加密存下來
                txhasg  = w3.toHex(w3.sha3(signed_txn.rawTransaction))
                return tmp

        def Token_Txn(to_addr,value,nonce):#Token交易
                ABI = json.loads('[{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"tokens","type":"uint256"}],"name":"approve","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"buy","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[],"name":"delContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"price","type":"uint256"}],"name":"setPrice","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"tokens","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"tokens","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"tokens","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"tokenOwner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"tokens","type":"uint256"}],"name":"Approval","type":"event"},{"constant":true,"inputs":[{"name":"tokenOwner","type":"address"},{"name":"spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowed","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"tokenOwner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balances","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"buyPrice","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"weiToEther","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]')
                Token = w3.eth.contract(
                    w3.toChecksumAddress('0xdaFc7DC630DD0974d6d034727cb94Af5A2287b60'),# deploy the contract /contractaddr
                    abi=ABI
                )
                to_addr = w3.toChecksumAddress(to_addr)
                privateKey = wt.PrivateKey()
                sender = w3.toChecksumAddress(wt.PublicKey())
                txn1 = {'gas':70000,'gasPrice':1,'nonce':int(nonce),'from':sender}
                txn2 = Token.functions.transfer(to_addr,int(value)).buildTransaction(txn1)
                signed_txn =  w3.eth.account.signTransaction(txn2,private_key=privateKey)
                tmp = signed_txn.rawTransaction
                return tmp
