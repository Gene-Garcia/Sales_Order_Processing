"""
Only used for the initial run
Initially populates the nodes hash tables
"""

class DataHelper:

    # Singly linked list
    stockRecords = None
    customerInformation = None
    salesJournal = None
    shippingLog = None

    # Queue
    customerOrder = None # informal
    openOrderFile = None # to ship
    backOrderFile = None # insufficient quantity
    salesOrderPendingFile = None # shipped, not yet delivered

    # Hash table for search
    custInfoHashTable = None
    stockRecordsHashTable = None

    @staticmethod
    def populate():
        pass