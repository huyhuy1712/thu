def get_sequence_list(num):
    if num == 0:
        return [0]

    result, i = [1], 2
    while sum(result) != num:
        if sum(result) + i > num:
            for j in range(i - 1, 0, -1):
                if sum(result) + j <= num:
                    result.append(j)
        else:
            result.append(i)
        i += 1

    return sorted(result, reverse=True)