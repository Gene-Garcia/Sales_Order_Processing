class CustomerOrder:
    def __init__(self):
        self.__items = [] # integers
        self.__itemQuantity = [] # integers
        self.__customerId = None # integer customer id

    # getters setters
    def setItems(self, items):
        self.__items = items
    def getItems(self):
        return self.__items

    def setItemQuantities(self, quantities):
        self.__itemQuantity = quantities
    def getItemQuantities(self):
        return self.__itemQuantity

    def setCustomerId(self, customerName):
        self.__customerId = customerName
    def getCustomerId(self):
        return self.__customerId

    # static variable
    highestId = 0
    @staticmethod
    def getId():
        CustomerOrder.highestId += 1
        return CustomerOrder.highestId