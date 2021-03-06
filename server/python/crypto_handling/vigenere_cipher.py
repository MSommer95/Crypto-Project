from server.python.crypto_handling.caesar_cipher import CaesarCipher
from server.python.crypto_handling.cipher_helper import CipherHelper
from server.python.crypto_handling.distribution_analyzer import DistAnalyzer


class VigenereCipher:

    def __init__(self):
        self.modulus = 26

    def caesar_cipher_key(self, key):
        caesar_array = []
        for char in key:
            caesar_array.append(CaesarCipher(ord(char.lower()) - 97))
        return caesar_array

    def cipher(self, text, key, option):
        crypt_text = ''
        i = 0
        caesar_key = self.caesar_cipher_key(key)
        while i < len(text):
            for caesar in caesar_key:
                ascii_position = CipherHelper.case_distinction(text[i])
                if option == 'encrypt':
                    cipher_letter = caesar.encrypt(ord(text[i]) - ascii_position)
                else:
                    cipher_letter = caesar.decrypt(ord(text[i]) - ascii_position)
                crypt_text += chr(cipher_letter + ascii_position)
                i += 1
                if i >= len(text):
                    break
        return crypt_text

    def guess_key_length(self, cipher_text):
        guess_length = 0
        key_length = 1
        while guess_length == 0 and key_length <= 100:
            guess_length = DistAnalyzer(cipher_text).avg_coincidence_index_test(key_length)
            key_length += 1
        return guess_length

    def crack_cipher(self, cipher_text):
        key_length = self.guess_key_length(cipher_text)
        key = ''
        if key_length > 0:
            for part in DistAnalyzer(cipher_text).split_cipher_text(key_length):
                max_value = ord(DistAnalyzer(part).letter_distribution()) - 97
                key += chr((max_value - (ord('e') - 97)) % 26 + 97)
            return key
        else:
            return 'Not able to crack or key is longer then 100 characters'
