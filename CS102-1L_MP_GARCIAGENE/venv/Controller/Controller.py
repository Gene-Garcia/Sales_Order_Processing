from Helpers.InputHelper import InputHelper
from Helpers.DataHelper import DataHelper
from Helpers.ASCIIHelper import ASCIIHelper

from DataStructures.QuickSort import QuickSort

from Models.CustomerOrder import CustomerOrder
from Models.SalesOrder import SalesOrder
from Models.CustomerInformation import  CustomerInformation
from Models.ShipmentDetails import ShipmentDetails
from Models.JournalEntry import JournalEntry
from Models.Product import Product

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
            print("\n\t1 Take customer's order")
            print("\t2 Create sales order")
            print("\t3 Process back orders")
            print("\t4 Ship orders")
            print("\t5 Bill customer")
            print("\t6 Display records")
            print("\t7 Other Menu")
            print("\t0 Terminate program")
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
        print("\n\t1 Customer information")
        print("\t2 Sales journal records")
        print("\t3 Shipping log")
        menuSelection = InputHelper.integerInputWithChoices("Select from display menu", [1, 2, 3])
        print()

        if menuSelection == 1:
            self.displayCustomers()

        elif menuSelection == 2:
            self.displaySalesJournals()

        elif menuSelection == 3:
            self.displayShippingLog()

    def showOtherMenu(self):
        print("\n\t1 Add Customer")
        print("\t2 Add Product")
        print("\t3 Increase Product Stock")
        print("\t4 Mark Order sa Paid")
        print("\t5 Mark Order as Delivered")
        menuSelection = InputHelper.integerInputWithChoices("Select from other menu", [1, 2, 3, 4, 5])
        print()

        if menuSelection == 1:
            self.addCustomer()

        elif menuSelection == 2:
            self.addProduct()

        elif menuSelection == 3:
            self.increaseProductStock()

        elif menuSelection == 4:
            self.markOrderAsPaid()

        elif menuSelection == 5:
            self.markOrderAsDelivered()

    def findShippingDetails(self, shippingIdToSearch):
        shippingDetail = self.data.shippingLog.head
        while shippingDetail != None:
            if shippingDetail.data.getShippingId() == shippingIdToSearch:
                break
            shippingDetail = shippingDetail.next

        return shippingDetail

    def recordSalesOrder(self, salesOrder, customerModel, productModel):
        # check if stock inventory is enough for the order
        if salesOrder.getQuantity() <= productModel.getStock():

            # check customer's credit limit and current payable
            totalSales = salesOrder.getQuantity() * productModel.getPrice()
            if (customerModel.getAmountPayable() + totalSales) >= customerModel.getCreditLimit():
                # file in back order file
                self.data.backOrderFile.enqueue(salesOrder)
                print("\n\tSales Order Queued in Back Order File because customer has maxed out their credit limit worh PHP",
                      customerModel.getCreditLimit(), "\n")

            else:
                # reduce stock
                productModel.setStock(productModel.getStock() - toProcess.getItemQuantities()[orderIndex])
                # file in open order file
                self.data.openOrderFile.enqueue(salesOrder)
                print("\n\tSales Order Queued in Open Order File Successfully\n")

        else:
            # file in back order file
            self.data.backOrderFile.enqueue(salesOrder)
            print("\n\tSales Order Queued in Back Order File Due to insufficient quantity\n")

    # other menu
    def addCustomer(self):
        print("\t>>> ADD NEW CUSTOMER RECORD <<<\n")

        # get name
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
        # check if product name is existing

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

            productModel.setStock( productModel.getStock() + stocks )

        else:
            print("\tThere are currently no stock records to increase")

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

                print("\t\tSales Journal Summary")
                journalEntry.displaySummary()

                customerModel = self.data.custInfoHashTable.findData(journalEntry.getSalesOrder().getCustomerId())
                print("\tCustomer name", customerModel.getName())

                productModel = self.data.stockRecordsHashTable.findData(journalEntry.getSalesOrder().getProductId())
                print("\tProduct Name", productModel.getName())
                print()

            if len(salesJournalIds) > 0:
                # select a sales journal
                selectedSalesJournalId = InputHelper.integerInputWithChoices("Select a sales journal Id", salesJournalIds)

                # find sales journal using the selectedSalesJournalId in hash table
                salesJournal = self.data.journalHashTable.findData(selectedSalesJournalId)

                print("\n\t\tSelected Sales Journal")
                salesJournal.data.displaySummary()

                customerModel = self.data.custInfoHashTable.findData(salesJournal.data.getSalesOrder().getCustomerId())
                print("\tCustomer name", customerModel.getName(), customerModel.getAmountPayable())

                productModel = self.data.stockRecordsHashTable.findData(salesJournal.data.getSalesOrder().getProductId())
                print("\tProduct Name", productModel.getName())

                # update sales journal
                salesJournal.data.setPaymentStatus(True)
                salesJournal.data.setDatePaid(date.today())

                # recomppute customer's amount payable
                salesAmount = salesJournal.data.getSalesOrder().getQuantity() * productModel.getPrice()
                customerModel.setAmountPayable( customerModel.getAmountPayable() - salesAmount  )

            else:
                print("\tAll the current sales orders are paid by the customers")

        else:
            print("\tThere currently no sales journal record")

    def markOrderAsDelivered(self):
        print("\t>>> MARK ORDER AS DELIVERED <<<\n")

        # display shipping log
        # select as shipping id
        # set as delivered

        shippingIds = []

        shippingDetail = self.data.shippingLog.head
        while shippingDetail != None:
            if shippingDetail.data.getDateDelivered() == None:
                shippingIds.append(shippingDetail.data.getShippingId())
                print("\t\tShipping Detail Summary")
                shippingDetail.data.displaySummary()
                print()

            shippingDetail = shippingDetail.next

        selectedShippingId = InputHelper.integerInputWithChoices("Select a shipping Id to be marked as delivered", shippingIds)

        """shippingDetail = self.data.shippingLog.head
        while shippingDetail != None:
            if shippingDetail.data.getShippingId() == selectedShippingId:
                break
            shippingDetail = shippingDetail.next"""

        # find shipping detail model
        shippingDetail = self.findShippingDetails(selectedShippingId)

        if shippingDetail != None:
            # set as delivered
            shippingDetail.data.setDateDelivered(date.today())

            print("\tShipping log record with id ", selectedShippingId, "is set as delivered as of", shippingDetail.data.getDateDelivered())

    # display menu
    def displayCustomers(self):
        print("\t>>> DISPLAY CUSTOMER INFORMATION SORT BY CUSTOMER NAME <<<\n")

        if self.data.customerInformation.head != None:

            customerList = self.data.customerInformation.convertToList()
            quicksort = QuickSort()
            quicksort.sort(customerList, 0, len(customerList) - 1)

            # display
            for customer in customerList:
                print("\t\tCustomer Information Summary")
                customer.data.displaySummary()
                print()

        else:
            print("\tThere are currently no recorded customer")

    def displaySalesJournals(self):
        print("\t>>> DISPLAY SALES JOURNALS SORT BY DATE COMPLETED <<<\n")

        if self.data.salesJournal.head != None:

            journalList = self.data.salesJournal.convertToList()
            quicksort = QuickSort()
            quicksort.sort(journalList, 0, len(journalList) - 1)

            # display
            for journal in journalList:
                print("\t\tSales Journal Entry Summary")
                journal.data.displaySummary()
                print()

        else:
            print("\tThere are currently no recorded sales journal")

    def displayShippingLog(self):
        print("\t>>> DISPLAY SHIPPING LOG SORT BY DATE <<<\n")

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

                print("\t\tShipping Log Summary")
                shippingDetail.data.displaySummary()
                if salesOrder == None:
                    # already billed
                    print("\tSales order of this shipping log is already recorded in the sales journal")
                else:
                    print("\t\tSales Order Summary")
                    salesOrder.data.displaySummary()
                print()

        else:
            print("\tThere are currently no recorded shipping log")

    # main menu
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

            """shippingDetail = self.data.shippingLog.head
            while shippingDetail != None:
                if shippingDetail.data.getShippingId() == salesOrder.data.getShippingId():
                    break
                shippingDetail = shippingDetail.next"""

            # find shipmentdetails using salesOrder's
            shippingDetail = self.findShippingDetails(salesOrder.data.getShippingId())

            # create journal entry
            journalEntry = JournalEntry()
            # shipping model date delivered
            journalEntry.setDateCompleted(shippingDetail.data.getDateShipped())
            print("\tDate Completed", shippingDetail.data.getDateShipped())
            journalEntry.setJournalId(JournalEntry.getId())
            journalEntry.setSalesOrder(salesOrder.data)

            # record journal entry
            self.data.salesJournal.insertNode(journalEntry)

            # insert to hash table
            self.data.journalHashTable.storeData(journalEntry.methodForHashTable(), journalEntry)

            # re-compute customers credit payable
            salesPrice = productModel.getPrice() * salesOrder.data.getQuantity()
            customerModel.setAmountPayable( customerModel.getAmountPayable() + salesPrice )

            print("\n\tCustomer", customerModel.getName(), "billed with sales order #", salesOrder.data.getSalesOrderId())
            print("\tCurrent amount payable of customer is PHP", customerModel.getAmountPayable())

        else:
            print("\tThere are currently no sales orders to be billed")

    def shipOrders(self):
        print("\t>>> SHIP ORDERS <<<\n")

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
        print("\t>>> PROCESSING BACK ORDERS <<<\n")
        # already a sales order
        salesBackOrder = self.data.backOrderFile.dequeue()

        if salesBackOrder != None:
            salesBackOrder = salesBackOrder.data

            # find in hash table
            customerModel = self.data.custInfoHashTable.findData(salesBackOrder.getCustomerId())

            if customerModel != None:
                """"# reconsile and check amount payables and credit limit"""

                productModel = self.data.stockRecordsHashTable.findData(salesBackOrder.getProductId())
                if productModel != None:
                    print("\tSales Order for", salesBackOrder.getCustomerId(), customerModel.getName())
                    salesBackOrder.displaySummary()
                    print("\tTotal cost in PHP", productModel.getPrice() * salesBackOrder.getQuantity())

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
                """"# reconsile and check amount payables and credit limit"""

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

                        # display sales order
                        print("\tSales Order for", salesOrder.getCustomerId(), customerModel.getName())
                        salesOrder.displaySummary()

                        totalSales = productModel.getPrice() * toProcess.getItemQuantities()[orderIndex]
                        print("\tTotal cost of", productModel.getName(),"in PHP", totalSales)

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
        customerModel = self.data.customerInformation.head
        while customerModel != None:
            customerIdList.append(customerModel.data.getCustomerId())
            customerModel.data.displaySummary()
            print()
            customerModel = customerModel.next

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

        # append to records
        customerOrder.setItems(orderProductIds)
        customerOrder.setItemQuantities(orderProductQuantities)

        # enqueue new customer order
        self.data.customerOrder.enqueue(customerOrder)