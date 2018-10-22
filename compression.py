import math


class HuffmanCode:

    def __init__(self, code):
        self.dic = {}
        self.code = {}
        self.l = len(code)
        for i in code:
            if i in self.code:
                self.code[i] += 1
            else:
                self.code[i] = 1
        for i in self.code:
            print(i, self.code[i], self.l)

    def entropy(self, probs):
        psum = 0
        for i in probs:
            psum += i * math.log(i, 2)
        return -psum

    def coding(self):
        rank = list(reversed(sorted([(self.code[i], i) for i in self.code], key=lambda x: x[0])))
        first = rank.pop()
        second = rank.pop()
        self.dic[first[1]] = '0'
        self.dic[second[1]] = '1'
        while rank:
            node = rank.pop()
            for i in self.dic:
                self.dic[i] = '0' + self.dic[i]
            self.dic[node[1]] = '1'
        print(self.dic)

    def bitrate(self):
        s = 0
        for i in self.dic:
            s += len(self.dic[i]) * self.code[i]
        print(s, self.l, s / self.l)


if __name__ == '__main__':
    code1 = 'aaaaaaadddbdeddaaaaeeddce'
    h = HuffmanCode(code1)
    h.coding()
    h.bitrate()
    entro = []
    for i in h.code:
        entro.append(h.code[i] / float(h.l))
    print(h.entropy(entro))
