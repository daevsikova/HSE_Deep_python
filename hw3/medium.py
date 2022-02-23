import numpy as np
from numbers import Number


class MatrixMixin(np.lib.mixins.NDArrayOperatorsMixin):
    _HANDLED_TYPES = (np.ndarray, Number)
    
    def __init__(self, data):
        self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        for x in inputs:
            if not isinstance(x, self._HANDLED_TYPES + (MatrixMixin,)):
                return NotImplemented

        inputs = (x.data for x in inputs)
        result = getattr(ufunc, method)(*inputs, **kwargs)
        return type(self)(result)

    def __str__(self):
        return '|' + '\n|'.join(['\t'.join([str(el) for el in row]) + '|' for row in self.data])

    def write(self, save_path):
        with open(save_path, 'w+') as f:
            f.write(str(self))


if __name__ == '__main__':
    np.random.seed(0)
    
    m1 = MatrixMixin(np.random.randint(0, 10, (10, 10)))
    m2 = MatrixMixin(np.random.randint(0, 10, (10, 10)))

    (m1 + m2).write('artifacts/medium/matrix+.txt')
    (m1 * m2).write('artifacts/medium/matrix*.txt')
    (m1 @ m2).write('artifacts/medium/matrix@.txt')
