'''
    This file contains functions for printing result of tests into a output.txt file
    Also functions that parses input schedule in input.txt into a 4D array so we can 
    run tests on it
'''
def write_output_header(file, num_of_teams, num_of_total_games, n, schedule):
    file.write("Report of schedule analysis begins")
    file.write("\n")
    file.write("Number of teams in total = " + str(num_of_teams))
    file.write("\n")
    file.write("Number of games in total = " + str(num_of_total_games))
    file.write("\n")
    file.write("Number of teams per side of the net (N) = " + str(n))
    file.write("\n")
    file.write("Input schedule shown below, you may copy this directly into excel if you're happy with this schedule.\nJust select the entire block, this block of text is formatted to paste into excel nicely")
    file.write("\n")
    file.write('\n'.join(['\t'.join(['\tvs'.join([''.join(['\t{}'.format(team) for team in side]) for side in court]) for court in game]) for game in schedule]))
    file.write("\n")

def write_output_game_list(file, game_list, description):
    # game_list is a array of items
    # game index starts at 0
    file.write("\n")
    file.write(description)
    file.write("\n")
    for game_index,game in enumerate(game_list):
        file.write("Game " + str(game_index+1) + " : " + str(game) + "\n")

def write_output_team_dict(file, team_dict, description):
    # team_dict is a disctionary of items
    # team index starts at 0
    file.write("\n")
    file.write(description)
    file.write("\n")
    for team_index in range(len(team_dict)):
        file.write("Team " + str(team_index+1) + " : " + str(team_dict[team_index]) + "\n")

def write_output_2d_array(file, two_d_array, description):
    file.write("\n")
    file.write(description)
    file.write("\n")
    file.write(format_2d_array(two_d_array))
    file.write("\n")

def format_2d_array(two_d_array):
    # reference : https://stackoverflow.com/a/17871279
    first_row = "\t" + ''.join(['T{}\t'.format(i+1) for i in range(len(two_d_array))]) + "\n"
    return first_row + '\n'.join([''.join(['T' + str(row_index+1)] + ['\t{}'.format(item) for item in row]) for row_index,row in enumerate(two_d_array)])

def write_output_threshold_tests(file, threshold_str, threshold, failed):
    file.write("\n")
    if failed:
        file.write("A " + threshold_str + " of " + str(threshold) + " was set and a larger number was found, test failed")
    else:
        file.write("A " + threshold_str + " of " + str(threshold) + " was set and no greater number was found, test passed")
