"""hippo

Usage:
  hippo.py [--N=<n>]
  hippo.py add <description>
  hippo.py edit <id> <description>
  hippo.py view <id>
  hippo.py remove <id>
  hippo.py list

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt

import time

from persist import Persister
import core


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

    def edit_item(self, item_id, desc):
        self.persister.change_item_desc(item_id, desc)
        print("Item {}'s description has been updated".format(item_id))

    def view_item(self, item_id):
        item = self.persister.get_item(item_id)
        print(item)

    def remove_item(self, item_id):
        self.persister.remove_item(item_id)
        print("Item {} has been removed".format(item_id))

    def list_items(self, pattern=None):
        for item in self.persister.get_items():
            print(core.list_display_item(item))

    def review(self, n):
        print("Reviewing {} items".format(n))
        items = core.review_filter_items(self.persister.get_items(), get_time())
        reviewed = 0

        while reviewed < n:
            curr = next(items)

            while True:
                print('\n'+core.list_display_item(curr)+'\n')
                inp = input(core.review_item_prompt())

                if inp in 'qs012345':
                    break
                else:
                    print("\nInvalid input")

            if inp == 'q':
                break
            elif inp == 's':
                continue
            else:
                new_item = core.assess_item(curr, int(inp))
                new_item['last_reviewed'] = get_time()
                self.persister.update_item(new_item)


if __name__ == '__main__':
    args = docopt(__doc__, version='hippo 0.1')
    cond = Conductor()

    default_review_num = 20

    if args['add']:
        cond.add_item(args['<description>'])
    elif args['edit']:
        cond.edit_item(args['<id>'], args['<description>'])
    elif args['view']:
        cond.view_item(args['<id>'])
    elif args['remove']:
        cond.remove_item(args['<id>'])
    elif args['list']:
        cond.list_items()
    else:
        if args['--N'] is not None:
            cond.review(args['--N'])
        else:
            cond.review(default_review_num)
