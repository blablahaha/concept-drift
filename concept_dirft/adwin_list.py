"""Add new bucket at head of window (which has smaller number of merged),
remove old bucket from tail of window (which has bigger number of merged)
"""
from concept_dirft.adwin_list_item import AdwinListItem


class AdwinList:
    def __init__(self, max_bucket_element=5):
        """
        :param max_bucket_element:max number of element in each bucket
        """
        self.count = 0
        self.max_bucket_element = max_bucket_element
        self.head = None
        self.tail = None
        self.add_to_head()

    def add_to_head(self):
        """Add the object at the beginning of the window
        """
        self.head = AdwinListItem(self.max_bucket_element, next=self.head)
        if self.tail is None:
            self.tail = self.head
        self.count += 1

    def add_to_tail(self):
        """Add the object at the end of the window
        """
        self.tail = AdwinListItem(self.max_bucket_element, previous=self.tail)
        if self.head is None:
            self.head = self.tail
        self.count += 1

    def remove_from_tail(self):
        """Remove the last object in the window
        """
        self.tail = self.tail.previous
        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None
        self.count -= 1
