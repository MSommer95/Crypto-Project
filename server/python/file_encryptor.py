
import cryptography
from cryptography.fernet import Fernet

key = Fernet.generate_key()

file = open('user/key/key.key', 'wb') #wb = write bytes
file.write(key)
file.close()

#  Open the file to encrypt
with open('user/unencrypted/Rechnung_2012_08_051.pdf', 'rb') as f:
    data = f.read()

fernet = Fernet(key)
encrypted = fernet.encrypt(data)

# Write the encrypted file
with open('user/encrypted/Rechnung_2012_08_051.pdf.encrypted', 'wb') as f:
    f.write(encrypted)

file = open('user/key/key.key', 'rb') # rb = read bytes
keyToDecrypt = file.read()
file.close()

#  Open the file to decrypt
with open('user/encrypted/Rechnung_2012_08_051.pdf.encrypted', 'rb') as f:
    data = f.read()

fernet = Fernet(key)
decrypted = fernet.decrypt(data)

# Write the decrypted file
with open('user/unencrypted/Rechnung_2012_08_051.pdf.decrypted', 'wb') as f:
    f.write(decrypted)