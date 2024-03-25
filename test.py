def find_duplicates(lst):
    duplicates = {}
    for i, item in enumerate(lst):
        if item in duplicates:
            duplicates[item].append(i)
        else:
            duplicates[item] = [i]

    result = {item: indices for item, indices in duplicates.items() if len(indices) > 1}
    return result


# Example usage
my_list = [1, 2, 3, 4, 2, 5, 3, 6]
duplicates_indices = find_duplicates(my_list)

for item, indices in duplicates_indices.items():
    print(f"Item {item} is duplicated at indices: {indices}")
