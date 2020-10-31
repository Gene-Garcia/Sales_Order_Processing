class Product:
    def __init__(self):
        self.__productId = None # integer value
        self.__name = None # string name
        self.__inStock = None # integer number of product stock

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

    # static variable
    highestId = 0
    @staticmethod
    def getId():
        Product.highestId += 1
        return Product.highestId