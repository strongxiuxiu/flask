def digital_computation(num_list)
    new_numbers = []
    for n in num_list
        new_numbers.append(int(n))
    num_1 = new_numbers
    num_2 = []
    num_1.sort()
    for i in num_1
        num = int(i) + 1
        num_2.append(num)
    list3 = list(set(num_2).difference(set(num_1)))
    list3.sort()
    if list3
        return list3[0]
    else
        num = int(num_1[-1]) + 1
        return num