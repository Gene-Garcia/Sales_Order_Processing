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
from Helpers.PrimeHelper import PrimeHelper

from datetime import date
import datetime


class DataRepository:

    def __init__(self):
        # Singly linked list
        self.stockRecords = SinglyLinkedList()
        self.customerInformation = SinglyLinkedList()
        self.salesJournal = SinglyLinkedList()
        self.shippingLog = SinglyLinkedList()

        # additional for bill customer
        # used to get the sales order that will be recorded in the sales journal
        self.temporaryPendingFile = SinglyLinkedList()

        # Queue
        self.customerOrder = Queue()  # informal
        self.openOrderFile = Queue()  # to ship
        self.backOrderFile = Queue()  # insufficient quantity
        self.salesOrderPendingFile = Queue()  # shipped, not yet delivered. If delivered, dequeued from the queue

        # Hash table for search
        self.custInfoHashTable = None #HashTable(23)
        self.stockRecordsHashTable = None #HashTable(23)
        # additional hash table
        self.journalHashTable = None #HashTable(23)
        self.shippingLogHashTable = None #HashTable(23)

        self.__DELIMETER = "%20"
        # file names
        self.__CUSTOMER_RECORDS = "customer.txt" #/
        self.__STOCK_RECORDS = "stocks.txt" #/

        self.__CUSTOMER_ORDERS = "customerOrders.txt" #/
        self.__OPEN_ORDER = "openOrders.txt" #/
        self.__BACK_ORDER = "backOrders.txt" #/

        self.__PENDING_ORDER = "pendingOrders.txt" #/
        self.__SHIPPING_LOG = "shippingLog.txt" #/

        self.__SALES_JOURNAL = "salesJournal.txt"   # contains sales order

    def populate(self):
        self.readRecords()

    def readRecords(self):
        # customer records
        try:
            with open(self.__CUSTOMER_RECORDS, "r") as file:
                datas = file.read().split("\n")
                # instantiate hash table
                self.custInfoHashTable = HashTable(PrimeHelper.findNearestPrime(len(datas)+20))

                for line in datas:
                    if line == '':
                        break
                    # customerId, name, amountPayable, creditLimit
                    line = line.split(self.__DELIMETER)
                    customer = CustomerInformation()
                    customer.setCustomerId(int(line[0]))
                    customer.setName(line[1])
                    customer.setAmountPayable(float(line[2]))
                    customer.setCreditLimit(float(line[3]))

                    # updated highest id
                    if customer.getCustomerId() >= CustomerInformation.highestId:
                        CustomerInformation.highestId = customer.getCustomerId()

                    # append to records
                    self.customerInformation.insertNode(customer)
                    self.custInfoHashTable.storeData(customer.methodForHashTable(), customer)
        except FileNotFoundError:
            file = open(self.__CUSTOMER_RECORDS, "x")
            file.close()

        # stock records
        try:
            with open(self.__STOCK_RECORDS, "r") as file:
                datas = file.read().split("\n")
                # instantiate hash table
                self.stockRecordsHashTable = HashTable(PrimeHelper.findNearestPrime(len(datas)+20))

                for line in datas:
                    if line == '':
                        break
                    # productId, name, stock count, price
                    line = line.split(self.__DELIMETER)
                    product = Product()
                    product.setProductId(int(line[0]))
                    product.setName(line[1])
                    product.setStock(int(line[2]))
                    product.setPrice(float(line[3]))

                    # updated highest id
                    if product.getProductId() >= Product.highestId:
                        Product.highestId = product.getProductId()

                    # append to records
                    self.stockRecords.insertNode(product)
                    self.stockRecordsHashTable.storeData(product.methodForHashTable(), product)
        except FileNotFoundError:
            file = open(self.__STOCK_RECORDS, "x")
            file.close()

        # customer orders
        try:
            with open(self.__CUSTOMER_ORDERS, "r") as file:
                datas = file.read().split("\n")

                for line in datas:
                    if line == '':
                        break
                    # items[int], itemQuantitites[int], customerId
                    line = line.split(self.__DELIMETER)
                    # convert the string representation to list
                    # the data are still string, we need to use map()
                    line[0] = line[0].strip('][').split(', ')
                    line[1] = line[1].strip('][').split(', ')

                    customerOrder = CustomerOrder()
                    customerOrder.setItems(list(map(int, line[0])))
                    customerOrder.setItemQuantities(list(map(int, line[1])))
                    customerOrder.setCustomerId(int(line[2]))

                    # append to records
                    self.customerOrder.enqueue(customerOrder)
        except FileNotFoundError:
            file = open(self.__CUSTOMER_ORDERS, "x")
            file.close()

        # open order file
        try:
            with open(self.__OPEN_ORDER, "r") as file:
                datas = file.read().split("\n")

                for line in datas:
                    if line == '':
                        break
                    # salesOrderId, customerId, productId, quantity, dateFilled, shippingId
                    line = line.split(self.__DELIMETER)

                    salesOrder = SalesOrder()
                    salesOrder.setSalesOrderId(int(line[0]))
                    salesOrder.setCustomerId(int(line[1]))
                    salesOrder.setProductId(int(line[2]))
                    salesOrder.setQuantity(int(line[3]))
                    salesOrder.setDateFilled(datetime.datetime.strptime(line[4], '%Y-%m-%d').date())
                    # sales order in the open order file have no shipping id yet, 'None' is stored
                    if line[5] != 'None':
                        salesOrder.setShippingId(int(line[5]))

                    # updated highest id
                    if salesOrder.getSalesOrderId() >= SalesOrder.highestId:
                        SalesOrder.highestId = salesOrder.getSalesOrderId()

                    # append to records
                    self.openOrderFile.enqueue(salesOrder)
        except FileNotFoundError:
            file = open(self.__OPEN_ORDER, "x")
            file.close()

        # back order file
        try:
            with open(self.__BACK_ORDER, "r") as file:
                datas = file.read().split("\n")

                for line in datas:
                    if line == '':
                        break
                    # salesOrderId, customerId, productId, quantity, dateFilled, shippingId
                    line = line.split(self.__DELIMETER)

                    salesOrder = SalesOrder()
                    salesOrder.setSalesOrderId(int(line[0]))
                    salesOrder.setCustomerId(int(line[1]))
                    salesOrder.setProductId(int(line[2]))
                    salesOrder.setQuantity(int(line[3]))
                    salesOrder.setDateFilled(datetime.datetime.strptime(line[4], '%Y-%m-%d').date())
                    # sales order in the back order file have no shipping id yet, 'None' is stored
                    if line[5] != 'None':
                        salesOrder.setShippingId(int(line[5]))

                    # updated highest id
                    if salesOrder.getSalesOrderId() >= SalesOrder.highestId:
                        SalesOrder.highestId = salesOrder.getSalesOrderId()

                    # append to records
                    self.backOrderFile.enqueue(salesOrder)
        except FileNotFoundError:
            file = open(self.__BACK_ORDER, "x")
            file.close()

        # pending file
        try:
            with open(self.__PENDING_ORDER, "r") as file:
                datas = file.read().split("\n")

                for line in datas:
                    if line == '':
                        break
                    # salesOrderId, customerId, productId, quantity, dateFilled, shippingId
                    line = line.split(self.__DELIMETER)
                    salesOrder = SalesOrder()
                    salesOrder.setSalesOrderId(int(line[0]))
                    salesOrder.setCustomerId(int(line[1]))
                    salesOrder.setProductId(int(line[2]))
                    salesOrder.setQuantity(int(line[3]))
                    salesOrder.setDateFilled(datetime.datetime.strptime(line[4], '%Y-%m-%d').date())
                    # sales order in the pending order file have shipping id
                    if line[5] != 'None':
                        salesOrder.setShippingId(int(line[5]))

                    # updated highest id
                    if salesOrder.getSalesOrderId() >= SalesOrder.highestId:
                        SalesOrder.highestId = salesOrder.getSalesOrderId()

                    # append to records
                    self.salesOrderPendingFile.enqueue(salesOrder)
                    self.temporaryPendingFile.insertNode(salesOrder)
        except FileNotFoundError:
            file = open(self.__PENDING_ORDER, "x")
            file.close()

        # shipping log
        try:
            with open(self.__SHIPPING_LOG, "r") as file:
                datas = file.read().split("\n")
                # instantiate hash table
                self.shippingLogHashTable = HashTable(PrimeHelper.findNearestPrime(len(datas) + 20))

                for line in datas:
                    if line == '':
                        break
                    # shippingId, dateShipped, dateDelivered
                    line = line.split(self.__DELIMETER)
                    shippingDetails = ShipmentDetails()
                    shippingDetails.setShippingId(int(line[0]))
                    shippingDetails.setDateShipped(datetime.datetime.strptime(line[1], '%Y-%m-%d').date())
                    # there are shipping log that are not yet delivered
                    if line[2] != 'None':
                        shippingDetails.setDateDelivered(datetime.datetime.strptime(line[2], '%Y-%m-%d').date())

                    # updated highest id
                    if shippingDetails.getShippingId() >= ShipmentDetails.highestId:
                        ShipmentDetails.highestId = shippingDetails.getShippingId()

                    # append to records
                    self.shippingLog.insertNode(shippingDetails)
                    self.shippingLogHashTable.storeData(shippingDetails.methodForHashTable(), shippingDetails)
        except FileNotFoundError:
            file = open(self.__SHIPPING_LOG, "x")
            file.close()

        # sales journal
        try:
            with open(self.__SALES_JOURNAL, "r") as file:
                datas = file.read().split("\n")
                # instantiate hash table
                self.journalHashTable = HashTable(PrimeHelper.findNearestPrime(len(datas)+20))

                for line in datas:
                    if line == '':
                        break
                    # journalId, dateCompleted (dateShipped), paid (boolean), datePaid
                    # salesOrderId, customerId, productId, quantity, dateFilled, shippingId
                    line = line.split(self.__DELIMETER)
                    journalEntry = JournalEntry()
                    journalEntry.setJournalId(int(line[0]))
                    journalEntry.setDateCompleted(datetime.datetime.strptime(line[1], '%Y-%m-%d').date())

                    if line[2] == 'True':
                        journalEntry.setPaymentStatus(True)
                        journalEntry.setDatePaid(datetime.datetime.strptime(line[3], '%Y-%m-%d').date())
                    else:
                        journalEntry.setPaymentStatus(False)

                    salesOrder = SalesOrder()
                    salesOrder.setSalesOrderId(int(line[4]))
                    salesOrder.setCustomerId(int(line[5]))
                    salesOrder.setProductId(int(line[6]))
                    salesOrder.setQuantity(int(line[7]))
                    salesOrder.setDateFilled(datetime.datetime.strptime(line[8], '%Y-%m-%d').date())
                    # just to catch any errors
                    if line[9] != 'None':
                        salesOrder.setShippingId(int(line[9]))

                    journalEntry.setSalesOrder(salesOrder)

                    # updated highest id
                    if journalEntry.getJournalId() >= JournalEntry.highestId:
                        JournalEntry.highestId = journalEntry.getJournalId()
                    if salesOrder.getSalesOrderId() >= SalesOrder.highestId:
                        SalesOrder.highestId = salesOrder.getSalesOrderId()

                    # append to records
                    self.salesJournal.insertNode(journalEntry)
                    self.journalHashTable.storeData(journalEntry.methodForHashTable(), journalEntry)
        except FileNotFoundError:
            file = open(self.__SALES_JOURNAL, "x")
            file.close()

    def saveRecords(self):
        # customer records
        try:
            with open(self.__CUSTOMER_RECORDS, "w") as file:
                # travers customer records
                customerRecord = self.customerInformation.head
                while customerRecord != None:
                    # customerId, name, amountPayable, creditLimit
                    line = str(customerRecord.data.getCustomerId()) + self.__DELIMETER
                    line += customerRecord.data.getName() + self.__DELIMETER
                    line += str(customerRecord.data.getAmountPayable()) + self.__DELIMETER
                    line += str(customerRecord.data.getCreditLimit()) + "\n"

                    file.write(line)
                    customerRecord = customerRecord.next
        except FileNotFoundError:
            file = open(self.__CUSTOMER_RECORDS, "x")
            file.close()
            self.saveRecords()

        # stock records
        try:
            with open(self.__STOCK_RECORDS, "w") as file:
                # travers stock records
                productRecord = self.stockRecords.head
                while productRecord != None:
                    # productId, name, stock count, price
                    line = str(productRecord.data.getProductId()) + self.__DELIMETER
                    line += productRecord.data.getName() + self.__DELIMETER
                    line += str(productRecord.data.getStock()) + self.__DELIMETER
                    line += str(productRecord.data.getPrice()) + "\n"

                    file.write(line)
                    productRecord = productRecord.next
        except FileNotFoundError:
            file = open(self.__STOCK_RECORDS, "x")
            file.close()
            self.saveRecords()

        # customer orders
        try:
            with open(self.__CUSTOMER_ORDERS, "w") as file:
                while True:
                    # dequeue customer order
                    customerOrder = self.customerOrder.dequeue()
                    if customerOrder == None:
                        break

                    # items[int], itemQuantitites[int], customerId
                    line = str(customerOrder.data.getItems()) + self.__DELIMETER
                    line += str(customerOrder.data.getItemQuantities()) + self.__DELIMETER
                    line += str(customerOrder.data.getCustomerId()) + "\n"
                    file.write(line)
        except FileNotFoundError:
            file = open(self.__CUSTOMER_ORDERS, "x")
            file.close()
            self.saveRecords()

        # open order file
        try:
            with open(self.__OPEN_ORDER, "w") as file:
                while True:
                    # dequeue sales order from open order file
                    salesOrder = self.openOrderFile.dequeue()
                    if salesOrder == None:
                        break

                    # salesOrderId, customerId, productId, quantity, dateFilled, shippingId
                    line = str(salesOrder.data.getSalesOrderId()) + self.__DELIMETER
                    line += str(salesOrder.data.getCustomerId()) + self.__DELIMETER
                    line += str(salesOrder.data.getProductId()) + self.__DELIMETER
                    line += str(salesOrder.data.getQuantity()) + self.__DELIMETER
                    line += str(salesOrder.data.getDateFilled()) + self.__DELIMETER
                    line += str(salesOrder.data.getShippingId()) + "\n"

                    file.write(line)
        except FileNotFoundError:
            file = open(self.__OPEN_ORDER, "x")
            file.close()
            self.saveRecords()

        # back order file
        try:
            with open(self.__BACK_ORDER, "w") as file:
                while True:
                    # dequeue sales order from back order file
                    salesOrder = self.backOrderFile.dequeue()
                    if salesOrder == None:
                        break

                    # salesOrderId, customerId, productId, quantity, dateFilled, shippingId
                    line = str(salesOrder.data.getSalesOrderId()) + self.__DELIMETER
                    line += str(salesOrder.data.getCustomerId()) + self.__DELIMETER
                    line += str(salesOrder.data.getProductId()) + self.__DELIMETER
                    line += str(salesOrder.data.getQuantity()) + self.__DELIMETER
                    line += str(salesOrder.data.getDateFilled()) + self.__DELIMETER
                    line += str(salesOrder.data.getShippingId()) + "\n"

                    file.write(line)
        except FileNotFoundError:
            file = open(self.__BACK_ORDER, "x")
            file.close()
            self.saveRecords()

        # pending order file
        try:
            with open(self.__PENDING_ORDER, "w") as file:
                while True:
                    # dequeue sales order from pending order file
                    # there is already a shippingId in the sales order
                    salesOrder = self.salesOrderPendingFile.dequeue()
                    if salesOrder == None:
                        break

                    # salesOrderId, customerId, productId, quantity, dateFilled, shippingId
                    line = str(salesOrder.data.getSalesOrderId()) + self.__DELIMETER
                    line += str(salesOrder.data.getCustomerId()) + self.__DELIMETER
                    line += str(salesOrder.data.getProductId()) + self.__DELIMETER
                    line += str(salesOrder.data.getQuantity()) + self.__DELIMETER
                    line += str(salesOrder.data.getDateFilled()) + self.__DELIMETER
                    line += str(salesOrder.data.getShippingId()) + "\n"

                    file.write(line)
        except FileNotFoundError:
            file = open(self.__PENDING_ORDER, "x")
            file.close()
            self.saveRecords()

        # shipping log
        try:
            with open(self.__SHIPPING_LOG, "w") as file:
                # traverse shipping log records
                shippingDetail = self.shippingLog.head
                while shippingDetail != None:
                    # shippingId, dateShipped, dateDelivered
                    line = str(shippingDetail.data.getShippingId()) + self.__DELIMETER
                    line += str(shippingDetail.data.getDateShipped()) + self.__DELIMETER
                    line += str(shippingDetail.data.getDateDelivered()) + "\n"
                    file.write(line)

                    shippingDetail = shippingDetail.next
        except FileNotFoundError:
            file = open(self.__SHIPPING_LOG, "x")
            file.close()
            self.saveRecords()

        # sales journal
        try:
            with open(self.__SALES_JOURNAL, "w") as file:
                # travers customer records
                salesJournal = self.salesJournal.head
                while salesJournal != None:

                    # journalId, dateCompleted (dateShipped), paid (boolean), datePaid
                    # salesOrderId, customerId, productId, quantity, dateFilled, shippingId
                    line = str(salesJournal.data.getJournalId()) + self.__DELIMETER
                    line += str(salesJournal.data.getDateCompleted()) + self.__DELIMETER
                    line += str(salesJournal.data.getPaymentStatus()) + self.__DELIMETER
                    line += str(salesJournal.data.getDatePaid()) + self.__DELIMETER
                    # sales order
                    line += str(salesJournal.data.getSalesOrder().getSalesOrderId()) + self.__DELIMETER
                    line += str(salesJournal.data.getSalesOrder().getCustomerId()) + self.__DELIMETER
                    line += str(salesJournal.data.getSalesOrder().getProductId()) + self.__DELIMETER
                    line += str(salesJournal.data.getSalesOrder().getQuantity()) + self.__DELIMETER
                    line += str(salesJournal.data.getSalesOrder().getDateFilled()) + self.__DELIMETER
                    line += str(salesJournal.data.getSalesOrder().getShippingId()) + "\n"

                    file.write(line)
                    salesJournal = salesJournal.next
        except FileNotFoundError:
            file = open(self.__SALES_JOURNAL, "x")
            file.close()
            self.saveRecords()