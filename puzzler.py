import sys
from pathlib import Path

import row as r
from restrictive_growth_strings import restrictive_growth_strings as rgs


class Puzzler:
    def __init__(self, depth, length, fast_count):
        self.length = length
        self.fast_count = False if fast_count.lower().startswith('y') else True
        self.depth = depth
        self.total_pattern_count = 2**(self.length*self.depth)
        self.good_patterns = 0
        self.partitions = [rgs(i) for i in range(0, length + 1)]
        self.rows = [r.Row(i, self.length, self.partitions) for i in range(0, 2**length)]
        self.node_count = 0
        for row in self.rows:
            self.node_count += len(row.nodes)

        # Make each subrow aware of all other subrows
        print("\n")
        for top in self.rows:
            print(f"Mapping sub rows... {(top.seed / 2**self.length)*100:.2f}%", end="\r")
            for bottom in self.rows:
                if not top.forms_pool(bottom) and top.is_trivially_contiguous(bottom):
                    r.build_tree(top, bottom)
        print("Sub row mapping complete!" + ' ' * 20 + "\n")


        if self.fast_count:
            self.count_patterns_memoized()
        else:
            path = Path.cwd() / 'debug'
            if not path.exists():
                path.mkdir()
            with open(f"debug\\debug_[{self.depth}x{self.length}].txt", 'w') as file:
                file.write(f"Puzzle Debug: Size: [{self.depth} x {self.length}]\n")
                file.write(f"Total Possible Pattern Count: {self.total_pattern_count}\n")
                file.write(f"Total Legal Patterns: Execution must be allowed to finish...\n")
            self.count_patterns()
        sys.stdout.write("\rCounting Complete!" + ' ' * 20 + "\n")

        print(f"\nThere are {self.good_patterns:,} legal patterns in a [{self.depth} x {self.length}] nurikabe game. There were {self.total_pattern_count:,} possible patterns.\n")
        print(f"{self.good_patterns / self.total_pattern_count:.{self.length - 2}%} were good patterns.\n")
        print(f"Nodes traversed: {self.rows[0].nodes[0].recursion_calls}\n")

    
    def count_patterns(self):
        for row in self.rows:
            for node in row.nodes:
                if node.is_start:
                    if len(node.segments) >= 1:
                        water = True
                    else:
                        water = False

                    self.good_patterns += node.traverse(['' for i in range(0, self.depth)], water, False, 1, self.depth)
                    #self.good_patterns += scheme.traverse_with_memoization(water, False, 1, self.depth)
        with open(f"debug\\debug_[{self.depth}x{self.length}].txt", "r") as file:
            contents = file.readlines()
        with open(f"debug\\debug_[{self.depth}x{self.length}].txt", "w") as file:
            contents.insert(3, "\n\n")
            contents[2] = f"Total Legal Patterns: {self.good_patterns}"        
            file.writelines(contents)

            
    # Utilizes memoization and converts the problem into a polynomial time solution
    # The loss in speed this time around comes from row mapping
    def count_patterns_memoized(self):
        for row in self.rows:
            for node in row.nodes:
                if node.is_start:
                    if len(node.segments) >= 1:
                        water = True
                    else:
                        water = False

                    self.good_patterns += node.traverse_with_memoization(water, False, 1, self.depth)


def scrub_input_and_run():
    while True:
        try:
            length = int(input("Please enter the row length of the puzzle: "))
            depth  = int(input("Please enter the depth/row count of the puzzle: "))
            debug  = input("Use debugger? Warning: this will dramatically slow the counting process to exponential speed! [y/n]: ")
            if length < 2 or depth < 2:
                raise ValueError("A number less than 2 was entered for either dimension, please try again.")
            else:
                break
        except ValueError as ve:
            print(ve)

    p = Puzzler(length, depth, debug)
    print(p)


if __name__ == "__main__":
    # Get the correct inputs and run the program
    scrub_input_and_run()
