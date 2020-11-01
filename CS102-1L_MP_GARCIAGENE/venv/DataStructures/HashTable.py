# data is the key to be hashed
# model is the data to be stored in the table[key] = model
class HashTable:
    def __init__(self, m):
        self.m = m # size of the table
        self.table = [None for x in range(m)] # populate index with None

    def storeData(self, data, model):
        # true if key is in the table is not taken, otherwise false

        # get key
        key = self.__getKey(data)
        if self.table[key] != None:
            # collision
            key = self.__linearProbing(data)

        # store model to table
        self.table[key] = model

    def __getKey(self, data):
        # formula h(k) = k mod m
        key = data % self.m
        return key

    def __linearProbing(self, data):
        # h(k) = k mod m + 1
        # h(k) = k mod m + 2
        # ...

        probeCtr = 1
        while True:
            key = self.__getKey(data) + probeCtr

            if key >= self.m:
                # out of bounds
                # go back to 0
                key = key - self.m
            if self.table[key] == None:
                return key
            probeCtr += 1

    def findData(self, data):
        key = self.__getKey(data)

        # key not in table
        if self.table[key] == None:
            return False

        # check value
        if self.table[key].methodForHashTable() == data:
            return self.table[key] # data found

        # linear probe the data
        # the key might be on the succeeding indexes
        for i in range(self.m):
            key = self.__linearProbing(data)

            # check value
            if self.table[key] != None:
                if self.table[key].methodForHashTable() == data:
                    return self.table[key]  # data found

        # not found
        return False