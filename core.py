INITIAL_FF = 2.5

def init_item(desc):
    return {
            'desc': desc,
            'ff': INITIAL_FF,
            'int_step': 0,
            'iri': 0.0
           }

def assess_item(item, fam):
    """item is a dict of the form:

       {
         'id': <int>,
         'desc': <string>,
         'last_review': <a datetime of some sort>,
         'ff': <float>,
         'int_step': <int>,
         'iri': <float>
       }

       "ff" is familiarity factor, which I like better than the "easiness
       factor" of SM-2.

        "iri" is inter-repetition interval"""

    if fam < 2:
        item['int_step'] = 1
    else:
        item['int_step'] += 1

    if item['int_step'] == 1:
        item['iri'] = 1.0
    elif item['int_step'] == 2:
        item['iri'] = 3.0 # 6.0 in SM-2, I'm trying 3.0
    else:
        item['iri'] += item['ff']

    # SM-2 algorithm says only to adjust if familiar was above a certain
    # threshold. haven't thought about what effect this has yet. 
    # TODO: revisit
    if fam >= 2:
        ff_adjust = [-0.8, -0.54, -0.32, -0.14, 0, 0.1]
        item['ff'] += ff_adjust[fam]

    return item

def list_display_item(item):
    return "{:3} : {}".format(item['id'], item['desc'])
