class Segment:


    def __init__(self, columns):
        self.left_most_column = columns[0]
        self.right_most_column = columns[-1]
        self.single_column = True if columns[0] is columns[-1] else False


    def connects(self, other):
        '''Check to see if any columns between two segments are the same'''
        other_cols = list(range(other.left_most_column, other.right_most_column + 1))
        for col in other_cols:
            if col >= self.left_most_column and col <= self.right_most_column:
                return True
        return False