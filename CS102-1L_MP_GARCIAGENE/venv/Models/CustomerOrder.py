class CustomerOrder:
    def __init__(self):
        self.__items = [] # integers
        self.__itemQuantity = [] # integers
        self.__customerName = None # string name

    # getters setters
    def setItems(self, items):
        self.__items = items
    def getItems(self):
        return self.__items

    def setItemQuantities(self, quantities):
        self.__itemQuantity = quantities
    def getItemQuantities(self):
        return self.__itemQuantity

    def setCustomerName(self, customerName):
        self.__customerName = customerName
    def getCustomerName(self):
        return self.__customerName