class JournalEntry:
    def __init__(self):
        self.__journalId = None # integer value
        self.__salesOrder = None # sales order model object
        self.__dateCompleted = None # date value

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

    # for sort
    def methodForSort(self):
        return self.getDateCompleted()

    # static variable
    highestId = 0

    @staticmethod
    def getId():
        JournalEntry.highestId += 1
        return JournalEntry.highestId