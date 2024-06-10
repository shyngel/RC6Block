import os
class RC6:
    def __init__(self,key) -> None:
        self.__helper = _helper()
        v = self.__check_key_validity(key)
        key += '\0' * v
        self.__key = self.__prepare_key(key)
    def __random_binary_num(self, block_size=4):
        return self.__helper.bytes_to_bits_binary(os.urandom(block_size))
    def __decrypt(self, block: str):
        encoded = self.__block_to_uint(block)
        orgi = []
        cipher = []
        if(len(encoded) < 5):
            A = int(encoded[0],2)
            B = int(encoded[1],2)
            C = int(encoded[2],2)
            D = int(encoded[3],2)
            cipher.append(A)
            cipher.append(B)
            cipher.append(C)
            cipher.append(D)
            r=12
            modulo = 2**32
            lgw = 5
            C = (C - self.__key[2*r+3])%modulo
            A = (A - self.__key[2*r+2])%modulo
            for j in range(1,r+1):
                i = r+1-j
                (A, B, C, D) = (D, A, B, C)
                u_temp = (D*(2*D + 1))%modulo
                u = self.__helper.rol(u_temp,lgw,32)
                t_temp = (B*(2*B + 1))%modulo 
                t = self.__helper.rol(t_temp,lgw,32)
                tmod=t%32
                umod=u%32
                C = (self.__helper.ror((C-self.__key[2*i+1])%modulo,tmod,32)  ^u)  
                A = (self.__helper.ror((A-self.__key[2*i])%modulo,umod,32)   ^t) 
            D = (D - self.__key[1])%modulo 
            B = (B - self.__key[0])%modulo
            orgi.append(A)
            orgi.append(B)
            orgi.append(C)
            orgi.append(D)
        return cipher,orgi
    def __encrypt(self, block: str):
        if len(block) > 16:
            raise Exception(f"Block size is {len(block)} bytes. Expected less than 16.")
        encoded = self.__block_to_uint(block)
        if len(encoded) < 4:
            while len(encoded) != 4:
                encoded.append(self.__random_binary_num())
        cipher = []
        orgi = []
        if(len(encoded) < 5):
            A = int(encoded[0],2)
            B = int(encoded[1],2)
            C = int(encoded[2],2)
            D = int(encoded[3],2)
            orgi.append(A)
            orgi.append(B)
            orgi.append(C)
            orgi.append(D)
            r=12
            modulo = 2**32
            lgw = 5
            B = (B + self.__key[0])%modulo
            D = (D + self.__key[1])%modulo 
            for i in range(1,r+1):
                t_temp = (B*(2*B + 1))%modulo 
                t = self.__helper.rol(t_temp,lgw,32)
                u_temp = (D*(2*D + 1))%modulo
                u = self.__helper.rol(u_temp,lgw,32)
                tmod=t%32
                umod=u%32
                A = (self.__helper.rol(A^t,umod,32) + self.__key[2*i])%modulo 
                C = (self.__helper.rol(C^u,tmod,32) + self.__key[2*i+ 1])%modulo
                (A, B, C, D)  =  (B, C, D, A)
            A = (A + self.__key[2*r + 2])%modulo 
            C = (C + self.__key[2*r + 3])%modulo    
            cipher.append(A)
            cipher.append(B)
            cipher.append(C)
            cipher.append(D)
        return orgi,cipher
    def __block_to_uint(self,sentence: str):
        
        encoded = []
        i = 0
        r = ''
        while i < len(sentence):
            n = self.__helper.bytes_to_bits_binary(sentence[i:i+4])
            encoded.append(n)
            i += 4
        return encoded
    def __uint_to_bytearray(self,nums: list):
        l_tx = []
        for i in nums:
            s = bin(i)[2:]
            s = '0' * (32 - len(s)) + s
            A = s[0:8]
            B = s[8:16]
            C = s[16:24]
            D = s[24:32]
            l_tx.append(int(D,2))
            l_tx.append(int(C,2))
            l_tx.append(int(B,2))
            l_tx.append(int(A,2))
        return l_tx
    def __prepare_key(self, key):
        r=12
        w=32
        modulo = 2**32
        s=(2*r+4)*[0]
        s[0]=0xB7E15163
        for i in range(1,2*r+4):
            s[i]=(s[i-1]+0x9E3779B9)%(2**w)
        encoded = self.__block_to_uint(key)
        enlength = len(encoded)
        l = []
        for i in encoded:
            l.append(int(i,2))
        
        v = 3*max(enlength,2*r+4)
        A=B=i=j=0
        
        for index in range(0,v):
            A = s[i] = self.__helper.rol((s[i] + A + B)%modulo,3,32)
            B = l[j] = self.__helper.rol((l[j] + A + B)%modulo,(A+B)%32,32) 
            i = (i + 1) % (2*r + 4)
            j = (j + 1) % (int(128 / 32))
        return s
    def __check_key_validity(self, key):
        if len(key) < 16:
            return (16-len(key))
        if len(key) > 2048:
            raise Exception("Key is too long.")
        return 0
    def change_key(self,new_key: str):
        self.__key = self.__prepare_key(new_key)
    def decrypt_data(self, data,length):
        ind = 0
        all_text = bytearray()
        a = 0 
        while ind < len(data):
            a = min(len(data) - ind, 16)
            cipher,orgi = self.__decrypt(data[ind:ind+a])
            all_text.extend(self.__uint_to_bytearray(orgi))
            ind+=a
        return all_text[:length]
    def encrypt_data(self, data):
        ind = 0
        all_text = bytearray()
        while ind < len(data):
            a = min(len(data) - ind, 16)
            cipher,orgi = self.__encrypt(data[ind:ind+a])
            all_text.extend(self.__uint_to_bytearray(orgi))
            ind+=a
        return all_text, ind
    

class _helper:
    def __init__(self) -> None:
        pass
    def ror(self,x, n, bits = 32):
        mask = (2**n) - 1
        mask_bits = x & mask
        return (x >> n) | (mask_bits << (bits - n))
    def rol(self,x, n, bits = 32):
        return self.ror(x, bits - n,bits)
    def bytes_to_bits_binary(self,byte_data):
        if isinstance(byte_data,str):
            temp = byte_data
            byte_data = bytearray()
            for i in temp:
                byte_data.append(ord(i))  
        bits_data = bin(int.from_bytes(byte_data, byteorder='little'))[2:]
        return bits_data