class ShipmentDetails:
    def __init__(self):
        self.__shippingId = None # integer value
        self.__dateShipped = None # date order leaves
        self.__dateDelivered = None # date value order recieved by customer

    # getters setters
    def setShippingId(self, id):
        self.__shippingId = id
    def getShippingId(self):
        return self.__shippingId

    def setDateShipped(self, date):
        self.__dateShipped = date
    def getDateShipped(self):
        return self.__dateShipped

    def setDateDelivered(self, date):
        self.__dateDelivered = date
    def getDateDelivered(self):
        return self.__dateDelivered