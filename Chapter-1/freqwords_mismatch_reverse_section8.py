

def read_input(filename):
    try:
        input_file = open(filename, "r")
        genome = input_file.readline()[:-1]
        k, d = input_file.readline().split(" ")
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return genome, int(k), int(d)

nucleotides = ['A', 'T', 'C', 'G']

def hamming_distance(genome1, genome2):
    mismatch_count = 0
    for i in range(0, len(genome1)):
        if genome1[i] != genome2[i]:
            mismatch_count += 1
    return mismatch_count

def neighbors(pattern, d):
    if d == 0:
        return pattern
    if len(pattern) == 1:
        return ['A', 'T', 'C', 'G']
    else:
        neighborhood = []
        suffix_neighbors = neighbors(pattern[1:], d)
        for sn in suffix_neighbors:
            if hamming_distance(pattern[1:], sn) < d:
                for n in nucleotides:
                    neighborhood.append(n+sn)
            else:
                neighborhood.append(pattern[0]+sn)
        return neighborhood

def frequency_table(text, k):
    frequency_dict = dict()
    n = len(text)
    for i in range(0, n-k):
        pattern = text[i:i+k]
        if pattern in frequency_dict:
            frequency_dict[pattern] += 1
        else:
            frequency_dict[pattern] = 1
    return frequency_dict

def max_map(map):
    return max(map.values())

def frequent_words(text, k):
    frequent_patterns = []
    frequency_map = frequency_table(text, k)
    max = max_map(frequency_map)
    for pattern in frequency_map:
        if frequency_map[pattern] == max:
            frequent_patterns.append(pattern)
    return frequent_patterns

def reverse_complement(string):
    reverse_string = ''
    for i in range(len(string)-1, -1, -1): # 2nd arg not inclusive hence -1
        if string[i] == 'A':
            reverse_string += 'T'
        elif string[i] == 'T':
            reverse_string += 'A'
        elif string[i] == 'C':
            reverse_string += 'G'
        elif string[i] == 'G':
            reverse_string += 'C'
        else:
            print('This string contains a weird thing')
    return reverse_string

def frequent_words_with_mismatch_and_reverse(genome, k, d):
    patterns = []
    frequency_dict = dict()
    n = len(genome)
    for i in range(0, n-k):
        pattern = genome[i:i+k]
        neighborhood = neighbors(pattern, d)
        reverse_pattern = reverse_complement(pattern)
        reverse_neighborhood = neighbors(reverse_pattern, d)

        for j in range(0, len(neighborhood)-1):
            neighbor = neighborhood[j]
            reverse_n = reverse_complement(neighbor)
            if neighbor in frequency_dict:
                frequency_dict[neighbor] += 1
            else:
                frequency_dict[neighbor] = 1

            if reverse_n in frequency_dict:
                frequency_dict[reverse_n] += 1
            else:
                frequency_dict[reverse_n] = 1

        for j in range(0, len(reverse_neighborhood)-1):
            reverse_neighbor = reverse_neighborhood[j]
            neighbor = reverse_complement(reverse_neighbor)
            if reverse_neighbor in frequency_dict:
                frequency_dict[reverse_neighbor] += 1
            else:
                frequency_dict[reverse_neighbor] = 1

            if neighbor in frequency_dict:
                frequency_dict[neighbor] += 1
            else:
                frequency_dict[neighbor] = 1

    max = max_map(frequency_dict)
    for key in frequency_dict:
        if frequency_dict[key] == max:
            patterns.append(key)
    return patterns


def start():
    genome, k, d = read_input("dataset.txt")
    result = frequent_words_with_mismatch_and_reverse(genome, k, d)
    for pattern in result:
        print(pattern, end=" ")


if __name__ == '__main__':
    start()
