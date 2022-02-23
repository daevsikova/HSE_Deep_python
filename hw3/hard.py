from easy import Matrix


class HashMixin:
    def __hash__(self):
        # остаток от деления (суммы всех элементов + 1) на 7
        return (sum(sum(row) for row in self.data) + 1) % 7


class HashedMatrix(HashMixin, Matrix):
    hash = HashMixin.__hash__

    def __init__(self, data) -> None:
        super().__init__(data)
        self.__cache = {}

    def __matmul__(self, x):
        
        key = (self.hash(), x.hash())
        if key not in self.__cache:
            self.__cache[key] = HashedMatrix(super().__matmul__(x).data)
        return self.__cache[key]


if __name__ == "__main__":
    A = HashedMatrix([[1, 1], [2, 2]])
    B = HashedMatrix([[5, 6], [7, 8]])
    C = HashedMatrix([[2, 2], [1, 1]])
    D = B
    
    AB = A @ B
    CD = C @ D
    
    assert (A.hash() == C.hash()) and (A != C) and (B == D) and (AB != CD)
    
    with open('artifacts/hard/A.txt', 'w+') as f:
        s = '\n'.join([str(row) for row in A.data])
        f.write(s)

    with open('artifacts/hard/B.txt', 'w+') as f:
        s = '\n'.join([str(row) for row in B.data])
        f.write(s)

    with open('artifacts/hard/C.txt', 'w+') as f:
        s = '\n'.join([str(row) for row in C.data])
        f.write(s)

    with open('artifacts/hard/D.txt', 'w+') as f:
        s = '\n'.join([str(row) for row in D.data])
        f.write(s)

    with open('artifacts/hard/AB.txt', 'w+') as f:
        s = '\n'.join([str(row) for row in AB.data])
        f.write(s)

    with open('artifacts/hard/CD.txt', 'w+') as f:
        C = Matrix([[2, 2], [1, 1]])
        D = Matrix([[5, 6], [7, 8]])
        s = '\n'.join([str(row) for row in (C @ D).data])
        f.write(s)

    with open('artifacts/hard/hash.txt', 'w+') as f:
        s = str(AB.hash()) + '\n' + str(CD.hash())
        f.write(s)
