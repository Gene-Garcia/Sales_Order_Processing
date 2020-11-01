
class InputHelper:

    @staticmethod
    def stringInput(message):
        userInput = None
        while True:
            userInput = input("\n\t" + message + " >>").strip()
            if (userInput != ""):
                break
            print("\tInput empty")
        return userInput

    @staticmethod
    def integerInput(message):
        userInput = None
        while True:
            try:
                userInput = int(input("\n\t" + message + " >>").strip())
                break
            except:
                print("\tInvalid input, integers only.")
                continue
        return userInput

    @staticmethod
    def floatInput(message):
        userInput = None
        while True:
            try:
                userInput = float(input("\n\t" + message + " >>").strip())
                break
            except:
                print("\tInvalid input, decimals only.")
        return userInput