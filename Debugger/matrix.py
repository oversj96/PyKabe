class Matrix:
    def __init__(self, row_length, number, rows, problem_rows, from_file):
        self.problem_type = "None"
        self.from_file = from_file
        self.row_length = row_length
        self.number = number
        self.rows = rows
        self.problem_rows = problem_rows
        self.seed = self.matrix_seed()
        self.first_water_point = None
        self.water_reachable = 0
        self.travel_map = [[True for j in range(0, row_length)] for i in range(0, row_length)]
        self.water_count = 0
        self.pos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.count_water()


    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.seed == other.seed


    def print_matrix(self):
        output = ""
        output += f"\nProblem Type: {self.problem_type}\n"
        output += f"{self.number} in {self.from_file}\n"       
        for i in range(0, len(self.rows)):
            for bit in self.rows[i]:
                if int(bit) == 1:
                    output += "1 "
                else:
                    output += "0 "
            if i not in self.problem_rows:
                output += f"  {to_decimal(self.rows[i])}\n"
            else:
                output += f"  {to_decimal(self.rows[i])}*\n"       
        output += "\n"
        return output

    def can_move(self, pos, direction):
        return (pos + direction <= len(self.rows) - 1 and pos + direction >= 0)


    def test_puzzle(self, pos_x, pos_y, call):
        self.travel_map[pos_x][pos_y] = False
        self.water_reachable += 1
        for point in self.pos:
            x, y = point
            if self.can_move(pos_x, x) and self.can_move(pos_y, y) and self.travel_map[pos_x + x][pos_y + y]:
                self.test_puzzle(pos_x + x, pos_y + y, call + 1)
        if call == 1:
            self.problem_type = "Illegal Puzzle" if self.water_reachable != self.water_count else "Missing Puzzle"


    def count_water(self):
        for i in range(0, len(self.rows)):
            for j in range(0, len(self.rows[i])):
                if int(self.rows[i][j]) == 0:
                    if self.first_water_point == None:
                        self.first_water_point = (i, j)
                    self.water_count += 1
                else:
                    self.travel_map[i][j] = False



    def matrix_seed(self):
        '''flattens the matrix rows into a binary vector and returns that in decimal.'''
        return int(''.join([str(j) for row in self.rows for j in row]), 2)


def to_decimal(row):
    return int(''.join(row), 2)