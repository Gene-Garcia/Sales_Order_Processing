from Controller.Controller import Controller

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
"""

def main():
    print("--__main__")

if __name__ == "__main__":
    main()