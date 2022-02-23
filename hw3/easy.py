import numpy as np


class Matrix:
    def __init__(self, data):
        self.shape = (len(data), len(data[0]))
        self.data = data

        for row in data:
            assert len(row) == self.shape[1], 'Matrix must be rectangular'

    def __add__(self, x):
        if x.shape != self.shape:
            raise ValueError(f'{x.shape} shape is not compatible for {self.shape} matrix shape')
        result = [[self[i, j] + x[i, j] for j in range(self.shape[1])] for i in range(self.shape[0])]
        return Matrix(result)

    def __mul__(self, x):
        if x.shape != self.shape:
            raise ValueError(f'{x.shape} shape is not compatible for {self.shape} matrix shape')
        result = [[self[i, j] * x[i, j] for j in range(self.shape[1])] for i in range(self.shape[0])]
        return Matrix(result)

    def __matmul__(self, x):
        if self.shape[1] != x.shape[0]:
            raise ValueError(f'{x.shape} shape is not compatible for {self.shape} matrix shape')
        result = [[sum(self[i, j] * x[j, k] for j in range(self.shape[1]))
          for k in range(x.shape[1])] for i in range(self.shape[0])]
        return Matrix(result)

    def __getitem__(self, idx):
        assert isinstance(idx, (int, tuple)), 'Allowed types for indices: int, tuple'
        
        if len(idx) > 2:
            raise ValueError('Only 1 or 2 dimensional indexes are allowed')

        if isinstance(idx, int):
            return self.data[idx]
        else:
            assert isinstance(idx[0], int)
            assert isinstance(idx[1], int)
            return self.data[idx[0]][idx[1]]


if __name__ == "__main__":
    np.random.seed(0)
    
    m1 = Matrix(np.random.randint(0, 10, (10, 10)).tolist())
    m2 = Matrix(np.random.randint(0, 10, (10, 10)).tolist())

    result = m1 + m2
    with open('artifacts/easy/matrix+.txt', 'w+') as f:
        s = '\n'.join([str(row) for row in result.data])
        f.write(s)

    result = m1 * m2
    with open('artifacts/easy/matrix*.txt', 'w+') as f:
        s = '\n'.join([str(row) for row in result.data])
        f.write(s)

    result = m1 @ m2
    with open('artifacts/easy/matrix@.txt', 'w+') as f:
        s = '\n'.join([str(row) for row in result.data])
        f.write(s)
