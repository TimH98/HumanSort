from random import shuffle, randint

t = 0

def getChoice(op1, op2):
    """ Returns True for op1, False for op2 """
    #return cs([True, False])
    #return [op2, op1] == sorted([op1, op2])
    let1 = op1[0]
    let2 = op2[0]

    i = 0
    while (let1 == let2):
        i += 1
        let2 = op2[i]

    c = None
    while c != let1 and c != let2 and c != 'UNDO':
        c = input('[' + let1 + '] ' + op1 + ' or [' + let2 + '] ' + op2)

    return c == let1


def merge(lists, idx1, idx2):
    """ Merges lists[idx1] and lists[idx2]. Both lists are removed from items,
        returns the merged result.
        Assumes lists are ordered best to worst. """
    global t
    l1 = lists[idx1]
    l2 = lists[idx2]

    topList = []
    botList = []    # NOTE: botList is reversed - sorted from worst to best
    top = True

    while l1 and l2:
        # Alternate between taking from the top and bottom of the lists
        if top:
            op1 = l1[0]
            op2 = l2[0]
            # Take user's favorite and add it to the topList
            t += 1
            if getChoice(op1, op2):
                topList.append(op1)
                l1.remove(op1)
            else:
                topList.append(op2)
                l2.remove(op2)
        else:
            op1 = l1[-1]
            op2 = l2[-1]
            # Take user's least favorite and add it to the botList
            t += 1
            if not getChoice(op1, op2):
                botList.append(op1)
                l1.remove(op1)
            else:
                botList.append(op2)
                l2.remove(op2)
        top = not top

    if l1:
        topList.extend(l1)
    elif l2:
        topList.extend(l2)

    lists.pop(idx2)
    lists.pop(idx1)
    return topList + botList[::-1]


def main():
    items = [line.strip('\n') for line in open('input.txt')]

    pow2 = 1    # pow2 = largest power of 2 less than or equal to len(items)
    while pow2 <= len(items):
        pow2 *= 2
    pow2 //= 2

    lists = [[i] for i in items]
    shuffle(lists)

    # Get lists down to a power of 2
    i = 0
    while len(lists) > pow2:
        lists.append(merge(lists, i, i+1))

    newLists = []
    while len(lists) > 1:
        while len(lists) > 1:
            lists.sort(key=len)
            newLists.append(merge(lists, 0, len(lists)-1))
        lists = newLists
        newLists = []

    with open('output.txt', 'w+') as outfile:
        for i in lists[0]:
            outfile.write(i + '\n')


class HumanSort:
    def __init__(self):
        choice = ''
        while choice not in ['l', 'n']:
            choice = input('[L]oad or [N]ew? ').lower()

        self.items = []
        self.comps = []

        if choice == 'l':
            self.load()
        else:
            fname = input('Input file name: ')
            self.items = [line.strip('\n') for line in open(fname)]
            for i in range(len(self.items)):
                self.comps.append([0]*len(self.items))

        self.sort()

    def load(self):
        """
        File structure:
        <number of items>
        <items, one per line>
        <array of comps, items separated by spaces, rows separated by newlines>
        :return:
        """

    def sort(self):
        done = False
        while not done:
            x = 0
            y = 1
            while x == y or self.comps[x][y] != 0:
                x = randint(0, len(self.items))
                y = randint(0, len(self.items))

            high = self.getChoice(x, y)
            low = [x, y].remove(high)[0]
            


    def getChoice(self, x, y):
        """ Returns x, y, or save
            x and y are integers, indexes into the items list
        """
        op1 = self.items[x]
        op2 = self.items[y]
        let1 = op1[0].lower()
        let2 = op2[0].lower()

        i = 0
        while (let1 == let2):
            i += 1
            let2 = op2[i].lower()

        c = None
        while c.lower() not in [let1, let2, 'save']:
            c = input('[' + let1 + '] ' + op1 + ' or [' + let2 + '] ' + op2)

        if c.lower() == let1:
            return x
        elif c.lower() == let2:
            return y
        else:
            return c


if __name__ == '__main__':
    hs = HumanSort()
    #main()
    """
    avg = 0
    for i in range(100):
        main()
        avg += t
        t = 0
    avg /= 100
    print(avg)
    """
