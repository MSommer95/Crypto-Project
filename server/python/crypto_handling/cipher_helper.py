class CipherHelper:

    @staticmethod
    def remove_special_chars(message):
        return ''.join(e for e in message if e.isalnum() and not e.isdigit())

    @staticmethod
    def case_distinction(letter):
        return 97 if ord(letter) >= 97 else 65
