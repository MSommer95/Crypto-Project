import textwrap
from collections import Counter


class DistAnalyzer:

    def __init__(self, cipher_text):
        self.cipher_text = ''.join(cipher_text.lower().split())

    def letter_distribution(self):
        distribution = Counter(self.cipher_text)
        return max(distribution, key=lambda key: distribution[key])

    @staticmethod
    def coincidence_index(cipher_text):
        distribution = Counter(cipher_text)
        sum_coincidence_index = 0
        for dist in distribution:
            sum_coincidence_index += (distribution[dist] * (distribution[dist] - 1))
        if sum_coincidence_index == 0:
            return sum_coincidence_index
        coincidence_index = sum_coincidence_index / (len(cipher_text) * (len(cipher_text) - 1))
        return coincidence_index

    def split_cipher_text(self, split_value):
        split_chars_holder = ["" for _ in range(split_value)]
        cipher_parts = textwrap.wrap(self.cipher_text, split_value)
        for i in range(len(cipher_parts)):
            for j in range(split_value):
                if j < len(cipher_parts[i]):
                    split_chars_holder[j] += cipher_parts[i][j]
                else:
                    break
        return split_chars_holder

    def avg_coincidence_index_test(self, split_value):
        coincidence_index = 0
        split_chars_holder = self.split_cipher_text(split_value)
        for split_char in split_chars_holder:
            coincidence_index += DistAnalyzer.coincidence_index(split_char)
        coincidence_index /= len(split_chars_holder)
        if 0.064 < coincidence_index < 0.072:
            return split_value
        else:
            return 0
