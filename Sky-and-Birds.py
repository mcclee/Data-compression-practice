import math
from PIL import Image
import numpy as np
from quantizer import Quantizer
from scipy import fftpack


class PI:
    def __init__(self, path):
        self.image = Image.open(path)
        self.pixels = np.array(self.image)
        self.newimage = []
        for i in self.pixels:
            pixel = []
            for j in i:
                pixel.append(float(j))
            self.newimage.append(pixel)
        self.newimage = np.array(self.newimage)

    def shownp(self, im):
        im = Image.fromarray(np.uint8(im))
        im.show(im)

    def save(self, path, im):
        im = Image.fromarray(np.uint8(im))
        im.save(path)

    def snr(self, org, compressed):
        p1 = np.power(org, 2)
        s1 = np.sum(p1)
        mi = org - compressed
        p2 = np.power(mi, 2)
        s2 = np.sum(p2)
        snr = 20 * math.log(pow(s1, 0.5)/(pow(s2, 0.5)), 10)
        return snr

    def entropy(self, array):
        dic = {}
        s = 0
        for i in array:
            for j in i:
                if j not in dic:
                    dic[j] = 1
                else:
                    dic[j] += 1
                s += 1
        entropy = 0
        for i in dic:
            p = dic[i] / s
            entropy -= p * math.log(p, 2)
        return entropy

    def block_oriented_DCT(self, array, d):
        ll = len(array)
        l2 = len(array[0])
        b = int(ll / d)
        b2 = int(l2 / d)
        bline = np.split(array, b)
        topset = []
        subset = []
        submap = []
        for l in range(len(bline)):
            blocks = np.split(bline[l], b2, axis=1)
            for block in blocks:
                dct = fftpack.dct(fftpack.dct(block.T, norm='ortho').T, norm='ortho')
                topset.append(dct[0][0])
                for i in reversed(range(1, 1)):
                    for j in range(i + 1):
                        subset.append(dct[j][i - j])
                        submap.append((j, i - j))
        dt, ds = self.goingon(subset, topset)
        topset = self.uniqua(topset, dt)
        subset = self.uniqua(subset, ds)
        print('quantized')
        return self.reshape(subset, topset, submap, b, b2, d)

    def goingon(self, subset, topset):
        dt = self.getdecisions(16, topset)
        ds = self.getdecisions(8, subset)
        return dt, ds

    def getdecisions(self, d, a):
        m = (np.min(a), np.max(a) + 0.001)
        sec = (m[1] - m[0]) / d
        return [m[0] + i * sec for i in range(d + 1)]

    def reshape(self, subset, topset, submap, l, ll, d):
        subset = subset[::-1]
        topset = topset[::-1]
        submap = submap[::-1]
        reshaped = None
        for i in range(l):
            linematrix = None
            for j in range(ll):
                ans = np.zeros((d, d))
                ans[0][0] = topset.pop()
                for time in range(0):
                    value = subset.pop()
                    index = submap.pop()
                    ans[index[0]][index[1]] = value
                ans = fftpack.idct(fftpack.idct(ans.T, norm='ortho').T, norm='ortho')
                if linematrix is not None:
                    linematrix = np.concatenate((linematrix, ans), axis=1)
                else:
                    linematrix = np.array(ans)
            if reshaped is not None:
                reshaped = np.concatenate((reshaped, linematrix), axis=0)
            else:
                reshaped = np.array(linematrix)
        return reshaped



    def uniqua(self, a, d):
        l = len(a)
        new = []
        for i in range(l):
            for j in range(len(d)):
                if d[j] <= a[i] < d[j + 1]:
                    new.append((d[j] + d[j + 1]) / 2)
        return new



if __name__ == '__main__':
    path = '/Users/linan/Downloads/newbird.png'
    p = PI(path)
    q = Quantizer()
    pic = p.block_oriented_DCT(p.newimage, 8)
    p.save('/Users/linan/Downloads/G3.png', pic)
    p.shownp(pic)
    print('SNR: ', p.snr(p.newimage, pic))
    #topset = np.load('/Users/linan/PycharmProjects/compression/topset.npy')
    #subset = np.load('/Users/linan/PycharmProjects/compression/subset.npy')
    #dt, ds = p.goingon(subset,topset)


    #p.show(p.pixels)
    #d = q.getdecisions(6, p.pixels)

    """
    array = p.newimage.flatten()
    print(type(array))
    r, c = q.clustering_based(array, 6)
    print(r)
    print(len(c))"""
    #newimage2 = np.reshape(q.cde(r, c), (448, 640))
    #print('E:', p.entropy(newimage2))
    #print('SNR: ', p.snr(p.newimage, newimage2))
    #p.save('/Users/linan/Downloads/cluster_based.png', newimage)
    #r1, d = q.iterate(p.newimage, d, 10)
    #print(r1)
    #for i in range(len(d)-1):
    #    print(d[i], d[i+1], (d[i+1] + d[i]) / 2)

    #image = q.deq(p.newimage, d, r1)
    #print('E:', p.entropy(image))
    #print('SNR:', p.snr(newimage2, image))
    #p.save('/Users/linan/Downloads/Max_Lloyd_quantizer.png', image)








