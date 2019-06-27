from random import shuffle, choice as cs

t = 0

def getChoice(op1, op2):
    """ Returns True for op1, False for op2 """
    #return cs([True, False])
    return [op2, op1] == sorted([op1, op2])
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
    """ Merges lists[idx1] and lists[idx2]. List 2 will be removed from items,
        List 1 will hold the merged result.
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

    lists[idx1] = topList + botList[::-1]
    lists.pop(idx2)


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
        merge(lists, i, i+1)

    while len(lists) > 1:
        lists.sort(key=len)     # TODO: I think this needs to be more robust - have a list move up a tier after being merged
        merge(lists, 0, 1)

    with open('output.txt', 'w+') as outfile:
        for i in lists[0]:
            outfile.write(i + '\n')


if __name__ == '__main__':
    avg = 0
    for i in range(100):
        main()
        avg += t
        t = 0
    avg /= 100
    print(avg)
