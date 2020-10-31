
class QuickSort:
    def __init__(self):
        pass

    def partition(self, listModel, start, last):
        pivot = listModel[start] # pivot is the first element
        low = start + 1
        high = last

        while True:
            # If the current value we're looking at is larger than the pivot
            # it's in the right place (right side of pivot) and we can move left,
            # to the next element.
            # We also need to make sure we haven't surpassed the low pointer, since that
            # indicates we have already moved all the elements to their correct side of the pivot
            while low <= high and listModel[high].methodForSort() >= pivot.methodForSort():
                high = high - 1

            # Opposite process of the one above
            while low <= high and listModel[low].methodForSort() <= pivot.methodForSort():
                low = low + 1

            # We either found a value for both high and low that is out of order
            # or low is higher than high, in which case we exit the loop
            if low <= high:
                listModel[low], listModel[high] = listModel[high], listModel[low]
                # The loop continues
            else:
                # We exit out of the loop
                break

        listModel[start], listModel[high] = listModel[high], listModel[start]

        return high

    def quick_sort(self, listModel, start, last):
        if start >= last:
            return

        pivotIndex = self.partition(listModel, start, last)
        self.quick_sort(listModel, start, pivotIndex - 1)
        self.quick_sort(listModel, pivotIndex + 1, last)