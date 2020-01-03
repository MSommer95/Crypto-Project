from server.python.crypto_handler.cipher_helper import CipherHelper
from server.python.crypto_handler.distribution_analyzer import DistAnalyzer


class CaesarCipher:

    def __init__(self, shift):
        self.shift = int(shift)
        self.modulus = 26

    def encrypt(self, letter):
        return (letter + self.shift) % self.modulus

    def decrypt(self, letter):
        return (letter - self.shift) % self.modulus

    def shift_letter(self, letter, option):
        ascii_position = CipherHelper.case_distinction(letter)
        letter_number_before = ord(letter) - ascii_position
        if option == 'encrypt':
            return chr(self.encrypt(letter_number_before) + ascii_position)
        else:
            return chr(self.decrypt(letter_number_before) + ascii_position)

    def cipher(self, message, option):
        words = message.split(' ')
        for i in range(len(words)):
            letters = list(CipherHelper.remove_special_chars(words[i]))
            for j in range(len(letters)):
                letters[j] = self.shift_letter(letters[j], option)
            words[i] = ''.join(letters)
        return ''.join(words)

    def crack_cipher(self, cipher_text):
        analyzer = DistAnalyzer(cipher_text)
        pop_letter = analyzer.letter_distribution()
        shift = (ord(pop_letter) - ord('e')) % self.modulus
        return shift
