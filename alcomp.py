import math
from fractions import Fraction


class ArithmeticCoding:
    def encode(self, string, dic, dic2):
        l = len(string)
        for i in range(1, l):
            probnow = dic[string[:i]]
            prob = dic2[string[i-1: i+1]]
            dic[string[:i+1]] = (Fraction(probnow[0] + (probnow[1] - probnow[0]) * prob[0]), Fraction(probnow[0] + (probnow[1] - probnow[0]) * prob[1]))
        i = string
        print(i, dic[i], (dic[i][0] + (dic[i][1]-dic[i][0])/2))
        return dic

    def bitrate(self, dic, string):
        print(float(dic[string][0]), float(dic[string][1]))
        return -math.log(dic[string][1] - dic[string][0], 2)

    def generatecode(self, groupes):
        str1 = ''
        for i in groupes:
            string = str(i[0])
            index = i[1]
            while index:
                lo = 1
                str2 = string
                while index >= lo * 2:
                    str2 = str2 + str2
                    lo *= 2
                index -= lo
            str1 = str1 + str2
        return str1


if __name__ == '__main__':
    dicPro = {'0': (0, 1/2), '1': (1/2, 1)}
    dicMKV = {'00': (0, 63/64), '11': (1/64, 1), '10': (0, 1/64), '01': (63/64, 1)}
    a = ArithmeticCoding()
    string2 = a.generatecode(((0, 13), (1, 11), (0, 10), (1, 15), (0, 14), (1, 9)))
    #print(len(string2))
    string1 = '00000111'
    newdic = a.encode(string1, dicPro, dicMKV)

    for i in newdic:
        print(i, (float(newdic[i][0]), float(newdic[i][1])))
    i = string1
    print(-math.log(float(newdic[i][1]) - float(newdic[i][0]), 2))
    #print(a.bitrate(newdic, string1))
    #print('\n')

