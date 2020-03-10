import row
import segment as s


class RowScheme:

    debug_count = 0

    def __init__(self, parent_row, segments, is_start, is_final_row, partition_scheme):
        self.parent_row = parent_row
        self.segments = segments
        self.is_start = is_start
        self.partition_scheme = partition_scheme  
        self.unique_segment_count = 0 if not self.segments else max(self.partition_scheme) + 1 
        self.depth_memoized = []
        self.memos = []
        self.successors = []
        self.single_partition_successors = []
        self.finalizers = []
        self.is_final_row = is_final_row
            

    def succeeds(self, other):
        # If partitionless scheme
        if self.is_final_row:
            if other.is_final_row:
                return True
            elif max(other.partition_scheme) == len(other.partition_scheme) - 1:
                return True

        # If single partition scheme
        elif len(set(self.partition_scheme)) == 1:
            if other.is_final_row:
                return True
            else:
                return self.connects_all_partitions(other)

        # If multipart scheme
        elif len(set(self.partition_scheme)) > 1:
            if other.is_final_row:
                return False
            else:
                return self.connects_all_partitions(other)

        # Any other case not handled is invalid or incorrectly handled, potentially.
        else:
            return False


    def finalizes(self, other):
        # If partitionless scheme
        if self.is_final_row:
            if other.is_final_row:
                return True
            elif len(other.segments) == 1:
                    return True
        
        # If single partition scheme
        elif len(set(self.partition_scheme)) == 1:
            if other.is_final_row:
                return True
            else:
                if len(set(other.partition_scheme)) == 1:
                    return self.connects_all_partitions(other)
        
        # If multipart scheme
        elif len(set(self.partition_scheme)) > 1:
            if other.is_final_row:
                 return False
            else:
                if len(other.segments) == 1:
                    return self.connects_all_partitions(other)
        else:
            return False


    def connects_all_partitions(self, other):
        '''This function assumes both schemes possess segments and are not the partitionless scheme.'''
        try:
            if self.is_final_row or other.is_final_row:
                raise ValueError("One of the rows was the partitionless scheme!")
            connections = [False for i in range(0, len(self.partition_scheme))]
            for i in range(0, len(self.segments)):
                for j in range(0, len(other.segments)):    
                    if not connections[i]:
                        if self.segments[i].connects(other.segments[j]):
                            connections[i] = True   
            
            # Maybe source of error, I'm tired while writing this.
            for i in range(0, len(connections)):
                if connections[i]:
                    key = self.partition_scheme[i]
                    for j in range(0, len(connections)):
                        if self.partition_scheme[j] == key:
                            connections[j] = True
            # If there is a false in the bool vector connections, this will return False.
            return not False in connections
        except ValueError as ve:
            print(ve)
        

    def traverse_with_memoization(self, water, end, depth, base_depth):
        # If the subrow memo vector has not been initialized for the puzzle depth
        if not self.depth_memoized:
            self.depth_memoized = [False for i in range(0, base_depth)]
            self.memos = [0 for i in range(0, base_depth)]
        
        if depth == 1:
            print(f"{self.parent_row.seed / 2**self.parent_row.length:.2%}")

        count = 0
        
        if end:
            if depth == base_depth - 1:
                count += 1
            else:
                count += self.traverse_with_memoization(water, end, depth + 1, base_depth)

        # If the current depth for this subrow has not been counted
        elif not self.depth_memoized[depth - 1]:            

            # Puzzle has reached the row before the last and considers the final row placements.
            if depth == base_depth - 1:
                for finalizer in self.finalizers:

                    # If forced end is set to True
                    if end:
                        if finalizer.is_final_row:
                            count += 1
                    else:
                        count += 1

            elif depth != base_depth - 1:

                if not water:
                    for successor in self.successors:
                        if successor.is_start:
                            has_water = len(successor.segments) >= 1
                            count += successor.traverse_with_memoization(has_water, end, depth + 1, base_depth)
                
                else:
                    for successor in self.successors:
                        if successor.is_final_row:
                            is_end = True
                        else:
                            is_end = False
                        count += successor.traverse_with_memoization(water, is_end, depth + 1, base_depth)
            else:
                print("breakpoint print out")


            # Make it known this depth has been counted for this subrow
            self.depth_memoized[depth - 1] = True
            # Assign the count to this subrows depth level
            self.memos[depth - 1] = count
        # If this depth has already been counted
        else:
            count = self.memos[depth - 1]

        #print(f"Seed: {self.parent_row.seed}, Depth: {depth}, Count: {count}")
        return count


    def traverse(self, string, water, end, depth, base_depth):      
        '''Travereses without memoizing, but allows for pattern printouts as a trade off.'''
       # If the subrow memo vector has not been initialized for the puzzle depth
        string[depth - 1] = self.parent_row
        if depth == 1:
            print(f"{self.parent_row.seed / 2**self.parent_row.length:.2%}")
        # Keep track of count at this node, always starts at zero
        count = 0

        if end:
            if depth == base_depth - 1:
                string[depth] = self.parent_row
                self.print_puzzle(string)
                count += 1
            else:
                count += self.traverse(string, water, end, depth + 1, base_depth)

        # Puzzle has reached the row before the last and considers the final row placements.
        elif depth == base_depth - 1:
            for finalizer in self.finalizers:

                # If forced end is set to True
                if end:
                    if finalizer.is_final_row:
                        string[depth] = finalizer.parent_row
                        self.print_puzzle(string)
                        count += 1
                else:
                        string[depth] = finalizer.parent_row
                        self.print_puzzle(string)
                        count += 1

        elif depth != base_depth - 1:

            if not water:
                for successor in self.successors:
                    if successor.is_start:
                        has_water = len(successor.segments) >= 1
                        count += successor.traverse(string, has_water, end, depth + 1, base_depth)
            
            else:
                for successor in self.successors:
                    if successor.is_final_row:
                        is_end = True
                    else:
                        is_end = False
                    count += successor.traverse(string, water, is_end, depth + 1, base_depth)
        else:
            print("breakpoint print out")

        #print(f"Seed: {self.parent_row.seed}, Depth: {depth}, Count: {count}")
        return count

    def print_puzzle(self, string):
        length = len(string[0].bits)
        depth = len(string)
        with open(f"debug\\debug_[{depth}x{length}].txt", 'a') as file:
            RowScheme.debug_count += 1
            file.write(f"{RowScheme.debug_count}\n")
            for row in string:
                for bit in row.bits:
                    if bit == 1:
                        file.write("1 ")
                    else:
                        file.write(f"0 ")
                file.write(f"  {row.seed}\n")        
            file.write("\n")
