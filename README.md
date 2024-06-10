RC6Block
================

Easy to use implementation of RC6 encryption in python.

Tested with a cpp implementation.

## Info

* Block size : 32 bytes with 4 chunks.

* Key size : 16 bytes

* Rounds: 12

## Features

* In cryptography, RC6 (Rivest Cipher 6) is a symmetric key block cipher derived from RC5. 

* It was designed by Ron Rivest, Matt Robshaw, Ray Sidney, and Yiqun Lisa Yin

* It was designed to meet the requirements of the Advanced Encryption Standard (AES) competition. 

* It is a proprietary algorithm, patented by RSA Security.

## Functions

The main class is rc6, the constructor accepts the encryption key. There are functions in this class:

```
change_key() -> None

return data -> None
```
Used to change the key after creating an instance of the class.

```
encrypt_data(plaintext) -> str, int

return data -> (encrypted text, length_of_plaintext)
```
Used to encrypt plaintext with key.

```
decrypt_data(ciphertext, length_of_plaintext) -> str

return data -> plaintext
```
