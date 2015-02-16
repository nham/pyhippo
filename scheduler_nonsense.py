# This is based loosely on the SM-2 algorithm by Piotr Wozniak. The biggest
# differences all stem from the fact that I am not using flashcards. Each
# item in the system is a concept or a theorem or idea or something similar. # The intention is that this program will handle my review schedule for my 
# notes, which mostly consist of stuff about the math I'm learning.

# It seems to me that learning math presents unique challenges that cannot
# be incorporated into a flash card system a la SuperMemo/Anki/Mnemosyne.
# Mathematics is highly hierarchical. E.g. it makes no sense to review the
# proof of a theorem about locally path-connected spaces if you've forgotten
# the definition, which would presumably be another card. So it seems you
# either need to introduce dependencies between flash cards, which seems
# to be too complicated, or abandon the flash card format.



# the mechanism of "review something every day until it sticks reasonably
# well" seems right to me, but I'm not sure the intStep mechanism should
# be preserved here?

class Scheduler:
    # qualities less than this mean recall failed, so intStep is reset
    CORRECT_RECALL_QUALITY = 2 

    # TODO: think about why this value is used and whether I should change it to
    # something else
    INITIAL_EF = 2.5

    # in the original SM-2 algorithm this is 6. I decided to make it
    # much smaller because the items I will be reviewing are not flash
    # cards, and will sometimes be bigger since they violate the
    # "minimum information principle"
    SECOND_INTERVAL = 3

    # EF cannot be less than this (see updateEF)
    # From the SM-2 algorithm description by Wozniak:
    #
    #  > Shortly after the first SuperMemo program had been implemented, I 
    #  > noticed that E-Factors should not fall below the value of 1.3.
    #  > Items having E-Factors lower than 1.3 were repeated annoyingly
    #  > often and always seemed to have inherent flaws in their formulation
    #  > (usually they did not conform to the minimum information principle)."
    #
    # so this may require tweaking
    EF_FLOOR = 1.3

    # quality is the rating the user gives when reviewing each item.
    # 0 quality means the item's contents were totally forgotten,
    # 1 means the item was somewhat familiar but still not recalled
    # and so on. the highest possible quality is MAX_QUALITY, meaning
    # there are (MAX_QUALITY + 1) different ratings available for use
    # in mnemosyne, MAX_QUALITY = 5
    MAX_QUALITY = 5

    def __init__(self, modules):
        self.intStep = 1
        self.I = 1 # inter-repetition interval after the (intStep)-th repetition (in days)
        self.EF = self.INITIAL_EF # easiness factor

        super().__init__(modules)


    def updateI(self):
        if intStep == 1:
            self.I = 1
        elif intStep == 2:
            self.I = self.SECOND_INTERVAL
        else:
            self.I *= EF

    def updateEF(self, quality):
        # the original adjustment polynomial is:
        #
        #   -0.02 x^2 - 0.08 x + 0.1
        #
        # where x = (5 - quality), originally
        # here's what this amounts to:
        #
        # q | EF adjustment
        # ------------------
        # 0 | -0.8
        # 1 | -0.54
        # 2 | -0.32
        # 3 | -0.14
        # 4 | 0
        # 5 | 0.1
        #
        # these were empirically adjusted over multiple years by the SuperMemo guy,
        # but I'm just going to make something that kinda resembles it
        # also, I'm going to just use a lookup table.
        adjust = [-0.8, -0.54, -0.32, -0.14, 0, 0.1]

        self.EF += adjust[quality]

        if self.EF < self.EF_FLOOR:
            self.EF = self.EF_FLOOR

    def update(self, quality):
        assert quality >= 0 and quality <= self.MAX_QUALITY
        self.updateEF(quality)

        # if the user failed recall, reset the intStep. it is as if we are trying
        # to memorize it anew
        if quality < self.CORRECT_RECALL_QUALITY:
            self.intStep = 1
        else:
            self.intStep += 1
            self.updateI()
