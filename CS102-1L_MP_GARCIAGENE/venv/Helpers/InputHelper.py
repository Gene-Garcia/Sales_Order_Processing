
class InputHelper:

    @staticmethod
    def stringInput(message):
        userInput = None
        while True:
            userInput = input("\t" + message + " >>").strip()
            if (userInput != ""):
                break
            print("\tInput empty")
        return userInput

    """@staticmethod
    def integerInput(message):
        userInput = None
        while True:
            try:
                userInput = int(input("\t" + message + " >>").strip())
                break
            except:
                print("\tInvalid input, integers only.")
        return userInput"""

    @staticmethod
    def integerInput(message, min):
        userInput = None
        while True:
            try:
                userInput = int(input("\t" + message + " >>").strip())

                if userInput >= min:
                    break
                else:
                    print("\tMinimum value is", min)
            except:
                print("\tInvalid input, integers only.")
        return userInput

    @staticmethod
    def integerInputWithChoices(message, choices = []):
        userInput = None
        while True:
            try:
                userInput = int(input(f"\t{message} - {choices} >>").strip())

                if userInput in choices:
                    break
                else:
                    print("\tInput not from choices.")
            except:
                print("\tInvalid input, integers only.")
        return userInput

    """@staticmethod
    def floatInput(message):
        userInput = None
        while True:
            try:
                userInput = float(input("\t" + message + " >>").strip())
                break
            except:
                print("\tInvalid input, decimals only.")
        return userInput"""

    @staticmethod
    def floatInput(message, min):
        userInput = None
        while True:
            try:
                userInput = float(input("\t" + message + " >>").strip())

                if userInput >= min:
                    break
                else:
                    print("\tMinimum value is", min)
            except:
                print("\tInvalid input, decimal only.")
        return userInput