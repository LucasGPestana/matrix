from typing import List

class Matrix:

    def __init__(self, value: List[List[float]]) -> None:

        self.value = value

    def __str__(self) -> str:

        display_matrix: str = ""

        flat_matrix = [elem for line in self.value for elem in line]

        # Adquire a quantidade de digitos do número com maior quantidade de digitos
        num_of_digits = len(sorted(list(map(str, flat_matrix)), key=lambda x: len(x), reverse=True)[0])
        
        for i in range(len(self.value)):

            for j in range(len(self.value[i])):

                if isinstance(self.value[i][j], int):

                    display_matrix += f"{self.value[i][j]:0{num_of_digits}d}\t"

                else:

                    display_matrix += f"{self.value[i][j]:0.{3 if '-' in str(self.value[i][j]) else 4}f}\t"

            display_matrix += "\n"

        return display_matrix

    # Representação da matriz na forma de uma lista de listas
    @property
    def values(self) -> List[List[float]]:

        return self.value

    # Quantidade de linhas
    @property
    def m(self) -> int:

        return len(self.value)

    # Quantidade de colunas
    @property
    def n(self) -> int:

        return len(self.value[0])

    @property
    def is_quadratic(self) -> bool:

        return self.m == self.n

    # Traço da matriz
    @property
    def trace(self) -> float:

        if not self.is_quadratic:

            print("Não é possível calcular o traço de uma matriz com quantidade de linhas e colunas diferente!")
            return float("NaN")

        return sum([self.value[i][i] for i in range(len(self.value))])
        

    # Determinante da matriz
    @property
    def det(self) -> float:

        if not self.is_quadratic:

            print("Não é possível calcular a determinante de uma matriz com quantidade de linhas e colunas diferente!")
            return float("NaN")

        return Matrix.calculateDeterminant(self.value)

    # Matriz de cofatores
    @property
    def cofactor_matrix(self) -> List[List[float]]:

        cofactor_matrix: List[List[float]] = list()

        for i in range(len(self.values)):
            
            line: List[float] = list()
            list_matrix = [list(line) for line in self.values]

            list_matrix.pop(i)

            # k representa o indice utilizado para iterar as colunas da matriz original
            for k in range(len(self.values[0])):

                # Uma cópia da cópia da matriz original sem a linha i, de modo que as alterações dessa matriz não reflitam na cópia da matriz (list_matrix)
                list_matrix_copy = [list(line) for line in list_matrix]

                for j in range(len(list_matrix)):

                    list_matrix_copy[j].pop(k)

                line.append(Matrix.getCofactorCoef(i, k) * Matrix.calculateDeterminant(list_matrix_copy))

            cofactor_matrix.append(line)

        return cofactor_matrix

    # Transposta da matriz
    @property
    def transpose(self) -> List[List[float]]:

        return Matrix.getTransposeMatrix(self.values)

    # Matriz adjunta
    @property
    def adjoint(self) -> List[List[float]]:

        return Matrix.getTransposeMatrix(self.cofactor_matrix)

    # Inverso da matriz
    @property
    def inverse(self):

        inverse_matrix = [[0 for _ in range(len(self.values[0]))] for _ in range(len(self.values))]

        for i in range(len(self.adjoint)):

            for j in range(len(self.adjoint[0])):

                inverse_matrix[i][j] = self.adjoint[i][j] / self.det

        return inverse_matrix
    
    # Pega a matriz transposta da representação da matriz passada como argumento
    @staticmethod
    def getTransposeMatrix(matrix: List[List[float]]) -> List[List[float]]:

        transpose_matrix = [[0 for _ in range(len(matrix))] for _ in range(len(matrix[0]))]

        for i in range(len(matrix)):

            for j in range(len(matrix[0])):

                transpose_matrix[j][i] = matrix[i][j]

        return transpose_matrix
    

    # Calcula o cofator do elemento dos indices passados como argumento (contagem a partir de 0)
    # row e col são os indices
    @staticmethod
    def getCofactorCoef(row: int, col: int) -> float:

        return ((-1) ** ((row + 1) + (col + 1)))

    # Calcula o determinante da matriz de fato, de forma recursiva
    @staticmethod
    def calculateDeterminant(matrix: List[List[float]]) -> float:

        det: float = 0

        if len(matrix) == 1 and len(matrix[0]) == 1:

            return matrix[0][0]

        for i in range(len(matrix)):

            # Criar uma cópia das listas internas e externas para não fazer referência por endereço de memória
            list_matrix = list([list(line) for line in matrix])

            # Remove a linha pelo método de Laplace
            list_matrix.pop(i)

            # Remove os elementos da coluna (ou seja, de indice 0) pelo método de Laplace na matriz sem a linha i
            # j representa a linha de iteração na copia da matriz, já sem a linha 1
            for j in range(len(list_matrix)):

                list_matrix[j].pop(0)

            # Nesse código, os elementos escolhidos como cofatores são os da coluna 0 (1 se o contador começasse por 1)

            # det(matrix mxn) = cofactor(i, 0) * matrix[i][0] * det(matrix m-1xn-1)
            det += Matrix.getCofactorCoef(i, 0) * matrix[i][0] * Matrix.calculateDeterminant(list_matrix)
            
        return det

    def product(self, matrix2: List[List[float]]) -> List[List[float]]:

        if len(self.values[0]) != len(matrix2):

            print("A quantidade de colunas da matriz 1 não corresponde a quantidade de linhas da matriz 2!")
            return

        # i, j são os índices da matriz 1 (correspondente a instância de Matrix)
        # j, k são os índices da matriz 2

        i, k = 0, 0
        
        resulted_matrix = [[0 for _ in range(len(matrix2[0]))] for _ in range(len(self.values))]

        while i != len(resulted_matrix) or k != len(resulted_matrix[0]):

            line_sum: float = 0

            try:

                # Serve para acessar um valor na matriz resultante a partir dos indices i, k
                # Caso um destes seja invalido, um IndexError será disparado
                resulted_matrix[i][k]

            except IndexError:

                # Se um dos indices não for invalido, quer dizer que o outro é

                if i == len(resulted_matrix): i -= 1
                    
                else: k -= 1

            finally:

                for j in range(len(self.values[0])):

                    line_sum += self.values[i][j] * matrix2[j][k]

                resulted_matrix[i][k] = line_sum

                if i < len(self.values): i += 1
                if k < len(matrix2[0]): k += 1

        return resulted_matrix
