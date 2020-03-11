import segment as s


def build_part_set(bottom_row, top_row_scheme):
    if not top_row_scheme.partition_scheme or len(bottom_row.segments) == 0:
        return []
    # Construct a new partiton set to be used
    new_set = [i for i in range(0, len(bottom_row.segments))]
    # For each segment in the bottom row...
    for i in range(0, len(bottom_row.segments)):
        # ...for each segment in the top row...
        for j in range(0, len(top_row_scheme.segments)):
            # determine of the bottom row connects to the top
            if bottom_row.segments[i].connects(top_row_scheme.segments[j]):
                # If it does, the new partition set is updated with the number
                new_set[i] = top_row_scheme.partition_scheme[j]
            
            else:
                if len(bottom_row.segments) > len(top_row_scheme.parent_row.segments):
                    for k in range(i, len(top_row_scheme.partition_scheme)):
                        top_row_scheme.partition_scheme[k] += 1

    for i in range(0, len(set(top_row_scheme.partition_scheme)) - 1):
        key = new_set[i]
        for j in range(i, len(new_set)):
            if new_set[j] == key:
                new_set[j] = i

    return new_set


def determine_part_set(bottom_row, top_row_scheme):
    # changed = [False for i in range(0, len(bottom_row.segments))]

    # part_numbers = []
    # new_set = [0 for i in range(0, len(bottom_row.segments))]

    # for i in range(0, len(top_row_scheme.segments)):
    #     segment_numbers = []
    #     for j in range(0, len(bottom_row.segments)):
    #         if top_row_scheme.segments[i].connects(bottom_row.segments[j]):
    #             segment_numbers.append(j)
    #     if segment_numbers:
    #         part_numbers.append(segment_numbers.copy())
    #     else:
    #         part_numbers.append([])
    #     del segment_numbers[:]
        
    # for i in range(0, len(bottom_row.segments)):
    #     if not changed[i]:
    #         for j in range(0, len(part_numbers)):
    #             if part_numbers[j]:
    #                 for k in range(0, len(part_numbers[j])):
    #                     new_set[k] = i
    #                     changed[k] = True
    #             else:
    #                 new_set[i] = i

    # return new_set
    
    # We are interested in the set created given the scheme

    part_hit = [None for i in range(0, len(bottom_row.segments))]

    for i in range(0, len(bottom_row.segments)):
        for j in range(0, len(top_row_scheme.segments)):
            if bottom_row.segments[i].connects(top_row_scheme.segments[j]):
                part_hit[i] = top_row_scheme.partition_scheme[j]
    
    new_set = [-1 for i in range(0, len(bottom_row.segments))]
    changed = [False for i in range(0, len(bottom_row.segments))]
    for i in range(0, len(bottom_row.segments)):
        next_part_num = max(new_set) + 1
        if part_hit[i] == None:
            new_set[i] = next_part_num
        else:
            key = part_hit[i]
            for j in range(i, len(bottom_row.segments)):
                if part_hit[j] == key and not changed[j]:
                    new_set[j] = next_part_num
                    changed[j] = True

    return new_set if -1 not in new_set else print(f"Error: set with -1 detected! Seed: {bottom_row.parent_row.seed}")



    



def determine_segments(row):
    seg_list = []
    columns = []
    for i in range(0, len(row)):
        if row[i] == 0:
            columns.append(i)
            if i == len(row) - 1:
                seg_list.append(s.Segment(columns.copy()))
        elif row[i] == 1 and len(columns) > 0:
            seg_list.append(s.Segment(columns.copy()))
            del columns[:]
    return seg_list


if __name__ == "__main__":
    pass
    # length = 4
    # part_schemes = [rgs(i) for i in range(0, length + 1)]
    # r1 = r.Row(10, length, part_schemes)
    # r2 = r.Row(3, length, part_schemes)
    # scheme = r1.schemes[1]

    # print(build_part_set(r1, scheme))
