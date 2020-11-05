class PrimeHelper:

    @staticmethod
    def findNearestPrime(m):
        """m is the length of the data"""
        while True:
            m += 1
            if PrimeHelper.isPrime(m):
                return m

    @staticmethod
    def isPrime(number):
        if number > 1:
            # check for factors
            for i in range(2, number):
                if (number % i) == 0:
                    return False
            else:
                return True

        else:
            return False