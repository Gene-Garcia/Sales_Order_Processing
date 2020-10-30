class JournalEntry:
    def __init__(self):
        self.__journalId = None # integer value
        self.__salesOrder = None # sales order model object
        self.__dateEntry = None # date value

    # getters setters
    def setJournalId(self, id):
        self.__journalId = id
    def getJournalId(self):
        return self.__journalId

    def setSalesOrder(self, model):
        self.__salesOrder = model
    def getSalesOrder(self):
        return self.__salesOrder

    def setDateEntry(self, date):
        self.__dateEntry = date
    def getDateEntry(self):
        return self.__dateEntry