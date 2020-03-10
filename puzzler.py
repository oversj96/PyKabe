import row as r
from restrictive_growth_strings import restrictive_growth_strings as rgs


class Puzzler:


    def __init__(self, length, depth, fast_count):
        self.length = length
        self.fast_count = False if fast_count.lower().startswith('y') else True
        self.depth = depth
        self.good_patterns = 0
        self.partitions = [rgs(i) for i in range(0, length + 1)]
        self.rows = [r.Row(i, self.length, self.partitions) for i in range(0, 2**length)]
        self.scheme_count = 0
        for row in self.rows:
            self.scheme_count += len(row.schemes)

        # Make each subrow aware of all other subrows
        print("\nMapping sub rows...\n")
        for top in self.rows:
            print(f"{top.seed / 2**self.length:.2%}")
            for bottom in self.rows:
                if not top.forms_pool(bottom) and top.is_trivially_contiguous(bottom):
                    r.map_subrows(top, bottom)
        print("\nSub row mapping complete!\n")

        print("Counting", end=" ")
        if self.fast_count:
            print("using memoization...\n")
            self.count_patterns_memoized()
        else:
            print("using debugger functions...\n")
            with open("debug.txt", 'w') as file:
                file.write(f"Preparing file for debug...\n\n")
            self.count_patterns()

        print(f"\nThere are {self.good_patterns} patterns in a [{self.length} x {self.depth}] nurikabe game. There were {2**self.length**2} possible patterns.\n")
        print(f"{self.good_patterns / 2**self.length**2:.{self.length - 2}%} were good patterns.\n")

    
    def count_patterns(self):
        for row in self.rows:
            for scheme in row.schemes:
                if scheme.is_start:
                    if len(scheme.segments) >= 1:
                        water = True
                    else:
                        water = False

                    self.good_patterns += scheme.traverse(['' for i in range(0, self.depth)], water, False, 1, self.depth)
                    #self.good_patterns += scheme.traverse_with_memoization(water, False, 1, self.depth)

    # Utilizes memoization and converts the problem into a polynomial time solution
    # The loss in speed this time around comes from row mapping
    def count_patterns_memoized(self):
        for row in self.rows:
            for scheme in row.schemes:
                if scheme.is_start:
                    if len(scheme.segments) >= 1:
                        water = True
                    else:
                        water = False

                    self.good_patterns += scheme.traverse_with_memoization(water, False, 1, self.depth)


if __name__ == "__main__":
    # Test the rgs function and count the partition sets which should result in a Bell Number.
    # Input should be from 0 to 10 as linearly higher numbers are exponentially harder to build
    # the set of all partitions of a set for.
    puzzler = Puzzler(int(input("Please enter the row length of the puzzle: ")),
                      int(input("Please enter the depth/row count of the puzzle: ")),
                      input("Use debugger? Warning: this will dramatically slow the counting process to exponential speed! [y/n]: "))
