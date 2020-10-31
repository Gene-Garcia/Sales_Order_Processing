from Controller.Controller import Controller
from DataStructures.QuickSort import QuickSort
from Models.CustomerInformation import CustomerInformation

"""
GARCIA, Gene Joseph V
CS102-1L - Final Machine Problem

Sales Order Processing with the application of Data Structure and Algorithms

Data structures applied:
    1. Singly Linked List
    2. Queue Data Structure
    3. Quick Sort
    4. Hash Table
"""

"""
list = SinglyLinkedList()

    s1 = SalesOrder()
    s1.setSalesOrderId(1)
    s1.setCustomerId(1)
    s1.setDateFilled("Now")
    s1.setProductId(1)
    s1.setQuantity(5)
    s1.setShippingId(1)

    s2 = SalesOrder()
    s2.setSalesOrderId(2)
    s2.setCustomerId(2)
    s2.setDateFilled("Now")
    s2.setProductId(2)
    s2.setQuantity(6)
    s2.setShippingId(2)

    s3 = SalesOrder()
    s3.setSalesOrderId(3)
    s3.setCustomerId(3)
    s3.setDateFilled("Now")
    s3.setProductId(3)
    s3.setQuantity(7)
    s3.setShippingId(3)

    list.insertNode(s1)
    list.insertNode(s2)
    list.insertNode(s3)

    current = list.head
    while current != None:
        print(id(current))
        print("Sales Id", current.data.getSalesOrderId())
        current = current.next
        
    queue = Queue()
    s1 = SalesOrder()
    s1.setSalesOrderId(1)
    s1.setCustomerId(1)
    s1.setDateFilled("Now")
    s1.setProductId(1)
    s1.setQuantity(5)
    s1.setShippingId(1)

    s2 = SalesOrder()
    s2.setSalesOrderId(2)
    s2.setCustomerId(2)
    s2.setDateFilled("Now")
    s2.setProductId(2)
    s2.setQuantity(6)
    s2.setShippingId(2)

    s3 = SalesOrder()
    s3.setSalesOrderId(3)
    s3.setCustomerId(3)
    s3.setDateFilled("Now")
    s3.setProductId(3)
    s3.setQuantity(7)
    s3.setShippingId(3)

    queue.enqueue(s1)
    queue.enqueue(s2)
    queue.enqueue(s3)
    
    queue.dequeue()
    
    current = queue.front
    while current != None:
        print(id(current))
        print("Sales Id",current.data.getSalesOrderId())
        current = current.next
        
    hashT = HashTable(5)

    s1 = SalesOrder()
    s1.setSalesOrderId(1)
    s1.setCustomerId(1)
    s1.setDateFilled("Now")
    s1.setProductId(1)
    s1.setQuantity(5)
    s1.setShippingId(1)

    s2 = SalesOrder()
    s2.setSalesOrderId(2)
    s2.setCustomerId(2)
    s2.setDateFilled("Now")
    s2.setProductId(2)
    s2.setQuantity(6)
    s2.setShippingId(2)

    s3 = SalesOrder()
    s3.setSalesOrderId(3)
    s3.setCustomerId(3)
    s3.setDateFilled("Now")
    s3.setProductId(3)
    s3.setQuantity(7)
    s3.setShippingId(3)

    hashT.storeData(s3.getSalesOrderId(), s3)
    hashT.storeData(s2.getSalesOrderId(), s2)
    hashT.storeData(s1.getSalesOrderId(), s1)

    print(hashT.table)
    for index in hashT.table:
        if index != None:
            print(index.getSalesOrderId())
            
    c1 = CustomerInformation()
    c1.setCustomerId(1)
    c1.setName("ZRyan")
    c2 = CustomerInformation()
    c2.setCustomerId(2)
    c2.setName("Ross")
    c3 = CustomerInformation()
    c3.setCustomerId(3)
    c3.setName("Joee")
    c4 = CustomerInformation()
    c4.setCustomerId(4)
    c4.setName("Pheebs")
    c5 = CustomerInformation()
    c5.setCustomerId(5)
    c5.setName("Ash")

    sort = QuickSort()
    dataList = [c4, c5, c2, c1, c3]
    for data in dataList:
        print(data.getCustomerId(), data.getName())
    sort.sort(dataList, 0, len(dataList) - 1)
    for data in dataList:
        print(data.getCustomerId(), data.getName())
"""

def main():
    print("--__main__")



if __name__ == "__main__":
    main()