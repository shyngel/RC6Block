from rc6 import RC6 as rc6

if __name__ == "__main__":
    key = 'random_key_here'
    new_key = 'second_random_key'

    ciphertext = 'something you need to encrypt'
    
    service = rc6(key)
    
    print('\nSTRING EXAMPLE\n')

    encrypted_data, c = service.encrypt_data(ciphertext)
    print(encrypted_data)
    
    decrypted_data = service.decrypt_data(encrypted_data, c)
    print(decrypted_data)

    print('\nBYTEARRAY EXAMPLE\n')

    service.change_key(new_key)

    cipherbytes = bytearray('\x79\x80\x12\x79\x80\x12\x79\x80\x12\x79\x80\x12\x79\x80\x12',encoding='UTF-8')

    encrypted_data, c = service.encrypt_data(cipherbytes)
    print(encrypted_data)
    
    decrypted_data = service.decrypt_data(encrypted_data, c)
    print(decrypted_data)
