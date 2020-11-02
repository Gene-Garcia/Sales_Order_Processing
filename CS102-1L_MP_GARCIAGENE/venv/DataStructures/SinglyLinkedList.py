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

        if current != None:
            if current.data.methodForDelete() == data.data.methodForDelete():
                # first node
                # its okay even if current.next is none
                self.head = current.next
                return # does not run code below

        while current != None:
            if current.data.methodForDelete() == data.data.methodForDelete():
                break
            previous = current
            current = current.next

        if current != None:
            # current is the node to be deleted
            previous.next = current.next

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