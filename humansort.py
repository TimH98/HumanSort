from random import shuffle, randint


class HumanSort:
    """
    self.comps[x][y] =
        -1 if x < y
        1 if x > y
    """
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

    def load(self):
        """
        File structure:
        <number of items>
        <items, one per line>
        <array of comps, items separated by spaces, rows separated by newlines>
        :return:
        """
        fname = input("Load file name: ")

        with open(fname, 'r') as infile:
            nitems = int(infile.readline()[:-1])
            for i in range(nitems):
                self.items.append(infile.readline()[:-1])
            for i in range(nitems):
                lst = infile.readline()[:-1].split(' ')
                self.comps.append([int(i) for i in lst])


    def save(self):
        fname = input("Save file name: ")
        with open(fname, 'w+') as outfile:
            outfile.write(str(len(self.items)) + '\n')
            outfile.write('\n'.join(self.items) + '\n')
            for row in self.comps:
                outfile.write(' '.join([str(i) for i in row]) + '\n')

    def output(self):
        items = []

        for i, name in enumerate(self.items):
            items.append({'name': name, 'score': sum(self.comps[i])})

        items.sort(key=lambda x: x['score'], reverse=True)

        fname = input('Output file name: ')
        with open(fname, 'w+') as outfile:
            for item in items:
                outfile.write(item['name'] + '\n')

    def sort(self):
        done = False
        while not done:
            x = 0
            y = 0
            while x == y or self.comps[x][y] != 0:
                x = randint(0, len(self.items)-1)
                y = randint(0, len(self.items)-1)

            resp = self.getChoice(x, y)
            if resp == 'save':
                return 'save'
            high = resp
            if high == x:
                low = y
            else:
                low = x
            self.comps[high][low] = 1
            self.comps[low][high] = -1
            self.checkCascade(high, low)

            done = self.checkDone()
        return 'done'

    def checkCascade(self, high, low):
        for i in range(len(self.items)):
            if i not in [high, low]:
                if self.comps[i][high] > 0:
                    self.comps[i][low] = 1
                    self.comps[low][i] = -1
                if self.comps[i][low] < 0:
                    self.comps[i][high] = -1
                    self.comps[high][i] = 1

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

        c = ''
        while c.lower() not in [let1, let2, 'save']:
            c = input('[' + let1 + '] ' + op1 + ' or [' + let2 + '] ' + op2 + '\n')

        if c.lower() == let1:
            return x
        elif c.lower() == let2:
            return y
        else:
            return c

    def checkDone(self):
        for x in range(len(self.items)):
            for y in range(len(self.items)):
                if x != y and self.comps[x][y] == 0:
                    return False
        return True


if __name__ == '__main__':
    hs = HumanSort()
    resp = hs.sort()
    if resp == 'save':
        hs.save()
    elif resp == 'done':
        hs.output()
