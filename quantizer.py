import numpy


class Quantizer:

    def max_lloyd(self, nums, d):
        r = []
        dl = len(d)
        l = len(nums)
        dic = {}
        for i in range(l):
            number = nums[i]
            for k in range(dl):
                if d[k] <= number < d[k + 1]:
                    if k in dic:
                        dic[k][0] += number
                        dic[k][1] += 1
                    else:
                        dic[k] = [number, 1]
        for i in range(dl - 1):
            r.append(dic[i][0] / (dic[i][1]))
        return r

    def d(self, r):
        l = len(r)
        d = [0]
        for i in range(1, l):
            d.append((r[i - 1] + r[i]) / 2)
        return d

    def iterate(self, a, di, it):
        maxmargin = di[-1]
        i = 1
        r1 = []
        while i <= it:
            print(f'Iteration:{i}')
            r1 = self.max_lloyd(a, di)
            print(f'r: {r1}')
            di = self.d(r1)
            di.append(maxmargin)
            print(f'd: {di}')
            i += 1
        return r1, di

    def deq(self, nums, d, r):
        new = []
        ld = len(d)
        l = len(nums)
        for i in range(l):
            ans = []
            for j in range(ld):
                if d[j] <= nums[i] < d[j + 1]:
                    ans.append(round(r[j], 5))
            new.append(ans)
        return numpy.array(new)

    def mse(self, a, dq):
        l = len(a)
        s = 0
        for i in range(l):
            s += pow((a[i] - dq[i]), 2)
        return s / l

    def uniqua(self, a, d):
        l = len(a)
        new = []
        q = []
        for i in range(l):
            for j in range(len(d)):
                if d[j] <= a[i] < d[j + 1]:
                    new.append((d[j] + d[j + 1]) / 2)
                    q.append(j)
        return new, q

    def semiqua(self, a, d):
        l = len(a)
        new = []
        q = []
        dic = {}
        for i in range(l):
            for j in range(len(d)):
                if d[j] <= a[i] <= d[j + 1]:
                    if j in dic:
                        dic[j] = (dic[j][0] + a[i], dic[j][1] + 1)
                    else:
                        dic[j] = (a[i], 1)
        for i in dic:
            dic[i] = int(dic[i][0] / dic[i][1])
        for i in range(l):
            ans = []
            ansq = []
            for j in range(len(d)):
                if d[j] <= a[i] < d[j + 1]:
                    ans.append(dic[j])
                    ansq.append(j)
                    break
            new.append(ans)
            q.append(ansq)
        return numpy.array(new)

    def getdecisions(self, d, a):
        m = (numpy.min(a), numpy.max(a) + 0.001)
        sec = (m[1] - m[0]) / d
        return [m[0] + i * sec for i in range(d + 1)]

    def clustering_based(self, nums, k):
        l = len(nums)
        sec = l // k
        r = []
        c = []
        for i in range(k):
            r.append(nums[sec * i])
        print(r, 'initiate!')
        for i in range(10):
            c = self.Cluster_assignment(nums, r)
        return r, c

    def Cluster_assignment(self, nums, r):
        l = len(nums)
        c = []
        for i in range(l):
            number = nums[i]
            cpr = []
            for j, k in enumerate(r):
                dis = abs(number - k)
                cpr.append((j, dis))
            cpr.sort(key=lambda x: x[1])
            c.append(cpr[0][0])
        dic = {}
        for i in range(l):
            if c[i] in dic:
                dic[c[i]][0] += nums[i]
                dic[c[i]][1] += 1
            else:
                dic[c[i]] = [nums[i], 1]
        for i in dic:
            r[i] = dic[i][0] / dic[i][1]
        return c

    def cde(self, r, c):
        dx = []
        for i in c:
            dx.append(round(r[i], 5))
        return dx


if __name__ == '__main__':
    q = Quantizer()
    a = [0, 0.8, 0.8, 0.7, 0.8, 0.8, 0.7, 1, 1, 1, 1, 1.2, 1.2, 1.2, 1.23, 1.74, 1.75, 1.73, 1.83, 1.84, 2.2, 2.2, 2.4, 2.36, 2.38, 2.9, 2.8]
    d1 = [0, 3/4, 3/2, 9/4]
    print(len(a))
    b = [0, 0.01, 2.8, 3.4, 1.99, 3.6, 5, 3.2, 4.5, 7.1, 7.9]
    d2 = [0, 2, 4, 6]
    d = [0, 0.7345833333333333, 1.450535714285714, 2.2332857142857145, 3]
    r = [0.4666666666666666, 1.0025, 1.8985714285714284, 2.5680000000000005]
    du = [0, 3/4, 3/2, 9/4, 3]
    #q.iterate(a, d1)
    #dq, uq = q.uniqua(a, du)
    nr, nc = q.clustering_based(a, 4)
    ans = q.cde(nr, nc)
    print(nr)
    print(nc)
    print(ans)
    print('MSE: ', q.mse(a, ans))
    '''
    print(dq)
    print(qu)
    
    dq, qu = q.semiqua(a, du)
    print(dq)
    print(qu)
    print('MSE:', q.mse(a, dq))'''



