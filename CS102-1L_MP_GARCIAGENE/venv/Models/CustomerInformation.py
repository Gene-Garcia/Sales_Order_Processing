from Helpers.ASCIIHelper import ASCIIHelper

class CustomerInformation:
    def __init__(self):
        self.__customerId = None # int value
        self.__name = None # string value
        self.__amountPayable = None # float value
        self.__creditLimit = None # float value

    # getters settesr
    def setCustomerId(self, id):
        self.__customerId = id
    def getCustomerId(self):
        return self.__customerId

    def setName(self, name):
        self.__name = name
    def getName(self):
        return self.__name

    def setAmountPayable(self, amount):
        self.__amountPayable = amount
    def getAmountPayable(self):
        return self.__amountPayable

    def setCreditLimit(self, limit):
        self.__creditLimit = limit
    def getCreditLimit(self):
        return self.__creditLimit

    def displaySummary(self):
        print(f"\t   Customer ID:    #{self.__customerId}")
        print(f"\t          Name:    {self.__name}")
        print(f"\t  Credit Limit:    PHP {self.__creditLimit}")
        print(f"\tAmount Payable:    PHP {self.__amountPayable}")

    # for sort
    def methodForSort(self):
        return self.getName()

    # for hash table
    def methodForHashTable(self):
        return self.getCustomerId()

    # static variable
    highestId = 0
    @staticmethod
    def getId():
        CustomerInformation.highestId += 1
        return CustomerInformation.highestId