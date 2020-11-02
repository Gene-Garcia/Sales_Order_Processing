from Helpers.InputHelper import InputHelper
from Helpers.DataHelper import DataHelper
from Helpers.ASCIIHelper import ASCIIHelper

from Models.CustomerOrder import CustomerOrder
from Models.SalesOrder import SalesOrder
from Models.CustomerInformation import  CustomerInformation

from datetime import date

class Controller:

    def __init__(self):
        print("--Controller")

        data = DataHelper()
        data.populate()
        self.data = data

        self.showMainMenu()

    def showMainMenu(self):
        while True:
            print("""
    1 Take customer's order
    2 Create sales order
    3 Process back orders
    4 Ship orders
    5 Bill customer # also insert record in Sales Journal
    6 Display records
    0 Terminate program""")
            menuSelection = InputHelper.integerInputWithChoices("Select from menu", [1, 2, 3, 4, 5, 6, 0])
            print()

            if menuSelection == 1:
                self.takeCustomerOrder()

            elif menuSelection == 2:
                self.createSalesOrder()

            elif menuSelection == 0:
                print("\n\tTerminating program...")
                break

    def showDisplayMenu(self):
        """
        1 Customer information
        2 Sales journal records
        3 Shipping log
        """
        pass

    def createSalesOrder(self):
        print("\tPROCESSING CUSTOMER ORDER TO SALES ORDERS\n")
        toProcess = self.data.customerOrder.dequeue()

        if toProcess:
            toProcess = toProcess.data
            # check if customer order's customer
            customerModel = self.data.custInfoHashTable.findData(ASCIIHelper.toASCII(toProcess.getCustomerName()))

            if customerModel != None:
                # reconsile and check amount payables and credit limit

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
            print("\tEmpty Queue of Customers orders")

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