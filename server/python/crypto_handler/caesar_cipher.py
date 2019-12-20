from server.python.crypto_handler.distribution_analyzer import DistAnalyzer


def case_distinction(letter):
    return 97 if ord(letter) >= 97 else 65


def remove_special_chars(message):
    return ''.join(e for e in message if e.isalnum())


class CaesarCipher:

    def __init__(self):
        self.shift = 0
        self.modulus = 26

    def encrypt(self, letter):
        return (letter + self.shift) % self.modulus

    def decrypt(self, letter):
        return (letter - self.shift) % self.modulus

    def shift_letter(self, letter, option):
        ascii_position = case_distinction(letter)
        letter_number_before = ord(letter) - ascii_position
        if option == 'encrypt':
            return chr(self.encrypt(letter_number_before) + ascii_position)
        else:
            return chr(self.decrypt(letter_number_before) + ascii_position)

    def cipher(self, message, option, shift):
        self.shift = shift
        words = message.split(' ')
        for i in range(len(words)):
            letters = list(remove_special_chars(words[i]))
            for j in range(len(letters)):
                letters[j] = self.shift_letter(letters[j], option)
            words[i] = ''.join(letters)
        return ' '.join(words)

    def crack_cipher(self, cipher_text):
        analyzer = DistAnalyzer(cipher_text)
        pop_letter = analyzer.letter_distribution()
        shift = (ord(pop_letter) - ord('e')) % self.modulus
        return shift
