from DataStructures.SinglyNode import SNode

class Queue:

    def __init__(self):
        self.front = None # head, out
        self.rear = None # in

    def enqueue(self, data):
        newQueue = SNode()
        newQueue.data = data

        #print("\tEnqueue-ing", data)
        if self.rear == None and self.front == None:
            # empty queue
            self.front = newQueue
            self.rear = newQueue
        else:
            # non-empty queue
            # traverse to go to the end of the list
            current = self.front
            while current.next != None:
                current = current.next
            current.next = newQueue
            self.rear = newQueue

    def dequeue(self):
        if self.front == None:
            # empty
            # print("\tempty Queue")
            return None
        else:
            # print("\tDequeue-ing")
            toDequeue = self.front

            # non-empty queue
            if self.front.next == None:
                # last queued item
                self.front = None
                self.rear = None
            else:
                # more than one in the queue
                self.front = self.front.next

            return toDequeue

    def front(self):
        if self.front != None:
            return self.front.data
        return None

    def rear(self):
        if self.rear != None:
            return self.rear.data
        return None

    def printQueue(self):
        current = self.front

        print("\tQueue", end=" > ")
        while current != None:
            print(f"{current.element}", end=" - ")
            current = current.next
        print("\n")