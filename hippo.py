import time

from persist import Persister
import core

#  - add item
#  - remove item
#  - I guess list items as well
#  - get me n items for review:
#  - I guess we need another command for when dependencies are not met, something like "put item on hold", or "temporarily skip"

# the "get me n items for review" command uses a spaced repetition scheduler
# based (loosely) on the SM-2 algorithm

# the scheduler should do something like:
#  - look at all items' "last reviewed" dates (specifically time delta between now and then)
#  - compare with the IRI
#  - determine a) how many are ready for review, and b) order them by "most overdue"
# I think it (the backend function) should emit a generator for item ids, actually.
# there should be another function that calls it and handles user interaction and skipping


def get_time():
    return round(time.time())

# my attempt at the imperative shell. this delegates to the core for logic, keeps state and mutates the world as needed
class Conductor:
    def __init__(self):
        self.persister = Persister()

    def add_item(self, desc):
        item = core.init_item(desc)
        item['last_reviewed'] = get_time()
        new_id = self.persister.add_item(item)
        print("Item {} has been added".format(new_id))


    def remove_item(self, item_id):
        self.persister.remove_item(item_id)
        print("Item {} has been removed".format(item_id))


    def list_items(self, pattern=None):
        print(self.persister.get_items())

    def review(self, n):
        print(self.persister.get_items())
