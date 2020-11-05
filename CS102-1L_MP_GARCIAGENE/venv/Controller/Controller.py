from Helpers.InputHelper import InputHelper
from Helpers.ASCIIHelper import ASCIIHelper

from DataStructures.QuickSort import QuickSort

from Models.CustomerOrder import CustomerOrder
from Models.SalesOrder import SalesOrder
from Models.CustomerInformation import  CustomerInformation
from Models.ShipmentDetails import ShipmentDetails
from Models.JournalEntry import JournalEntry
from Models.Product import Product

from Models.DataRepository import DataRepository

from datetime import date

class Controller:

    def __init__(self):
        data = DataRepository()
        self.data = data
        self.data.populate()

        # menus for lambda
        self.mainMenus = {
            1: self.takeCustomerOrder,
            2: self.createSalesOrder,
            3: self.processBackOrder,
            4: self.shipOrders,
            5: self.billCustomer,
            6: self.showDisplayMenu,
            7: self.showOtherMenu,
            0: self.terminateProgram
        }
        self.displayMenus = {
            1: self.displayCustomers,
            2: self.displaySalesJournals,
            3: self.displayShippingLog
        }
        self.otherMenus = {
            1: self.addCustomer,
            2: self.addProduct,
            3: self.increaseProductStock,
            4: self.markOrderAsPaid,
            5: self.markOrderAsDelivered
        }

        self.showMainMenu()

    def showMainMenu(self):
        menuSelection = None

        while menuSelection != 0:
            print("\n\t1 Take customer's order")
            print("\t2 Create sales order")
            print("\t3 Process back orders")
            print("\t4 Ship orders")
            print("\t5 Bill customer")
            print("\t6 Display records")
            print("\t7 Other Menu")
            print("\t0 Terminate program")
            menuSelection = InputHelper.integerInputWithChoices("> Select from menu", [1, 2, 3, 4, 5, 6, 7, 0])
            print()

            self.mainMenus[menuSelection]()
            # end program
            if menuSelection == 0:
                break

    def showDisplayMenu(self):
        print("\n\t1 Customer information")
        print("\t2 Sales journal records")
        print("\t3 Shipping log")
        menuSelection = InputHelper.integerInputWithChoices("> Select from display menu", [1, 2, 3])
        print()

        self.displayMenus[menuSelection]()

    def showOtherMenu(self):
        print("\n\t1 Add Customer")
        print("\t2 Add Product")
        print("\t3 Increase Product Stock")
        print("\t4 Mark Order sa Paid")
        print("\t5 Mark Order as Delivered")
        menuSelection = InputHelper.integerInputWithChoices("> Select from other menu", [1, 2, 3, 4, 5])
        print()

        self.otherMenus[menuSelection]()

    # reusable code
    def recordSalesOrder(self, salesOrder, customerModel, productModel):
        # check if stock inventory is enough for the order
        if salesOrder.getQuantity() <= productModel.getStock():

            # change credit limit policy
            # as long as it is not yet maxed out allow it to process
            a = 10

            # check customer's credit limit and current payable
            totalSales = salesOrder.getQuantity() * productModel.getPrice()
            if (customerModel.getAmountPayable() + totalSales) >= customerModel.getCreditLimit():
                # file in back order file
                self.data.backOrderFile.enqueue(salesOrder)
                print("\n\tSales Order Queued in Back Order File because customer will max out their credit limit worh PHP",
                      customerModel.getCreditLimit(), "\n")

            else:
                # reduce stock
                productModel.setStock(productModel.getStock() - salesOrder.getQuantity())
                # file in open order file
                self.data.openOrderFile.enqueue(salesOrder)
                print("\n\tSales Order Queued in Open Order File Successfully\n")

        else:
            # file in back order file
            self.data.backOrderFile.enqueue(salesOrder)
            print("\n\tSales Order Queued in Back Order File Due to insufficient quantity\n")
    # reusable code
    def displayOrderSummary(self, orderQuantity, productName, productPrice, customerName):
        # display customer
        print(f"\n\t     Customer Name:    {customerName}")
        # display product
        print(f"\t      Product Name:    {productName}")
        if orderQuantity != -1:
            print(f"\t Total Sales Price:    PHP {productPrice * orderQuantity}")

    # other menu
    def addCustomer(self):
        print("\t>>> ADD NEW CUSTOMER RECORD <<<\n")

        # get name of customer
        name = InputHelper.stringInput("Enter customer name")

        # check if name is existing
        customerModel = self.data.customerInformation.head
        while customerModel != None:
            if customerModel.data.getName().upper() == name.upper():
                break # customer exists
            customerModel = customerModel.next

        if customerModel == None:
            # set credit limit
            creditLimit = InputHelper.floatInput("Enter customer credit limit", min = 0)

            customerModel = CustomerInformation()
            customerModel.setName(name)
            customerModel.setCustomerId(CustomerInformation.getId())
            customerModel.setAmountPayable(0)
            customerModel.setCreditLimit(creditLimit)

            # insert node
            self.data.customerInformation.insertNode(customerModel)

            # insert to hash table
            self.data.custInfoHashTable.storeData(customerModel.methodForHashTable(), customerModel)

        else:
            print("\tCustomer with name", name, "is already existing.")

    def addProduct(self):
        print("\t>>> ADD NEW PRODUCT <<<\n")

        # get product name
        productName = InputHelper.stringInput("Enter new product's name").upper()

        # find product model by name
        productModel = self.data.stockRecords.head
        while productModel != None:
            if productModel.data.getName() == productName:
                break # product is already existing
            productModel = productModel.next

        if productModel == None:
            basePrice = InputHelper.floatInput("Enter product's price", 0)
            productStock = InputHelper.integerInput("Enter current product stock", 0)

            productModel = Product()
            productModel.setProductId(Product.getId())
            productModel.setName(productName)
            productModel.setPrice(basePrice)
            productModel.setStock(productStock)

            # insert to stock records
            self.data.stockRecords.insertNode(productModel)

            # insert to stock records hash table
            self.data.stockRecordsHashTable.storeData(productModel.methodForHashTable(), productModel)

        else:
            print("\tProduct with", productName, "is already existing.")

    def increaseProductStock(self):
        print("\t>>> INCREASE PRODUCT INVENTORY STOCK <<<\n")

        productIds = []

        # display products first
        productModel = self.data.stockRecords.head

        if productModel != None:
            while productModel != None:
                print("\t\tProduct Record Summary")
                productIds.append(productModel.data.getProductId())
                productModel.data.displaySummary()
                productModel = productModel.next
                print()

            # select a product id to increase
            selectedProductId = InputHelper.integerInputWithChoices("Select a product Id to increase stock", productIds)

            # find productModel in hash table
            productModel = self.data.stockRecordsHashTable.findData(selectedProductId)

            # get stock numbers to add
            stocks = InputHelper.integerInput("How many stocks will the product be increased", min = 0)

            # update stocks
            productModel.setStock( productModel.getStock() + stocks )

        else:
            print("\tThere are currently no stock records")

    def markOrderAsPaid(self):
        print("\t>>> MARK SALES JOURNAL ENTRY AS PAID <<<\n")
        # display sales journal by date completed that are unpaid
        # select a sales journal
        # set journalEntry as paid
        # find customer model and compute its amount

        if self.data.salesJournal.head != None:

            # display sales journal by date completed
            salesJournalList = self.data.salesJournal.convertToList()
            quicksort = QuickSort()
            quicksort.sort(salesJournalList, 0, len(salesJournalList) - 1)

            # unpaid journals ids
            salesJournalIds = []

            # display sales journals
            for journalEntry in salesJournalList:
                journalEntry = journalEntry.data

                if journalEntry.getPaymentStatus() == True:
                    # paid sales order
                    continue

                # append the unpaid sales journal's id
                salesJournalIds.append(journalEntry.getJournalId())

                print("\t\t\tSALES JOURNAL ENTRY TO BE PAID")
                journalEntry.displaySummary()

                customerModel = self.data.custInfoHashTable.findData(journalEntry.getSalesOrder().getCustomerId())
                productModel = self.data.stockRecordsHashTable.findData(journalEntry.getSalesOrder().getProductId())

                # display
                self.displayOrderSummary(journalEntry.getSalesOrder().getQuantity(), productModel.getName(),
                                         productModel.getPrice(), customerModel.getName())
                print()

            if len(salesJournalIds) > 0:
                # select a sales journal
                selectedSalesJournalId = InputHelper.integerInputWithChoices("Select a sales journal Id", salesJournalIds)

                # find sales journal using the selectedSalesJournalId in hash table
                salesJournal = self.data.journalHashTable.findData(selectedSalesJournalId)

                print("\n\t\t\tSELECTED SALES JOURNAL TO BE PAID")
                salesJournal.displaySummary()

                customerModel = self.data.custInfoHashTable.findData(salesJournal.getSalesOrder().getCustomerId())
                productModel = self.data.stockRecordsHashTable.findData(salesJournal.getSalesOrder().getProductId())

                # update sales journal
                salesJournal.setPaymentStatus(True)
                salesJournal.setDatePaid(date.today())

                # re-compute customer's amount payable
                salesAmount = salesJournal.getSalesOrder().getQuantity() * productModel.getPrice()
                customerModel.setAmountPayable( customerModel.getAmountPayable() - salesAmount  )

                # display
                self.displayOrderSummary(salesJournal.getSalesOrder().getQuantity(), productModel.getName(),
                                         productModel.getPrice(), customerModel.getName())

                print(f"\n\tSales Journal record with ID #{salesJournal.getJournalId()} is paid as of {salesJournal.getDatePaid()}")

            else:
                print("\tAll the current sales orders are paid by the customers")

        else:
            print("\tThere currently no sales journal record")

    def markOrderAsDelivered(self):
        print("\t>>> MARK ORDER AS DELIVERED <<<\n")

        # dequeue from pending file
        # find its shipping idd

        # dequeue a sales order, and mark its shipping details as delivered
        # a sales order in the SO pending file is already recorded in the Sales Journal, during bill customer function
        salesOrder = self.data.salesOrderPendingFile.dequeue()

        if salesOrder != None:

            # find the shipping detail
            shippingDetail = self.data.shippingLogHashTable.findData(salesOrder.data.getShippingId())

            if shippingDetail != None:
                shippingDetail.setDateDelivered(date.today())

                print("\t\t\tSALES ORDER SUMMARY")
                salesOrder.data.displaySummary()

                print("\n\t\t\tSHIPPING LOG SUMMARY")
                shippingDetail.displaySummary()

                print(f"\n\tShipping log record with ID #{shippingDetail.getShippingId()} is set as delivered as of {shippingDetail.getDateDelivered()}")

        else:
            print("\tThere are no currently undelivered sales orders")

    # display menu
    def displayCustomers(self):
        print("\t>>> DISPLAY CUSTOMER INFORMATION SORT BY CUSTOMER NAME <<<\n")

        if self.data.customerInformation.head != None:

            customerList = self.data.customerInformation.convertToList()
            quicksort = QuickSort()
            quicksort.sort(customerList, 0, len(customerList) - 1)

            # display
            for customer in customerList:
                print("\t\t\tCUSTOMER INFORMATION RECORDS")
                customer.data.displaySummary()
                print("\t----------------------------------------")
                print()

        else:
            print("\tThere are currently no recorded customer")

    def displaySalesJournals(self):
        print("\t>>> DISPLAY SALES JOURNAL ENTRIES SORT BY DATE COMPLETED <<<\n")

        if self.data.salesJournal.head != None:

            journalList = self.data.salesJournal.convertToList()
            quicksort = QuickSort()
            quicksort.sort(journalList, 0, len(journalList) - 1)

            # display
            print("\t--------------------------------------")
            for journal in journalList:
                print("\t\t\tSALES JOURNAL ENTRY")
                journal.data.displaySummary()

                shippingDetail = self.data.shippingLogHashTable.findData(journal.data.getSalesOrder().getShippingId())
                print("\n\t\t\tSHIPPING LOG DETAIL")
                shippingDetail.displaySummary()
                print("\t--------------------------------------")
                print()

        else:
            print("\tThere are currently no recorded sales journal")

    def displayShippingLog(self):
        print("\t>>> DISPLAY SHIPPING LOGS SORT BY DATE <<<\n")

        if self.data.shippingLog.head != None:

            shippingList = self.data.shippingLog.convertToList()
            quicksort = QuickSort()
            quicksort.sort(shippingList, 0, len(shippingList) - 1)

            # display
            for shippingDetail in shippingList:
                # find connected sales order that are not yet recorded in the sales journals
                salesOrder = self.data.temporaryPendingFile.head
                while salesOrder != None:
                    if salesOrder.data.getShippingId() == shippingDetail.data.getShippingId():
                        break
                    salesOrder = salesOrder.next

                print("\t\t\tSHIPPING LOG DETAILS")
                shippingDetail.data.displaySummary()
                if salesOrder == None:
                    # already billed
                    print("\tSales order of this shipping log is already recorded in the sales journal")
                else:
                    print("\t\t\tSALES ORDER SUMMARY")
                    salesOrder.data.displaySummary()
                print("\t-------------------------------------")
                print()

        else:
            print("\tThere are currently no recorded shipping log")

    # main menu
    def terminateProgram(self):
        self.data.saveRecords()
        print("Terminating the program...")

    def billCustomer(self):
        print("\t>>> BILL CUSTOMERS <<<\n")
        # includes re-computing customer credit/amount payable

        if self.data.temporaryPendingFile.head != None:

            shippingLogList = self.data.shippingLog.convertToList()
            quicksort = QuickSort()
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
                    print("\t\t\tSALES ORDER FOR BILLING")
                    salesOrder.data.displaySummary()

                    customerModel = self.data.custInfoHashTable.findData(salesOrder.data.getCustomerId())
                    productModel = self.data.stockRecordsHashTable.findData(salesOrder.data.getProductId())

                    # display
                    self.displayOrderSummary(salesOrder.data.getQuantity(), productModel.getName(),
                                             productModel.getPrice(), customerModel.getName())

                    # shipping details
                    print("\n\t\t\tSHIPPING LOG SUMMARY")
                    log.displaySummary()
                    print("\t------------------------------------------")
                print()

            # select sales order
            selectedSalesOrderId = InputHelper.integerInputWithChoices("Select from sales order Id", salesOrderIdList)

            # find the sales order using the selected id
            salesOrder = self.data.temporaryPendingFile.head
            while salesOrder != None:
                if salesOrder.data.getSalesOrderId() == selectedSalesOrderId:
                    break
                salesOrder = salesOrder.next

            print("\n\t\t\tSELECTED SALES ORDER FOR BILLING")
            salesOrder.data.displaySummary()

            customerModel = self.data.custInfoHashTable.findData(salesOrder.data.getCustomerId())
            productModel = self.data.stockRecordsHashTable.findData(salesOrder.data.getProductId())

            # display
            self.displayOrderSummary(salesOrder.data.getQuantity(), productModel.getName(), productModel.getPrice(), customerModel.getName())

            # remove the sales order from the temporaryPendingFile
            self.data.temporaryPendingFile.deleteNode(salesOrder)

            # find shipmentdetails using salesOrder's
            shippingDetail = self.data.shippingLogHashTable.findData((salesOrder.data.getShippingId()))

            # create journal entry
            journalEntry = JournalEntry()
            # shipping model date delivered
            journalEntry.setDateCompleted(shippingDetail.getDateShipped())
            journalEntry.setJournalId(JournalEntry.getId())
            journalEntry.setSalesOrder(salesOrder.data)
            print(f"\t    Date Completed:    {journalEntry.getDateCompleted()}")

            # record journal entry
            self.data.salesJournal.insertNode(journalEntry)

            # insert to hash table
            self.data.journalHashTable.storeData(journalEntry.methodForHashTable(), journalEntry)

            # re-compute customers credit payable
            salesPrice = productModel.getPrice() * salesOrder.data.getQuantity()
            customerModel.setAmountPayable( customerModel.getAmountPayable() + salesPrice )

            print(f"\n\tCustomer {customerModel.getName()} billed with sales order #{salesOrder.data.getSalesOrderId()}")
            print(f"\tCurrent amount payable of customer is PHP {customerModel.getAmountPayable()}")

        else:
            print("\tThere are currently no sales orders to be billed")

    def shipOrders(self):
        print("\t>>> SHIP ORDERS <<<\n")

        salesOrderToShip = self.data.openOrderFile.dequeue()
        if salesOrderToShip != None:
            salesOrderToShip = salesOrderToShip.data

            print(f"\tCreating shipment records for sales order #{salesOrderToShip.getSalesOrderId()}")

            # create shipping record
            shippingDetails = ShipmentDetails()
            shippingDetails.setShippingId(ShipmentDetails.getId())
            shippingDetails.setDateShipped(date.today())
            shippingDetails.setDateDelivered(None)

            # reference shipping details to sales order
            salesOrderToShip.setShippingId(shippingDetails.getShippingId())

            print("\n\t\t\tSALES ORDER FOR SHIPMENT")
            salesOrderToShip.displaySummary()

            customerModel = self.data.custInfoHashTable.findData(salesOrderToShip.getCustomerId())
            productModel = self.data.stockRecordsHashTable.findData(salesOrderToShip.getProductId())

            # display
            self.displayOrderSummary(salesOrderToShip.getQuantity(), productModel.getName(), productModel.getPrice(), customerModel.getName())

            print("\n\t\t\tSHIPPING LOG DETAILS")
            shippingDetails.displaySummary()

            # entry to shipping log
            self.data.shippingLog.insertNode(shippingDetails)
            # store in hash table
            self.data.shippingLogHashTable.storeData(shippingDetails.methodForHashTable(), shippingDetails)
            # entry to pending file
            self.data.salesOrderPendingFile.enqueue(salesOrderToShip)
            self.data.temporaryPendingFile.insertNode(salesOrderToShip)

            # add date computation
            print("\n\tSales order filed for shipment and will be delivered to the customer after exactly 7 days")

        else:
            print("\n\tThere are currently no orders for shipping")

    def processBackOrder(self):
        print("\t>>> PROCESSING BACK ORDERS <<<\n")
        # already a sales order
        salesBackOrder = self.data.backOrderFile.dequeue()

        if salesBackOrder != None:
            salesBackOrder = salesBackOrder.data

            # find in hash table
            customerModel = self.data.custInfoHashTable.findData(salesBackOrder.getCustomerId())

            if customerModel != None:

                productModel = self.data.stockRecordsHashTable.findData(salesBackOrder.getProductId())
                if productModel != None:
                    print("\n\t\t\tBACK SALES ORDER SUMMARY")
                    salesBackOrder.displaySummary()

                    # display
                    self.displayOrderSummary(salesBackOrder.getQuantity(), productModel.getName(), productModel.getPrice(), customerModel.getName())

                    # enqueued again if stock is still insufficient or customers credit limit is not enough
                    self.recordSalesOrder(salesBackOrder, customerModel, productModel)

        else:
            print("\tThere are currently no back orders in queue")

    def createSalesOrder(self):
        print("\t>>> PROCESSING CUSTOMER ORDER TO SALES <<<\n")
        toProcess = self.data.customerOrder.dequeue()

        if toProcess:
            toProcess = toProcess.data

            # find customer record in the hash table
            customerModel = self.data.custInfoHashTable.findData(toProcess.getCustomerId())

            if customerModel != None:

                # each item ordered will have a sales order
                for orderIndex in range(len(toProcess.getItems())):

                    # find product record in the stock records hash table
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

                        print("\t\t\tNEW SALES ORDER")
                        # display sales order
                        salesOrder.displaySummary()
                        # display
                        self.displayOrderSummary(toProcess.getItemQuantities()[orderIndex], productModel.getName(), productModel.getPrice(), customerModel.getName())

                        self.recordSalesOrder(salesOrder, customerModel, productModel)

            else:
                print("\tCustomer not found with id", toProcess.getCustomerName())

        else:
            print("\tThere are currently no customer orders in queue")

    def takeCustomerOrder(self):
        print("\t>>> TAKE CUSTOMER ORDER <<<\n")

        customerOrder = CustomerOrder()

        productIdList = []
        customerIdList = []

        # display customer
        print("\t\t\tCUSTOMERS INFORMATION")
        customerModel = self.data.customerInformation.head
        while customerModel != None:
            customerIdList.append(customerModel.data.getCustomerId())
            customerModel.data.displaySummary()
            print()
            customerModel = customerModel.next

        # select customer
        customerId = InputHelper.integerInputWithChoices("Select a customer Id", customerIdList)

        # traverse stock recrods to display products and obtain the product ids
        print("\n\t\t\tPRODUCTS INFORMATION")
        productModel = self.data.stockRecords.head
        while productModel != None:
            productIdList.append(productModel.data.getProductId())
            productModel.data.displaySummary()
            print()
            productModel = productModel.next

        # product name
        # product quantity
        productInput = None
        quantityInput = None
        orderProductIds = []
        orderProductQuantities = []
        # add product and quantity
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

        # display customer order summary
        print("\n\t\t\tCUSTOMER ORDER SUMMARY")
        print(f"\tCustomer Name:    {self.data.custInfoHashTable.findData(customerId).getName()}")
        print(f"\tOrdered Products and Quantity")
        for orderIndex in range(len(orderProductIds)):
            productModel = self.data.stockRecordsHashTable.findData(orderProductIds[orderIndex])
            print(f"\t{productModel.getName()}    {orderProductQuantities[orderIndex]} piece(s)   Total: {productModel.getPrice() * orderProductQuantities[orderIndex]}")

        # append to records
        customerOrder.setCustomerId(customerId)
        customerOrder.setItems(orderProductIds)
        customerOrder.setItemQuantities(orderProductQuantities)

        # enqueue new customer order
        self.data.customerOrder.enqueue(customerOrder)