class JournalEntry:
    def __init__(self):
        self.__journalId = None # integer value
        self.__salesOrder = None # sales order model object
        self.__dateCompleted = None # date value
        self.__paid = False # boolean
        self.__datePaid = None # date value

    # getters setters
    def setJournalId(self, id):
        self.__journalId = id
    def getJournalId(self):
        return self.__journalId

    def setSalesOrder(self, model):
        self.__salesOrder = model
    def getSalesOrder(self):
        return self.__salesOrder

    def setDateCompleted(self, date):
        self.__dateCompleted = date
    def getDateCompleted(self):
        return self.__dateCompleted

    def setPaymentStatus(self, status):
        self.__paid = status
    def getPaymentStatus(self):
        return self.__paid

    def setDatePaid(self, date):
        self.__datePaid = date
    def getDatePaid(self):
        return self.__datePaid

    def displaySummary(self):
        print("\tJournal Id", self.__journalId)
        print("\tDate Completed", self.__dateCompleted)
        if self.__paid:
            print("\tSales Order Payment Status is paid")
            print("\tDate Paid", self.__datePaid)
        else:
            print("\tSales Order Payment Status is unpaid")
        print("\t\tSales Order Summary")
        self.__salesOrder.displaySummary()

    # for sort
    def methodForSort(self):
        return self.getDateCompleted()

    # static variable
    highestId = 0

    @staticmethod
    def getId():
        JournalEntry.highestId += 1
        return JournalEntry.highestId