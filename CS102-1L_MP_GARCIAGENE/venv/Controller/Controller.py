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
        """
        1 Add Customer
        2 Add Product
        3 Add Product Stock
        """
        pass

    def billCustomer(self):
        print("\tBILL CUSTOMERS\n")
        # includes re-computing customer credit/amount payable

        if self.data.temporaryPendingFile.head != None:

            shippingLogList = self.data.shippingLog.convertToList()
            quicksort = QuickSort()
            quicksort.sort(shippingLogList, 0, len(shippingLogList) - 1)

            # temporary list of sales order ids
            salesOrderIdList = []
            # display shipping log
            for log in shippingLogList:
                log = log.data
                # find sales order using shippingId
                current = self.data.temporaryPendingFile.head
                while current != None:
                    if current.data.getShippingId() == log.getShippingId():
                        salesOrderIdList.append(current.data.getSalesOrderId())
                        break
                    current = current.next

                if current != None:
                    current.data.displaySummary()
                    log.displaySummary()

                print()

            # select sales order
            selectedSalesOrderId = InputHelper.integerInputWithChoices("Select from sales order Id", salesOrderIdList)

            # find the sales order using the selected id
            salesOrder = self.data.temporaryPendingFile.head
            while salesOrder != None:
                if salesOrder.data.getSalesOrderId() == selectedSalesOrderId:
                    break
                salesOrder = salesOrder.next

            print("\tSelected Sales Order")
            salesOrder.data.displaySummary()
            # remove the sales order from the temporaryPendingFile
            self.data.temporaryPendingFile.deleteNode(salesOrder)

            # create journal entry
            journalEntry = JournalEntry()
            journalEntry.setDateFiled(date.today())
            journalEntry.setJournalId(JournalEntry.getId())
            journalEntry.setSalesOrder(salesOrder)

            # record journal entry
            self.data.salesJournal.insertNode(journalEntry)

            # re-compute customers credit payable

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

            print("\n\tSales Order Summary")
            toShip.displaySummary()

            print("\n\tShipping Log details")
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

            # find customer using id
            current = self.data.customerInformation.head
            while current != None:
                if current.data.getCustomerId() == salesBackOrder.getCustomerId():
                    break
                current = current.next
            # find in hash table, to abide by the proposal
            customerModel = self.data.custInfoHashTable.findData(ASCIIHelper.toASCII(current.data.getName()))

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
            customerModel = self.data.custInfoHashTable.findData(ASCIIHelper.toASCII(toProcess.getCustomerName()))

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
                print("\tCustomer not found with name", toProcess.getCustomerName())

        else:
            print("\tThere are currently no customer orders in queue")

    def takeCustomerOrder(self):
        customerOrder = CustomerOrder()

        productIdList = []

        # customer name
        customerName = InputHelper.stringInput("Customer name [Observe proper name capitalization]")
        customerOrder.setCustomerName(customerName)

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