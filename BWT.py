import time


class BWT:
    def __init__(self):
        self.result = []
        self.pool = []
        self.dic = {' ': ' @'}

    def rotate(self, string):
        return string[-1] + string[:-1]

    def coding(self, string):
        self.result = []
        res = ''
        string = '$' + string
        l = len(string)
        while l:
            self.result.append(string)
            string = self.rotate(string)
            l -= 1
        self.result.sort()
        for i in self.result:
            res = res + i[-1]
        return res

    def decode(self, string):
        generate = []
        l = len(string)
        for roll in range(l):
            for i in range(l):
                if roll == 0:
                    generate.append(string[i])
                else:
                    generate[i] = string[i] + generate[i]
            print('distribute letters:')
            print(generate)
            generate.sort()
            print('sort the arraylist:')
            print(generate)
        for i in generate:
            if i[0] == '$':
                print('The original code is:', i)
                return i
        return None

    def preproccess(self,string):
        index = string.find(' ')
        while index != -1:
            string = string[:index] + '@' + string[index + 1:]
            index = string.find(' ')
        return string


if __name__ == '__main__':
    w = BWT()
    c = 'ababcbbac'
    t1 = time.time()
    bwt = w.coding(c)
    q = w.decode(bwt)
    t2 = time.time()

