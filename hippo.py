class Module:
    def __init__(self, content):
        self.active = True


class Scheduler:
    # qualities less than this mean recall failed, so intStep is reset
    CORRECT_RECALL_QUALITY = 2 

    # TODO: think about why this value is used and whether I should change it to
    # something else
    INITIAL_EF = 2.5

    SECOND_INTERVAL = 6

    # EF cannot be less than this (see updateEF)
    EF_FLOOR = 1.3

    # quality is the rating the user gives when reviewing each item.
    # 0 quality means the item's contents were totally forgotten,
    # 1 means the item was somewhat familiar but still not recalled
    # and so on. the highest possible quality is MAX_QUALITY, meaning
    # there are (MAX_QUALITY + 1) different ratings available for use
    # in mnemosyne, MAX_QUALITY = 5, but I'm trying it with 4
    MAX_QUALITY = 4

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
        adjust = [-0.75, -0.45, -0.2, 0, 0.1]

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
