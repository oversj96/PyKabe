import segment as s


def build_part_set(bottom_row, top_row_scheme):
    if not top_row_scheme.partition_set or len(bottom_row.segments) == 0:
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
                new_set[i] = top_row_scheme.partition_set[j]

            else:
                if len(bottom_row.segments) > len(
                    top_row_scheme.parent_row.segments
                ):
                    for k in range(i, len(top_row_scheme.partition_set)):
                        top_row_scheme.partition_set[k] += 1

    for i in range(0, len(set(top_row_scheme.partition_set)) - 1):
        key = new_set[i]
        for j in range(i, len(new_set)):
            if new_set[j] == key:
                new_set[j] = i

    return new_set


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
