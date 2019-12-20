from collections import Counter


class DistAnalyzer:

    def __init__(self, cipher_text):
        self.cipher_text = ''.join(cipher_text.lower().split())

    def letter_distribution(self):
        distribution = Counter(self.cipher_text)
        return max(distribution, key=lambda key: distribution[key])
