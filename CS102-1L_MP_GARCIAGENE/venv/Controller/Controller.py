from Helpers.InputHelper import InputHelper
from Helpers.DataHelper import DataHelper
from Helpers.ASCIIHelper import ASCIIHelper

from DataStructures.QuickSort import QuickSort

from Models.CustomerOrder import CustomerOrder
from Models.SalesOrder import SalesOrder
from Models.CustomerInformation import  CustomerInformation
from Models.ShipmentDetails import ShipmentDetails
from Models.JournalEntry import JournalEntry

from datetime import date

class Controller:

    def __init__(self):
        print("--Controller")

        data = DataHelper()
        data.populate()
        self.data = data

        self.showMainMenu()

    def showMainMenu(self):
        menuSelection = None
        while menuSelection != 0:
            print("""
    1 Take customer's order
    2 Create sales order
    3 Process back orders
    4 Ship orders
    5 Bill customer # also insert record in Sales Journal
    6 Display records
    7 Other Menu
    0 Terminate program""")
            menuSelection = InputHelper.integerInputWithChoices("Select from menu", [1, 2, 3, 4, 5, 6, 7, 0])
            print()

            if menuSelection == 1:
                self.takeCustomerOrder()

            elif menuSelection == 2:
                self.createSalesOrder()

            elif menuSelection == 3:
                self.processBackOrders()

            elif menuSelection == 4:
                self.shipOrders()

            elif menuSelection == 5:
                self.billCustomer()

            elif menuSelection == 6:
                self.showDisplayMenu()

            elif menuSelection == 7:
                self.showOtherMenu()

            elif menuSelection == 0:
                print("\n\tTerminating program...")
                break

    def showDisplayMenu(self):
        """
        1 Customer information
        2 Sales journal records
        3 Shipping log
        4 SO Pending files
        """
        pass

    def showOtherMenu(self):
        print("""
    1 Add Customer
    2 Add Product
    3 Add Product Stock
    4 Mark Order sa Paid
    5 Mark Order as Delivered
        """)
        menuSelection = InputHelper.integerInputWithChoices("Select from other menu", [1, 2, 3, 4, 5])
        print()

        if menuSelection == 1:
            pass

        elif menuSelection == 4:
            self.markOrderAsPaid()

        elif menuSelection == 5:
            pass

    def markOrderAsPaid(self):
        print("\tMARK SALES ORDER AS PAID\n")
        # display sales journal by date completed that are unpaid
        # select a sales journal
        # ask amount to be given
        # set journalEntry as paid
        # find customer model and compute its amount

        if self.data.salesJournal.head != None:

            # display sales journal by date completed
            salesJournalList = self.data.salesJournal.convertToList()
            quicksort = QuickSort()
            # pass by reference
            quicksort.sort(salesJournalList, 0, len(salesJournalList) - 1)

            # temp sales journal ids that are unpaid
            salesJournalIds = []

            # display sales journal
            for journalEntry in salesJournalList:
                journalEntry = journalEntry.data

                if journalEntry.getPaymentStatus() == True:
                    # continue loop
                    continue

                # append the unpaid sales journal's id
                salesJournalIds.append(journalEntry.getJournalId())

                print("\t\tSales Journal Summary")
                journalEntry.displaySummary()

                # display customer
                customerModel = self.data.custInfoHashTable.findData(journalEntry.getSalesOrder().getCustomerId())
                print("\tCustomer name", customerModel.getName())

                # display product
                productModel = self.data.stockRecordsHashTable.findData(journalEntry.getSalesOrder().getProductId())
                print("\tProduct Name", productModel.getName())

                print()

            if len(salesJournalIds) > 0:
                # select a sales journal
                selectedSalesJournalId = InputHelper.integerInputWithChoices("Select a sales journal Id", salesJournalIds)

                # find sales journal using the selectedsalesjournalid
                salesJournal = self.data.salesJournal.head
                while salesJournal != None:
                    if salesJournal.data.getJournalId() == selectedSalesJournalId:
                        break
                    salesJournal = salesJournal.next

                print("\t\tSelected Sales Journal")
                salesJournal.data.displaySummary()

                # display customer
                customerModel = self.data.custInfoHashTable.findData(salesJournal.data.getSalesOrder().getCustomerId())
                print("\tCustomer name", customerModel.getName(), customerModel.getAmountPayable())

                # display product
                productModel = self.data.stockRecordsHashTable.findData(salesJournal.data.getSalesOrder().getProductId())
                print("\tProduct Name", productModel.getName())

                # update sales journal
                salesJournal.data.setPaymentStatus(True)
                salesJournal.data.setDatePaid(date.today())

                # recomppute customer's amount payable
                # implement stack
                salesAmount = salesJournal.data.getSalesOrder().getQuantity() * productModel.getPrice()
                customerModel.setAmountPayable( customerModel.getAmountPayable() - salesAmount  )

                # even though that I only update the variables
                # it will reflect in the singly linked list stored nodes, and in the hash table

            else:
                print("\tAll the current sales orders are paid by the customers")

        else:
            print("\tThere currently no sales journal record")


    def billCustomer(self):
        print("\tBILL CUSTOMERS\n")
        # includes re-computing customer credit/amount payable

        if self.data.temporaryPendingFile.head != None:

            shippingLogList = self.data.shippingLog.convertToList()
            quicksort = QuickSort()
            # pass by reference
            quicksort.sort(shippingLogList, 0, len(shippingLogList) - 1)

            # temporary list of sales order ids
            salesOrderIdList = []

            # display shipping log and its sales order
            for log in shippingLogList:
                log = log.data
                # find sales order using shippingId
                salesOrder = self.data.temporaryPendingFile.head
                while salesOrder != None:
                    if salesOrder.data.getShippingId() == log.getShippingId():
                        salesOrderIdList.append(salesOrder.data.getSalesOrderId())
                        break
                    salesOrder = salesOrder.next

                if salesOrder != None:
                    # sales order
                    salesOrder.data.displaySummary()

                    # shipping details
                    log.displaySummary()

                    # display customer
                    customerModel = self.data.custInfoHashTable.findData(salesOrder.data.getCustomerId())
                    print("\tCustomer name", customerModel.getName())

                    # display product
                    productModel = self.data.stockRecordsHashTable.findData(salesOrder.data.getProductId())
                    print("\tProduct Name", productModel.getName())

                print()

            # select sales order
            selectedSalesOrderId = InputHelper.integerInputWithChoices("Select from sales order Id", salesOrderIdList)

            # find the sales order using the selected id
            salesOrder = self.data.temporaryPendingFile.head
            while salesOrder != None:
                if salesOrder.data.getSalesOrderId() == selectedSalesOrderId:
                    break
                salesOrder = salesOrder.next

            print("\n\t\tSelected Sales Order")
            salesOrder.data.displaySummary()

            # display customer
            customerModel = self.data.custInfoHashTable.findData(salesOrder.data.getCustomerId())
            print("\tCustomer name", customerModel.getName())

            # display product
            productModel = self.data.stockRecordsHashTable.findData(salesOrder.data.getProductId())
            print("\tProduct Name", productModel.getName())

            # remove the sales order from the temporaryPendingFile
            self.data.temporaryPendingFile.deleteNode(salesOrder)

            # find shipmentdetails using salesOrder's
            shippingDetail = self.data.shippingLog.head
            while shippingDetail != None:
                if shippingDetail.data.getShippingId() == salesOrder.data.getShippingId():
                    break
                shippingDetail = shippingDetail.next

            # create journal entry
            journalEntry = JournalEntry()
            # shipping model date delivered
            journalEntry.setDateCompleted(shippingDetail.data.getDateShipped())
            print("\tDate Completed", shippingDetail.data.getDateShipped())
            journalEntry.setJournalId(JournalEntry.getId())
            journalEntry.setSalesOrder(salesOrder.data)

            # record journal entry
            self.data.salesJournal.insertNode(journalEntry)

            # re-compute customers credit payable

            print("\n\tCustomer", customerModel.getName(), "billed with sales order #", salesOrder.data.getSalesOrderId())

        else:
            print("\tThere are currently no sales orders to be billed")

    def shipOrders(self):
        print("\tSHIP ORDERS\n")

        toShip = self.data.openOrderFile.dequeue()
        if toShip != None:
            toShip = toShip.data

            print("\tCreating shipment records for sales order #", toShip.getSalesOrderId())

            # create shipping record
            shippingDetails = ShipmentDetails()
            shippingDetails.setShippingId(ShipmentDetails.getId())
            shippingDetails.setDateShipped(date.today())
            shippingDetails.setDateDelivered(None)

            # reference shipping details to sales order
            toShip.setShippingId(shippingDetails.getShippingId())

            print("\n\t\tSales Order Summary")
            toShip.displaySummary()

            # display customer
            customerModel = self.data.custInfoHashTable.findData(toShip.getCustomerId())
            print("\tCustomer name", customerModel.getName())

            # display product
            productModel = self.data.stockRecordsHashTable.findData(toShip.getProductId())
            print("\tProduct Name", productModel.getName())

            print("\n\t\tShipping Log details")
            shippingDetails.displaySummary()

            # entry to shipping log
            self.data.shippingLog.insertNode(shippingDetails)
            # entry to pending file
            self.data.salesOrderPendingFile.enqueue(toShip)
            self.data.temporaryPendingFile.insertNode(toShip)

            # add date computation
            print("\n\tSales order filed for shipment and will be delivered to the customer after exactly 7 days")

        else:
            print("\n\tThere are currently no orders for shipping")

    def processBackOrders(self):
        print("\tPROCESSING BACK ORDERS\n")
        # already a sales order
        salesBackOrder = self.data.backOrderFile.dequeue()

        if salesBackOrder != None:
            salesBackOrder = salesBackOrder.data

            # find in hash table
            customerModel = self.data.custInfoHashTable.findData(salesBackOrder.getCustomerId())

            if customerModel != None:
                """"# reconsile and check amount payables and credit limit"""
                # # # # what if a product is already stocked but, the sales order is at the back of the queue

                # check inventory
                # if sufficient enqueue to open order
                # otherwise enqueue again to back order file

                productModel = self.data.stockRecordsHashTable.findData(salesBackOrder.getProductId())
                if productModel != None:
                    print("\tSales Order for", salesBackOrder.getCustomerId(), customerModel.getName())
                    salesBackOrder.displaySummary()
                    print("\tTotal cost in PHP", productModel.getPrice() * salesBackOrder.getQuantity())

                    # check if stock inventory is enough for the order
                    if salesBackOrder.getQuantity() <= productModel.getStock():
                        # reduce stock
                        productModel.setStock(productModel.getStock() - salesBackOrder.getQuantity())
                        # file in open order file
                        self.data.openOrderFile.enqueue(salesBackOrder)
                        print("\n\tSales Order Queued in Open Order File Successfully")
                    else:
                        # file in back order file
                        self.data.backOrderFile.enqueue(salesBackOrder)
                        print("\n\tSales Order Queued in Back Order File Again Due to insufficient quantity")

        else:
            print("\tThere are currently no back orders in queue")

    def createSalesOrder(self):
        print("\tPROCESSING CUSTOMER ORDER TO SALES ORDERS\n")
        toProcess = self.data.customerOrder.dequeue()

        if toProcess:
            toProcess = toProcess.data
            # check if customer order's customer
            customerModel = self.data.custInfoHashTable.findData(toProcess.getCustomerId())

            if customerModel != None:
                """"# reconsile and check amount payables and credit limit"""

                # loop each item
                # check product records if existing
                # check stocks if sufficient
                # create sales order
                # create open order or back order

                for orderIndex in range(len(toProcess.getItems())):

                    productModel = self.data.stockRecordsHashTable.findData(toProcess.getItems()[orderIndex])
                    if productModel != None:

                        # create sales order
                        salesOrder = SalesOrder()
                        salesOrder.setSalesOrderId(SalesOrder.getId())
                        salesOrder.setProductId(productModel.getProductId())
                        salesOrder.setQuantity(toProcess.getItemQuantities()[orderIndex])
                        salesOrder.setCustomerId(customerModel.getCustomerId())
                        salesOrder.setDateFilled(date.today())
                        # no shipping id yet

                        # display sales order
                        print("\tSales Order for", salesOrder.getCustomerId(), customerModel.getName())
                        salesOrder.displaySummary()
                        print("\tTotal cost in PHP", productModel.getPrice() * toProcess.getItemQuantities()[orderIndex])

                        # check if stock inventory is enough for the order
                        if toProcess.getItemQuantities()[orderIndex] <= productModel.getStock():
                            # reduce stock
                            productModel.setStock( productModel.getStock() - toProcess.getItemQuantities()[orderIndex] )
                            # file in open order file
                            self.data.openOrderFile.enqueue(salesOrder)
                            print("\n\tSales Order Queued in Open Order File Successfully")
                        else:
                            # file in back order file
                            self.data.backOrderFile.enqueue(salesOrder)
                            print("\n\tSales Order Queued in Back Order File Due to insufficient quantity\n")

            else:
                print("\tCustomer not found with id", toProcess.getCustomerName())

        else:
            print("\tThere are currently no customer orders in queue")

    def takeCustomerOrder(self):
        customerOrder = CustomerOrder()

        productIdList = []
        customerIdList = []

        # display customer
        current = self.data.customerInformation.head
        while current != None:
            customerIdList.append(current.data.getCustomerId())
            print(f"\tId {current.data.getCustomerId()} {current.data.getName()}\n\tCurrent Payables {current.data.getAmountPayable()}\n")
            current = current.next

        # select customer
        customerId = InputHelper.integerInputWithChoices("Select a customer Id", customerIdList)
        customerOrder.setCustomerId(customerId)

        # display products
        print("\n\tProducts")
        current = self.data.stockRecords.head
        while current != None:
            productIdList.append(current.data.getProductId())
            print(f"\tid {current.data.getProductId()} {current.data.getName()}\tPHP {current.data.getPrice()}")
            current = current.next

        # product name
        # product quantity
        productInput = None
        quantityInput = None
        orderProductIds = []
        orderProductQuantities = []
        while True:
            productInput = InputHelper.integerInputWithChoices("Select a product Id", productIdList)
            quantityInput = InputHelper.integerInput("Product quantity", 1)

            if productInput in orderProductIds:
                # if the selected product id is already added, just increment its quantities
                index = orderProductIds.index(productInput)
                orderProductQuantities[index] += quantityInput
            else:
                orderProductIds.append(productInput)
                orderProductQuantities.append(quantityInput)

            userInput = InputHelper.stringInput("Enter Y to add more products").upper()
            if userInput != "Y":
                break

        # append to records
        customerOrder.setItems(orderProductIds)
        customerOrder.setItemQuantities(orderProductQuantities)
        self.data.customerOrder.enqueue(customerOrder)