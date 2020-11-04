class SalesOrder:
    def __init__(self):
        self.__salesOrderId = None # integer value
        self.__customerId = None # integer value, foreign
        self.__productId = None # integer value, foreign
        self.__quantity = None # integer value
        self.__dateFilled = None # date value
        self.__shippingId = None # integer value, foreign key

    # getters setters
    def setSalesOrderId(self, id):
        self.__salesOrderId = id
    def getSalesOrderId(self):
        return self.__salesOrderId

    def setCustomerId(self, id):
        self.__customerId = id
    def getCustomerId(self):
        return self.__customerId

    def setProductId(self, id):
        self.__productId = id
    def getProductId(self):
        return self.__productId

    def setQuantity(self, quantity):
        self.__quantity = quantity
    def getQuantity(self):
        return self.__quantity

    def setDateFilled(self, date):
        self.__dateFilled = date
    def getDateFilled(self):
        return self.__dateFilled

    def setShippingId(self, id):
        self.__shippingId = id
    def getShippingId(self):
        return self.__shippingId

    def displaySummary(self):
        print(f"\tSales Order ID:    #{self.__salesOrderId}")
        print(f"\t   Date Filled:    {self.__dateFilled}")
        print(f"\t   Customer ID:    #{self.__customerId}")
        print(f"\t    Product ID:    #{self.__productId}")
        print(f"\t      Quantity:    {self.__quantity} piece(s)")
        print(f"\t   Shipping ID:    #{self.__shippingId}")

    # for delete
    def methodForDelete(self):
        return self.__salesOrderId

    # static variable
    highestId = 0
    @staticmethod
    def getId():
        SalesOrder.highestId += 1
        return SalesOrder.highestId
