import sys
import math

def parse_line(cur_line):
    max_num = 0

    cur_line_list = cur_line.split() # this works for split by tab or space

    # filter by number
    cur_line_number_only = []
    for string in cur_line_list:
        if string.isnumeric(): 
            num = int(string)
            cur_line_number_only.append(num)
            max_num = num if num > max_num else max_num

    # return a tuple of list of numbers + the max number in that list
    # for example: 1 2 vs 3 4 5 6 vs 7 8 will return [1,2,3,4,5,6,7,8]
    return (cur_line_number_only, max_num)

def parse_input_schedule_file(file):
    # read line by line and count how many games there are
    num_of_teams = 0 
    num_of_total_games = 0
    n = 0
    schedule = []

    # parse first line to infer the variable n
    # assume there will always be two courts, 

    while True:
        cur_line = file.readline() # returns an empty string(falsy) if end of file is reached

        # end of schedule is reached when 
        # 1. cur_line is a empty string
        # or
        # 2. first character is not a number
        if not cur_line or not cur_line[0].isnumeric():
            break

        result_tuple = parse_line(cur_line)
        result_list = result_tuple[0]
        num_of_teams = result_tuple[1] if result_tuple[1] > num_of_teams else num_of_teams

        if not n :
            # n is not set yet, we're processing first line
            n = math.floor(len(result_list)/2/2)
            if n < 1: sys.exit("Syntax error in input file schedule, N < 1")

        if len(result_list) < n*2*2:
            if len(result_list) == n*2:
                # one of the games left empty intentionally, fill 0s in
                for i in range(n*2):
                    result_list.append(0)
            else:
                # len(result_list) != n*2, syntax error. This should never happen
                sys.exit("Syntax error in input file schedule, one of the rows is none empty but number of teams don't fill up half of the court")
            
        game_list = []
        for court_index in range(2):
            court_list = []
            for side_index in range(2):
                side_list = []
                for n_index in range(n):
                    side_list.append(result_list[n*2*court_index + n*side_index + n_index])
                court_list.append(side_list)
            game_list.append(court_list)

        schedule.append(game_list)

        num_of_total_games += 1
    return (num_of_teams, num_of_total_games, n, schedule)
