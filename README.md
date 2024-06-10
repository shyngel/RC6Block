RC6Block
================
	
Easy to use implementation of RC6 encryption in python.

Tested with a cpp implementation.

## Info

* Block size : 32 bytes with 4 chunks.

* Key size : 16 bytes

* Rounds: 12

# To run this program, you need to have the following dependencies installed:

* Python 3.x
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
