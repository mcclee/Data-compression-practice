import numpy
import matplotlib.pyplot as plt
from scipy import fftpack, linalg


class Transforms:
    def __init__(self, fftfunction, length):
        self.matrix = []
        for i in range(length):
            self.matrix.append(fftfunction(i))
        self.matrix = numpy.array(self.matrix)

    def fft(self, matrix1):
        return numpy.fft.fft(matrix1)

    def absolute(self, matrix1):
        ans = []
        for i in matrix1:
            ans.append(numpy.abs(i))
        return numpy.array(ans)

    def sorting(self, matrix1):
        return sorted(enumerate(matrix1), key=lambda x: x[1])

    def inversefft(self, matrix):
        return numpy.fft.ifft(matrix)

    def dct(self, matrix):
        return fftpack.dct(matrix, norm='ortho')

    def idct(self, matrix):
        return fftpack.idct(matrix, norm='ortho')

    def hadamard(self, number):
        return linalg.hadamard(number)

    def walsh(self, number):
        if number != 2:
            base = linalg.hadamard(number/2)
            ansh = numpy.concatenate((base, base), axis=1)
            ansb = numpy.concatenate((base, -base), axis=1)
            hmatrix = numpy.concatenate((ansh, ansb))
            changeset = []
            l = len(hmatrix)
            for i in hmatrix:
                signchanges = 0
                for j in reversed(range(l)):
                    if j - 1 >= 0 and i[j - 1] != i[j]:
                        signchanges += 1
                changeset.append(signchanges)
            ans2 = []
            for i in sorted(enumerate(changeset), key=lambda x: x[1]):
                ans2.append(hmatrix[i[0]])
            return ans2

    def preinverse(self, matrix, k):
        magnitude = fft.absolute(matrix)
        sortedresult = fft.sorting(magnitude)
        for i in range(k):
            matrix[sortedresult[i][0]] = 0

    def meansquareerror(self, mat1, mat2):
        l = len(mat1)
        squareerror = pow(mat1 - mat2, 2)
        mean = numpy.sum(squareerror)/l
        return mean


if __name__ == '__main__':
    function1 = lambda x: pow(x, 3)/4
    function2 = lambda x: numpy.math.cos((3*x + 1)/16*numpy.pi)
    fft = Transforms(function2, 16)
    mt = fft.matrix
    '''walsh = fft.walsh(16)
    walt = 1/4 * numpy.matmul(walsh, fft.matrix)
    fft.preinverse(walt)
    rewal = 1/4 * numpy.matmul(walt, walsh)

    ftm = fft.fft(mt)
    fft.preinverse(ftm)
    iftm = fft.inversefft(ftm)'''
    errors = []
    for i in range(1, 16):
        dctm = fft.dct(mt)
        fft.preinverse(dctm, i)
        idctm = fft.idct(dctm)
        error = fft.meansquareerror(idctm, mt)
        errors.append(error)
    errors = numpy.array(errors)
    rag = [i for i in range(1, 16)]
    plt.plot(rag, errors, 'bo-')
    plt.title('MSE of DCT')
    plt.xlabel('MSE')
    plt.ylabel('Last n')
    plt.legend(('MSE', 'walsh trans', 'fft', 'dct'))
    plt.show()
    print('Last n        ', 'MSE')
    for i in range(15):
        print(' ', i, '  ', errors[i])








