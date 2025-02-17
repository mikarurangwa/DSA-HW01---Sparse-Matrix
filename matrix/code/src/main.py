import os

class SparseMatrix:
    def __init__(self, file_path=None, num_rows=None, num_cols=None):
        """Initializes the sparse matrix."""
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.data = {}
        
        if file_path:
            self._load_from_file(file_path)
    
    def _load_from_file(self, file_path):
        """Loads a sparse matrix from a file."""
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                
                if len(lines) < 2:
                    raise ValueError("Input file has wrong format")
                
                self.num_rows = int(lines[0].strip().split('=')[1])
                self.num_cols = int(lines[1].strip().split('=')[1])
                
                for line in lines[2:]:
                    line = line.strip()
                    if not line:
                        continue
                    if not (line.startswith('(') and line.endswith(')')):
                        raise ValueError("Input file has wrong format")
                    
                    parts = line[1:-1].split(',')
                    if len(parts) != 3:
                        raise ValueError("Input file has wrong format")
                    
                    row, col, value = map(int, parts)
                    self.set_element(row, col, value)
        except Exception as e:
            raise ValueError(f"Error reading file: {str(e)}")
    
    def get_element(self, row, col):
        """Retrieves an element from the sparse matrix."""
        return self.data.get((row, col), 0)
    
    def set_element(self, row, col, value):
        """Sets an element in the sparse matrix."""
        if row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
            raise IndexError("Index out of bounds")
        
        if value == 0:
            self.data.pop((row, col), None)
        else:
            self.data[(row, col)] = value
    
    def add(self, other):
        """Adds two sparse matrices."""
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrices dimensions do not match")
        
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)
        keys = set(self.data.keys()).union(other.data.keys())
        
        for key in keys:
            summed_value = self.get_element(*key) + other.get_element(*key)
            result.set_element(key[0], key[1], summed_value)
        
        return result
    
    def subtract(self, other):
        """Subtracts another sparse matrix from this matrix."""
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrices dimensions do not match")
        
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)
        keys = set(self.data.keys()).union(other.data.keys())
        
        for key in keys:
            diff_value = self.get_element(*key) - other.get_element(*key)
            result.set_element(key[0], key[1], diff_value)
        
        return result
    
    def multiply(self, other):
        """Multiplies two sparse matrices."""
        if self.num_cols != other.num_rows:
            raise ValueError("Number of columns in first matrix must equal number of rows in second matrix")
        
        result = SparseMatrix(num_rows=self.num_rows, num_cols=other.num_cols)
        
        for (i, j), value in self.data.items():
            for k in range(other.num_cols):
                if (j, k) in other.data:
                    mult_value = result.get_element(i, k) + value * other.get_element(j, k)
                    result.set_element(i, k, mult_value)
        
        return result
    
    def __str__(self):
        """Returns a human-readable string representation of the sparse matrix."""
        elements = [f"({r}, {c}, {v})" for (r, c), v in self.data.items()]
        return f"SparseMatrix {self.num_rows}x{self.num_cols}: " + " ".join(elements)
    

def main():
    # Set your directories here:
    BASE_DIR = "/workspaces/DSA-HW01---Sparse-Matrix/matrix/code/src"
    INPUT_DIR = "/workspaces/DSA-HW01---Sparse-Matrix/matrix/sample_inputs"
    OUTPUT_DIR = "/workspaces/DSA-HW01---Sparse-Matrix/matrix/sample_results"

    print("Base directory:", BASE_DIR)
    print("Input directory:", INPUT_DIR)
    print("Output directory:", OUTPUT_DIR)
    
    # Build the file paths from the input directory.
    matrix1_file = os.path.join(INPUT_DIR, "matrix1.txt")
    matrix2_file = os.path.join(INPUT_DIR, "matrix2.txt")
    
    try:
        matrix1 = SparseMatrix(matrix1_file)
        matrix2 = SparseMatrix(matrix2_file)
        
        while True:
            print("\nChoose an operation:")
            print("1. Addition")
            print("2. Subtraction")
            print("3. Multiplication")
            print("4. Exit")
            choice = input("Enter choice (1/2/3/4): ")
            
            if choice == '1':
                result = matrix1.add(matrix2)
                print("\nResult of Addition:")
                print(result)
            elif choice == '2':
                result = matrix1.subtract(matrix2)
                print("\nResult of Subtraction:")
                print(result)
            elif choice == '3':
                result = matrix1.multiply(matrix2)
                print("\nResult of Multiplication:")
                print(result)
            elif choice == '4':
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice! Please select a valid option.")
    
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
