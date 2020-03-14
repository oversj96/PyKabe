from pathlib import Path
from matrix import Matrix

def read_matrix(file, position, row_length):
    number = file[position].replace(" ", "").replace(".","").replace("\n", "")
    rows = []

    for i in range(position + 1, position + row_length + 1):
        row = file[i].lstrip(" ")[:2*row_length - 1].replace("\n", "").split(" ")
        if row[0] == "1" or row[0] == "0":
            rows.append(row)


    return number, rows


def compare_files(file1, file2, row_length):
    larger_file = file1 if len(file1) > len(file2) else file2
    smaller_file = file1 if larger_file is file2 else file2
    offset = 0
    with open("Debugger\\larger_file_differences.txt", 'w') as file1, open("Debugger\\smaller_file_differences.txt", 'w') as file2:
        
        if larger_file[0].find("Puzzle") != -1:
            larger_file = larger_file[4:]
        else:
            smaller_file = smaller_file[4:]

        max_puzzle = int(larger_file[len(larger_file) - row_length - 2].rstrip('.').rstrip("\n"))        
        puzzle = 0
        while puzzle <= max_puzzle:
            increment_one = puzzle * (row_length + 2)
            increment_two = (row_length + 2)*(puzzle + offset)
            number1, rows1 = read_matrix(larger_file, increment_one, row_length)
            mat1 = Matrix(row_length, number1, rows1, [], "Larger File")   
            puzzle += 1        
            if mat1 != None:
                if mat1.first_water_point != None:
                    mat1.test_puzzle(mat1.first_water_point[0], mat1.first_water_point[1], 1)
                    if mat1.problem_type == "Illegal Puzzle":
                        offset -= 1    
                    elif mat1.problem_type == "Missing Puzzle":
                        offset += 1              
                    file1.write(mat1.print_matrix())
                    
                    
                

                    

if __name__ == "__main__":
    my_output = Path.cwd() / "debug" / "debug_[7x7].txt"
    with open(my_output, 'r', newline=None) as file:
        file1 = file.readlines()
        # for line in lines:
        #     if line.find("Total Legal Patterns:"):
        #         count = int(line[21:].replace(" ", ""))

    other_output = Path.cwd() / "debug" / "pattern.txt"
    with open(other_output, 'r', newline=None) as file:
        file2 = file.readlines()

    compare_files(file1, file2, 5)