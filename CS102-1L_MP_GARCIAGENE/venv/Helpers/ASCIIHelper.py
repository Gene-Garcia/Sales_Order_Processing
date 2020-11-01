class ASCIIHelper:
    @staticmethod
    def toASCII(text):
        # using list comprehension
        # traverse each character in text
        data = [ord(character) for character in text]
        print(data)