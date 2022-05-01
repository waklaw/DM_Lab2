from prettytable import PrettyTable


def getFile():
    text = []
    with open("data.txt", "r") as file:
        lines = file.readlines()
        for i in lines:
            text.append(i.replace('\n', ''))
    for i in range(len(text)):
        text[i] = text[i].split(" ")
    return text


def dijktra(matrix, source, dest):
    global ind
    shortest = [0 for i in range(len(matrix))]
    selected = [source]
    N = len(matrix)

    inf = 9999999
    min = inf
    for i in range(N):
        if (i == source):
            shortest[source] = 0
        else:
            if (matrix[source][i] == 0):
                shortest[i] = inf
            else:
                shortest[i] = matrix[source][i]
                if (shortest[i] < min):
                    min = shortest[i]
                    ind = i

    if (source == dest):
        return 0

    selected.append(ind)
    while (ind != dest):
        for i in range(N):
            if i not in selected:
                if (matrix[ind][i] != 0):
                    if ((matrix[ind][i] + min) < shortest[i]):
                        shortest[i] = matrix[ind][i] + min
        tempMin = 9999999
        for i in selected:
             print(i, '-> ', end='')

        print('')

        for j in range(N):
            if j not in selected:
                if (shortest[j] < tempMin):
                    tempMin = shortest[j]
                    ind = j
        min = tempMin
        selected.append(ind)

    return shortest[dest]


def getOdd(matrix):
    degrees = [0 for i in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] != 0:
                degrees[i] += 1

    odds = [i for i in range(len(degrees)) if degrees[i] % 2 != 0]
    print('Not even nodes:', odds)

    return odds


def createPairs(odds):
    pairs = []
    for i in range(len(odds) - 1):
        pairs.append([])
        for j in range(i + 1, len(odds)):
            pairs[i].append([odds[i], odds[j]])

    print('Pairs will be:', end=' ')
    for i in pairs:
        print(i, end=', ')
    print('')

    return pairs


def sumEdges(matrix):
    sum = 0
    l = len(matrix)
    for i in range(l):
        for j in range(i, l):
            sum += matrix[i][j]
    return sum


def chinesePostman(matrix):
    odds = getOdd(matrix)
    if (len(odds) == 0):
        return sumEdges(matrix)
    pairs = createPairs(odds)
    l = (len(pairs) + 1) // 2

    pairingsSum = []

    def getPairs(pairs, done=[], final=[]):
        if (pairs[0][0][0] not in done):
            done.append(pairs[0][0][0])

            for i in pairs[0]:
                f = final[:]
                val = done[:]
                if (i[1] not in val):
                    f.append(i)
                else:
                    continue

                if (len(f) == l):
                    pairingsSum.append(f)
                    return
                else:
                    val.append(i[1])
                    getPairs(pairs[1:], val, f)
        else:
            getPairs(pairs[1:], done, final)

    getPairs(pairs)
    minSums = []

    for i in pairingsSum:
        s = 0
        for j in range(len(i)):
            s += dijktra(matrix, i[j][0], i[j][1])
        minSums.append(s)

    minimum = min(minSums)
    chinese_dis = minimum + sumEdges(matrix)

    return chinese_dis


if __name__ == '__main__':
    array = getFile()
    array = [[int(j) if '.' not in j else float(j) for j in i] for i in array]
    numberOfNodes = int(array[0][0])
    matrix = array[1:]

    table = PrettyTable([chr(i) for i in range(65, 65 + numberOfNodes)])
    for i in matrix:
        table.add_row(i)
    print(table)

    print('Postman minimal distance is:', chinesePostman(matrix))
