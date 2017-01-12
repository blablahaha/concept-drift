"""Adaptive Sliding Window"""
from concept_dirft.adwin_list import AdwinList


class Adwin():
    def __init__(self, delta=0.01, max_buckets=5, min_clock=32):
        """
        :param delta:confidence value
        :param max_buckets:max number of buckets which have same number of original date in one row
        :param min_clock:min number of new data to reduce window and detect change
        """
        self.delta = delta,
        self.max_buckets = max_buckets
        self.min_clock = min_clock
        self.count = 0
        self.width = 0
        self.total = 0
        self.variance = 0
        self.bucket_number = 0
        # last_bucket_row: defines the max number of merged
        self.last_bucket_row = 0
        self.list_row_buckets = AdwinList(self.max_buckets)

    def set_input(self, value):
        self.count += 1
        # Insert the new element
        self.__insert_element(value)

    def __insert_element(self, value):
        self.width += 1
        internal_variance = 0
        # Insert the new bucket
        self.list_row_buckets.head.insert_bucket(value, 0)
        self.bucket_number += 1
        # Calculate the internal_variance
        if self.width > 1:
            internal_variance = (self.width - 1) * (
                (value - self.total / (self.width - 1)) * (value - self.total / (self.width - 1))
            ) / self.width
        self.variance += internal_variance
        self.total += value
        self.__compress_buckets()

    def __compress_buckets(self):
        """Merging two buckets corresponds to creating a new bucket whose size is equal to
        the sum of the sizes of those two buckets.
        The size of bucket means that it contains how many original data
        """
        cursor = self.list_row_buckets.head
        i = 0
        while cursor is not None:
            # Find the number of buckets in a row
            k = cursor.bucket_size_row
            # Merge buckets if row is full
            if k == self.max_buckets + 1:
                next_node = cursor.next
                if next_node is None:
                    self.list_row_buckets.add_to_tail()
                    next_node = cursor.next
                    self.last_bucket_row += 1

                n1 = pow(2, i)
                n2 = pow(2, i)
                u1 = cursor.bucket_total[0] / n1
                u2 = cursor.bucket_total[1] / n2
                internal_variance = n1 * n2 * (u1 - u2) * (u1 - u2) / (n1 + n2)
                next_node.insert_bucket(cursor.bucket_total[0] + cursor.bucket_total[1],
                                        cursor.bucket_variance[0] + cursor.bucket_variance[1] + internal_variance)
                self.bucket_number += 1
                cursor.compress_buckets_row(2)
                if next_node.bucket_size_row <= self.max_buckets:
                    break
            else:
                break
            cursor = cursor.next
            i += 1
