from server.python.crypto_handler.caesar_cipher import CaesarCipher
from server.python.crypto_handler.distribution_analyzer import DistAnalyzer


class VigenereCipher:

    def __init__(self):
        self.modulus = 26

    def caesar_cipher_key(self, key):
        caesar_array = []
        for char in key:
            caesar_array.append(CaesarCipher((ord(char.lower()) - 97) % self.modulus))
        return caesar_array

    def cipher(self, text, key, option):
        crypt_text = ''
        i = 0
        while i < len(text):
            for caesar in self.caesar_cipher_key(key):
                if option == 'encrypt':
                    cipher_letter = caesar.encrypt(ord(text[i].lower()) - 97)
                else:
                    cipher_letter = caesar.decrypt(ord(text[i].lower()) - 97)
                crypt_text += chr(cipher_letter + 97)
                i += 1
                if i >= len(text):
                    break
        return crypt_text

    def guess_key_length(self, cipher_text):
        best_guess = 0
        split_value = 1

        while best_guess == 0 and split_value <= 50:
            best_guess = DistAnalyzer(cipher_text).kappa_test(split_value)
            split_value += 1

        return best_guess

    def crack_cipher(self, cipher_text):
        key_length = self.guess_key_length(cipher_text)
        key = ''
        if key_length > 0:
            for part in DistAnalyzer(cipher_text).split_cipher_text(key_length):
                max_value = ord(DistAnalyzer(part).letter_distribution()) - 97
                key += chr((max_value - (ord('e') - 97)) % 26 + 97)
            return key
        else:
            return 'Not able to crack'
