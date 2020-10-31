
class QuickSort:
    def __init__(self):
        pass

    def partition(self, listModel, firstIndex, lastIndex):
        pivot = listModel[firstIndex] # pivot is the first element
        low = firstIndex + 1 # +1 because the predeccessor index is taken as pivot
        high = lastIndex

        while True:
            # check each data starting from the last index (high)
            # as long as the data are greater than or = to the pivot
            # it stays at the right side of the pivot
            # however not yet sorted
            while low <= high and listModel[high].methodForSort() >= pivot.methodForSort():
                high = high - 1

            # check each data starting from the first index
            # as long as the traversed data are lower than the pivot
            # it stays at the left side
            # also not sorted
            while low <= high and listModel[low].methodForSort() <= pivot.methodForSort():
                low = low + 1

            # if it reaches here, the loop at the top is break and
            # this shows that listmodel[low] is greater than listmodel[high]
            # perform switch
            # continue loop
            # low <= high ensure that the whole partition is not yet traverse
            # otherwise, low > high, break the loop
            if low <= high:
                listModel[low], listModel[high] = listModel[high], listModel[low]
            else:
                break

        # we swap the pivot which is the first index to the last position of high
        # which means
        # the predeccessor values on the left of high
        # are all less than the pivot
        # eg. [29, 94,27,41,66,28,10], 29 is pivot
        # after traversal and swapping [29 10,27,[28],66,41,94]
        # the last position of high is at the index of 28, thus 29 and 28 will be switched
        # 29 is the latest pivot value and partitioning index
        listModel[firstIndex], listModel[high] = listModel[high], listModel[firstIndex]

        return high

    def sort(self, listModel, firstIndex, lastIndex):
        if firstIndex >= lastIndex:
            return
        pivotIndex = self.partition(listModel, firstIndex, lastIndex)
        self.sort(listModel, firstIndex, pivotIndex - 1)
        self.sort(listModel, pivotIndex + 1, lastIndex)