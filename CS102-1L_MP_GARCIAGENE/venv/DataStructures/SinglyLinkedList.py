from DataStructures.SinglyNode import SNode

# data is model
class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insertNode(self, data):
        newNode= SNode();
        newNode.data = data

        if self.head == None:
            # empty list
            self.head = newNode

        else:
            # non-empty list
            current = self.head
            # get the last node
            while current.next != None:
                current = current.next

            # insert node to be the next node of the last node
            current.next = newNode

    def deleteNode(self, data):
        # find node
        current = self.head

        # check if head is equals to data
        if current.data != data:
            while current != None:
                if current.next != None:
                    if current.next.data == data:
                        break
                current = current.next

        if current != None:
            # node found
            if current.data == self.head.data:
                # first node
                self.head = current.next

            elif current.next != None:
                # middle node
                current.next = current.next.next

            else:
                # last node
                current.next = None

        else:
            # node not found or list empty
            pass

    def traverseNode(self):
        current = self.head
        print("List")
        while current != None:
            print(current.data, end="->")
            current = current.next

    def convertToList(self):
        convertedList = []

        current = self.head
        while current != None:
            convertedList.append(current)
            current = current.next

        return convertedList