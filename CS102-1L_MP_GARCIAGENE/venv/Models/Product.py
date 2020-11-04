from Helpers.ASCIIHelper import ASCIIHelper

class Product:
    def __init__(self):
        self.__productId = None # integer value
        self.__name = None # string name
        self.__inStock = None # integer number of product stock
        self.__unitPrice = None # price of a single item

    # getters setters
    def setProductId(self, id):
        self.__productId = id
    def getProductId(self):
        return self.__productId

    def setName(self, name):
        self.__name = name
    def getName(self):
        return self.__name

    def setStock(self, quantity):
        self.__inStock = quantity
    def getStock(self):
        return self.__inStock

    def setPrice(self, price):
        self.__unitPrice = price
    def getPrice(self):
        return self.__unitPrice

    def displaySummary(self):
        print(f"\t    Product ID:    #{self.__productId}")
        print(f"\t  Product Name:    {self.__name}")
        print(f"\tCurrent Stocks:    {self.__inStock} piece(s)")
        print(f"\t    Unit Price:    PHP {self.__unitPrice}")

    # for hash table
    def methodForHashTable(self):
        return self.getProductId()

    # static variable
    highestId = 0
    @staticmethod
    def getId():
        Product.highestId += 1
        return Product.highestId