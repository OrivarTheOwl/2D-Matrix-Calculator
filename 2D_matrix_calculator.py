class MatrixOperations:

    # Creates a matrix based on user input
    @staticmethod
    def create_matrix():
        # Obtains row and column dimensions from user input
        while True:
            try:
                row_count = int(input("\nRow count: "))
                column_count = int(input("Column count: "))
            except ValueError:
                print("Invalid Input")
                continue
            if row_count < 1 or column_count < 1:
                print("Matrix must have dimensions of at least 1x1")
                continue
            break
        print(f"Matrix Dimensions: {row_count}x{column_count}\n")

        MatrixClass.matrix = []
        current_row = 1
        current_column = 1
        current_list = []

        # Fills the matrix with values from user input
        while current_row <= row_count:
            while True:
                try:
                    current_list.append(float(input(f"Entry for Row {current_row}, Column {current_column}: ")))
                except ValueError:
                    print("Invalid Input")
                    continue
                break
            if current_column == column_count:
                current_row += 1
                current_column = 1
                MatrixClass.matrix.append(current_list)
                current_list = []
            else:
                current_column += 1
        print("Matrix created successfully!")

    # Displays the current matrix
    @staticmethod
    def display_matrix():
        for row in MatrixClass.matrix:
            print(row)

    # Transposes the current matrix
    @staticmethod
    def transpose_matrix(matrix):
        new_matrix = []
        current_row = []
        column_index = 0

        # Determines the longer of the row and column width
        if len(matrix) > len(matrix[0]):
            num_of_iterations = len(matrix)
        else:
            num_of_iterations = len(matrix[0])

        # Inefficient way to iterate through each row and
        # take the element of the current index to add to
        # the new transposed matrix row
        while column_index < num_of_iterations:
            for row in matrix:
                index = 0
                for entry in row:
                    if row.index(entry, index) == column_index:
                        current_row.append(entry)
                    index += 1
            if len(current_row) > 0:
                new_matrix.append(current_row)
                column_index += 1
                current_row = []
            else:
                break
        return new_matrix

    # Inverses the current matrix
    @staticmethod
    def inverse_matrix():
        # Must be square matrix to be inverted
        if len(MatrixClass.matrix) != len(MatrixClass.matrix[0]):
            print("Matrix is not invertible")
            return
        # Checks if the matrix is 1x1
        if len(MatrixClass.matrix) == 1:
            if MatrixClass.matrix[0] == 0:
                print("Matrix is not invertible")
            else:
                print(f"[{1 / MatrixClass.matrix[0][0]}]")
            return
        
        # Obtains the flattened version of the original list
        flattened_matrix = MatrixOperations.flatten_matrix(MatrixClass.matrix)
        # Calculates the identity matrix to check validity at the end
        identity_matrix = MatrixOperations.create_identity_matrix(len(MatrixClass.matrix))


        # Calculates the matrix of minors for the given matrix
        flattened_matrix_of_minors = MatrixOperations.calculate_matrix_of_minors(MatrixClass.matrix)
        # Obtains the unflatted matrix of minors
        unflattened_matrix_of_minors = MatrixOperations.unflatten_matrix(flattened_matrix_of_minors)

        # Obtains the cofactor matrix for the matrix of minors
        flattened_cofactor_matrix = MatrixOperations.calculate_cofactor_matrix(unflattened_matrix_of_minors)
        # Obtains the unflattened cofactor matrix
        unflattened_cofactor_matrix = MatrixOperations.unflatten_matrix(flattened_cofactor_matrix)

        # Obtains the adjoint matrix
        unflattened_adjoint_matrix = MatrixOperations.transpose_matrix(unflattened_cofactor_matrix)
        # Obtains the flattened adjoint matrix
        flattened_adjoint_matrix = MatrixOperations.flatten_matrix(unflattened_adjoint_matrix)

        # Calculates the determinant
        determinant = MatrixOperations.calculate_determinant(flattened_matrix)
        try:
            determinant_fraction = 1 / determinant
        except ZeroDivisionError:
            determinant_fraction = False
        if determinant_fraction == False:
            print("Matrix is not invertible")
            return
        
        # Calculates the inverse flattened matrix with the determinant and adjoint
        multiplied_matrix = MatrixOperations.multiply_by_constant(determinant_fraction, flattened_adjoint_matrix)
        # Unflattens for the proper inverse matrix
        inversed_matrix = MatrixOperations.unflatten_matrix(multiplied_matrix)

        # Multiplies the starter matrix by the inverse to obtain the final flattened matrix
        flattened_final_matrix = MatrixOperations.multiply_2_matrices(MatrixClass.matrix, inversed_matrix)
        if flattened_final_matrix == False:
            print("Matrix is not invertible")
            return
        # Unflattens the final flattened matrix
        final_matrix = MatrixOperations.unflatten_matrix(flattened_final_matrix)
        if final_matrix == identity_matrix:
            for row in inversed_matrix:
                print(row)
        else:
            print("Matrix is not invertible")

    # Creates an identity matrix of the given dimensions
    @staticmethod
    def create_identity_matrix(dimensions: int):
        identity_matrix = []
        current_row = 1
        current_column = 1
        current_list = []

        # Adds a 1 to the column index of the number of the row
        # Otherwise, adds a 0 to the column index
        while current_row <= dimensions:
            if current_column == current_row:
                current_list.append(1)
            else:
                current_list.append(0)

            if current_column == dimensions:
                current_row += 1
                current_column = 1
                identity_matrix.append(current_list)
                current_list = []
            else:
                current_column += 1
        return identity_matrix

    # Flattens a matrix list
    @staticmethod
    def flatten_matrix(matrix: list):
        flattened_list = []
        for row in matrix:
            for entry in row:
                flattened_list.append(entry)
        return flattened_list

    # Unflattens a matrix list
    @staticmethod
    def unflatten_matrix(matrix: list):
        unflattened_list = []
        dimensions = int(len(matrix) ** 0.5)
        current_row = []
        for entry in matrix:
            if len(current_row) != dimensions:
                current_row.append(entry)
            if len(current_row) == dimensions:
                unflattened_list.append(current_row)
                current_row = []
        return unflattened_list

    # Calculates a matrix of minors
    @staticmethod
    def calculate_matrix_of_minors(matrix: list):
        matrix_of_minors = []
        flattened_matrix = MatrixOperations.flatten_matrix(matrix)
        number_locations = MatrixOperations.calculate_index_dictionary(matrix)

        # Creates the matrix of minors for the given matrix
        current_list = []
        for row in matrix:
            target_row = matrix.index(row)
            target_column = 0
            for target_number in row:
                index = 0
                for number in flattened_matrix:
                    if number_locations[index][0] == target_row or number_locations[index][1] == target_column:
                        pass
                    else:
                        current_list.append(number)
                    index += 1
                target_column += 1
                # Calculates the and adds the final determinant to the matrix of minors
                if len(matrix) == 2:
                    matrix_of_minors.append(current_list[0])
                else:
                    matrix_of_minors.append(MatrixOperations.calculate_determinant(current_list))
                current_list = []

        return matrix_of_minors
        
    # Creates a dictionary with row and column numbers for each index
    @staticmethod
    def calculate_index_dictionary(matrix):
        number_locations = {}
        row_number = 0
        column_number = 0
        dimensions = len(matrix)
        for number in range(len(matrix) * len(matrix[0])):
            number_locations[number] = [row_number, column_number]
            if column_number == dimensions - 1:
                row_number += 1
                column_number = 0
            else:
                column_number += 1
        return number_locations

    # Calculates the determinant of a flattened 2x2 matrix
    @staticmethod
    def calculate_determinant(matrix: list):
        if len(matrix) == 4:
            determinant = (matrix[0] * matrix[3]) - (matrix[1] * matrix[2])
            return determinant
        # Recursively calculates the determinant for matrix of larger than 2x2
        else:
            unflattened_matrix = MatrixOperations.unflatten_matrix(matrix)
            flattened_matrix = MatrixOperations.flatten_matrix(unflattened_matrix)
            number_locations = MatrixOperations.calculate_index_dictionary(unflattened_matrix)
            row_1 = MatrixOperations.calculate_cofactor_matrix([unflattened_matrix[0]])
            determinant = 0
            target_column = 0

            for entry in row_1:
                current_list = []
                index = 0
                for number in flattened_matrix:
                    if number_locations[index][0] == 0 or number_locations[index][1] == target_column:
                        pass
                    else:
                        current_list.append(number)
                    index += 1
                target_column += 1
                determinant += entry * MatrixOperations.calculate_determinant(current_list)

            return determinant

    # Obtains the cofactor matrix
    @staticmethod
    def calculate_cofactor_matrix(matrix):
        cofactor_matrix = []
        i = 0
        j = 0
        for row in matrix:
            if matrix.index(row, i) % 2 == 0:
                for number in row:
                    if j % 2 != 0:
                        number = -number
                    cofactor_matrix.append(number)
                    j += 1
            else:
                for number in row:
                    if j % 2 == 0:
                        number = -number
                    cofactor_matrix.append(number)
                    j += 1
            i += 1
            j = 0

        return cofactor_matrix

    # Multiplies a flattened matrix by a constant
    @staticmethod
    def multiply_by_constant(constant: float, matrix: list):
        multiplied_matrix = []
        for entry in matrix:
            multiplied_matrix.append(round(entry * constant, 2))
        return multiplied_matrix

    # Multiplies 2 matrices together
    @staticmethod
    def multiply_2_matrices(matrix1: list, matrix2: list):
        if len(matrix1[0]) != len(matrix2):
            print("Matices cannot be multiplied, therefore:")
            return False
        column_count = len(matrix2[0])
        
        # Iterates through each row of the 1st matrix and multiplies
        # appropriate values for each column before moving to the next row
        new_matrix = []
        for row in matrix1:
            column_index = 0
            while column_index < column_count:
                current_sum = 0
                row_index = 0
                while row_index < len(row):
                    current_sum += row[row_index] * matrix2[row_index][column_index]
                    row_index += 1
                column_index += 1
                new_matrix.append(round(current_sum))
        return new_matrix

    # Returns the total sum of each entry in the current matrix
    @staticmethod
    def sum_matrix():
        matrix_sum = 0
        for row in MatrixClass.matrix:
            for entry in row:
                matrix_sum += entry
        return matrix_sum



class MatrixClass:
    # Matrix variable
    matrix = [[1, 2],
              [3, 4]
              ]

    def __init__(self):
        self.run()

    # Shows the list of options
    @staticmethod
    def show_instructions():
        print("\n----- Options -----")
        print("1 - Create Matrix")
        print("2 - Display Matrix")
        print("3 - Transpose Matrix")
        print("4 - Inverse Matrix")
        print("5 - Sum Matrix")
        print("6 - Exit")

    # While loop to run the program
    def run(self):
        while True:
            self.show_instructions()
            user_input = input(("\nSelect an option: "))

            match user_input:
                case "1":
                    MatrixOperations.create_matrix()
                case "2":
                    MatrixOperations.display_matrix()
                case "3":
                    MatrixClass.matrix = MatrixOperations.transpose_matrix(MatrixClass.matrix).copy()
                    print("Matrix transposed successfully!")
                case "4":
                    MatrixOperations.inverse_matrix()
                case "5":
                    print(f"Matrix Sum: {MatrixOperations.sum_matrix()}")
                case "6":
                    break
                case _:
                    print("Invalid Input")



MatrixClass()
