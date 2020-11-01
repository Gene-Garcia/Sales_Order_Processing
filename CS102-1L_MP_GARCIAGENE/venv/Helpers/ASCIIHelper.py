class ASCIIHelper:
    @staticmethod
    def toASCII(text):
        # using list comprehension
        # traverse each character in text
        data = [ord(character) for character in text]
        # add all ascii of each character
        sumOfCharacters = sum(data)
        return sumOfCharacters