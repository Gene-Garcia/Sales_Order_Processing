"""
Only used for the initial run
Initially populates the nodes hash tables
"""

from Models.Product import Product
from Models.CustomerInformation import CustomerInformation
from Models.CustomerOrder import CustomerOrder
from Models.SalesOrder import SalesOrder
from Models.ShipmentDetails import ShipmentDetails
from Models.JournalEntry import JournalEntry

from DataStructures.SinglyLinkedList import SinglyLinkedList
from DataStructures.HashTable import HashTable
from DataStructures.Queue import Queue

from Helpers.ASCIIHelper import ASCIIHelper

from datetime import date

class DataHelper:

    def __init__(self):
        # Singly linked list
        self.stockRecords = SinglyLinkedList()
        self.customerInformation = SinglyLinkedList()
        self.salesJournal = SinglyLinkedList()
        self.shippingLog = SinglyLinkedList()

        # additional for bill customer
        self.temporaryPendingFile = SinglyLinkedList()

        # Queue
        self.customerOrder = Queue() # informal
        self.openOrderFile = Queue() # to ship
        self.backOrderFile = Queue() # insufficient quantity
        self.salesOrderPendingFile = Queue() # shipped, not yet delivered

        # Hash table for search
        self.custInfoHashTable = HashTable(23)
        self.stockRecordsHashTable = HashTable(23)

    def __populateStockRecords(self):
        # stock records
        product1 = Product()
        product1.setName("ERGONOMIC CHAIR")
        product1.setProductId(Product.getId())
        product1.setStock(24)
        product1.setPrice(89300)

        product2 = Product()
        product2.setName("BASIC CHAIR")
        product2.setProductId(Product.getId())
        product2.setStock(10)
        product2.setPrice(28760)

        product3 = Product()
        product3.setName("SMALL CHAIR")
        product3.setProductId(Product.getId())
        product3.setStock(5)
        product3.setPrice(18760)

        self.stockRecords.insertNode(product1)
        self.stockRecords.insertNode(product2)
        self.stockRecords.insertNode(product3)

        self.stockRecordsHashTable.storeData(product1.methodForHashTable(), product1)
        self.stockRecordsHashTable.storeData(product2.methodForHashTable(), product2)
        self.stockRecordsHashTable.storeData(product3.methodForHashTable(), product3)

    def __populateCustomerInformation(self):
        # customer information and hash table
        customer1 = CustomerInformation()
        customer1.setCustomerId(CustomerInformation.getId())
        customer1.setName("Joe Tribbiani")
        customer1.setCreditLimit(230500)
        customer1.setAmountPayable(5000)

        customer2 = CustomerInformation()
        customer2.setCustomerId(CustomerInformation.getId())
        customer2.setName("Pheobe Buffay")
        customer2.setCreditLimit(500)
        customer2.setAmountPayable(12500)

        customer3 = CustomerInformation()
        customer3.setCustomerId(CustomerInformation.getId())
        customer3.setName("Sheldon Cooper")
        customer3.setCreditLimit(89000)
        customer3.setAmountPayable(0)

        customer4 = CustomerInformation()
        customer4.setCustomerId(CustomerInformation.getId())
        customer4.setName("Penny Hofstadter")
        customer4.setCreditLimit(230500)
        customer4.setAmountPayable(67000)

        self.customerInformation.insertNode(customer1)
        self.customerInformation.insertNode(customer2)
        self.customerInformation.insertNode(customer3)
        self.customerInformation.insertNode(customer4)

        self.custInfoHashTable.storeData(customer1.methodForHashTable(), customer1)
        self.custInfoHashTable.storeData(customer2.methodForHashTable(), customer2)
        self.custInfoHashTable.storeData(customer3.methodForHashTable(), customer3)
        self.custInfoHashTable.storeData(customer4.methodForHashTable(), customer4)

    def __populateCustomerOrder(self):
        # customer orders
        cusOrder1 = CustomerOrder()
        cusOrder1.setCustomerName("Penny Hofstadter")
        cusOrder1.setItems([3, 1])
        cusOrder1.setItemQuantities([20, 10])

        cusOrder2 = CustomerOrder()
        cusOrder2.setCustomerName("Joey Tribbiani")
        cusOrder2.setItems([2, 3])
        cusOrder2.setItemQuantities([5, 15])

        cusOrder3 = CustomerOrder()
        cusOrder3.setCustomerName("Sheldon Cooper")
        cusOrder3.setItems([3])
        cusOrder3.setItemQuantities([30])

        self.customerOrder.enqueue(cusOrder1)
        self.customerOrder.enqueue(cusOrder2)
        self.customerOrder.enqueue(cusOrder3)

    def __populateOpenOrderFile(self):
        today = date.today()

        so1 = SalesOrder()
        so1.setSalesOrderId(SalesOrder.getId())
        so1.setDateFilled(today)
        so1.setCustomerId(2)
        so1.setProductId(1)
        so1.setQuantity(10)
        so1.setShippingId(None)

        so2 = SalesOrder()
        so2.setSalesOrderId(SalesOrder.getId())
        so2.setDateFilled(today)
        so2.setCustomerId(1)
        so2.setProductId(3)
        so2.setQuantity(10)
        so2.setShippingId(None)

        so3 = SalesOrder()
        so3.setSalesOrderId(SalesOrder.getId())
        so3.setDateFilled(today)
        so3.setCustomerId(2)
        so3.setProductId(2)
        so3.setQuantity(10)
        so3.setShippingId(None)

        self.openOrderFile.enqueue(so1)
        self.openOrderFile.enqueue(so2)
        self.openOrderFile.enqueue(so3)

    def __populateBackOrderFile(self):
        today = date.today()

        so1 = SalesOrder()
        so1.setSalesOrderId(SalesOrder.getId())
        so1.setDateFilled(today)
        so1.setCustomerId(3)
        so1.setProductId(2)
        so1.setQuantity(50)
        so1.setShippingId(None)

        so2 = SalesOrder()
        so2.setSalesOrderId(SalesOrder.getId())
        so2.setDateFilled(today)
        so2.setCustomerId(2)
        so2.setProductId(1)
        so2.setQuantity(5)
        so2.setShippingId(None)

        so3 = SalesOrder()
        so3.setSalesOrderId(SalesOrder.getId())
        so3.setDateFilled(today)
        so3.setCustomerId(1)
        so3.setProductId(2)
        so3.setQuantity(15)
        so3.setShippingId(None)

        self.backOrderFile.enqueue(so1)
        self.backOrderFile.enqueue(so2)
        self.backOrderFile.enqueue(so3)

    def __populateSOPendingFile(self):
        today = date.today()

        so1 = SalesOrder()
        so1.setSalesOrderId(SalesOrder.getId())
        so1.setDateFilled(today)
        so1.setCustomerId(1)
        so1.setProductId(2)
        so1.setQuantity(50)

        s1 = ShipmentDetails()
        s1.setShippingId(ShipmentDetails.getId())
        s1.setDateShipped(today)
        s1.setDateDelivered(None)

        so1.setShippingId(s1.getShippingId())

        so2 = SalesOrder()
        so2.setSalesOrderId(SalesOrder.getId())
        so2.setDateFilled(today)
        so2.setCustomerId(2)
        so2.setProductId(2)
        so2.setQuantity(50)

        s2 = ShipmentDetails()
        s2.setShippingId(ShipmentDetails.getId())
        s2.setDateShipped(today)
        s2.setDateDelivered(None)

        so2.setShippingId(s2.getShippingId())

        self.salesOrderPendingFile.enqueue(so1)
        self.shippingLog.insertNode(s1)
        self.salesOrderPendingFile.enqueue(so2)
        self.shippingLog.insertNode(s2)

        self.temporaryPendingFile.insertNode(so1)
        self.temporaryPendingFile.insertNode(so2)

    def __populateSalesJournal(self):
        today = date.today()

        so1 = SalesOrder()
        so1.setSalesOrderId(SalesOrder.getId())
        so1.setDateFilled(today)
        so1.setCustomerId(3)
        so1.setProductId(1)
        so1.setQuantity(10)

        s1 = ShipmentDetails()
        s1.setShippingId(ShipmentDetails.getId())
        s1.setDateShipped(today)
        s1.setDateDelivered(None)

        so1.setShippingId(s1.getShippingId())

        j1 = JournalEntry()
        j1.setJournalId(JournalEntry.getId())
        j1.setSalesOrder(so1)
        j1.setDateCompleted(s1.getDateShipped())

        so2 = SalesOrder()
        so2.setSalesOrderId(SalesOrder.getId())
        so2.setDateFilled(today)
        so2.setCustomerId(1)
        so2.setProductId(3)
        so2.setQuantity(24)

        s2 = ShipmentDetails()
        s2.setShippingId(ShipmentDetails.getId())
        s2.setDateShipped(today)
        s2.setDateDelivered(None)

        so2.setShippingId(s2.getShippingId())

        j2 = JournalEntry()
        j2.setJournalId(JournalEntry.getId())
        j2.setSalesOrder(so2)
        j2.setDateCompleted(s2.getDateShipped())

        self.salesJournal.insertNode(j1)
        self.salesJournal.insertNode(j2)

    def populate(self):
        self.__populateStockRecords()
        self.__populateCustomerInformation()
        self.__populateCustomerOrder()
        self.__populateOpenOrderFile()
        self.__populateBackOrderFile()
        self.__populateSOPendingFile()
        self.__populateSalesJournal()
