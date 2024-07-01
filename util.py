def comp_num_in_2d_array(two_d_array, num):
    for row in two_d_array:
        for item in row:
            if item > num: return True