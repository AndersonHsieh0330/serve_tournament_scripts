'''
    this should work with any # amount of signed up teams as one "team"
    aka works for both 3ps and reverses or any future tournament formats

    Terminologies Used in comments and variables:
        game - Refers to each period of game play, usually one game contains 2 courts for Friday tournaments at CIF
        court - Refers to each gym at CIF gym 1/2. Contains 2 sides.
        side - Refers to each side of the net. Contains 6 players in a normal volleyball game; Contains N teams based on tournament format. Ex. N = 2 for 3ps tournament
        team - same thing as a signup team, contains X number of players.
        signup team - the team that members sign up as in the registration form. Contains X number of players.
        N - number of signup teams on each 6 man team. N = 6/X. For example, N = 3 for 3ps tournament
        X - number of players on each signup teams. 6 = X * N.
'''
from write_output import *
from parse_schedule import *
from util import *
import sys

def check_play_with(cur_schedule, num_of_teams):
    '''
        this is a 2D array that shows how many times each team play with another team
        for example: play_with_table[1][3]
        this shows the number of times team 2 play with team 4 
        note that all the index +1 = team number
        Also play_with_table[1][3] should = play_with_table[3][1]
    '''
    play_with_table = [[0 for i in range(num_of_teams)] for i in range(num_of_teams)]

    # iterate through each side and fill information into the play_with_table
    for game in cur_schedule:
        for court in game:
            # assumes if the very first slot is a 0 that game is left empty on purpose, so we skip it
            # which means our check_zeros function executed before this function and passed
            if court[0][0] == 0: continue
            for side in court:
                # compute combination of every team with every other team in the same side
                for team in side:
                    for team_2 in side:
                        # skipping the current checking team itself
                        if team == team_2: continue
                        play_with_table[team-1][team_2-1] = play_with_table[team-1][team_2-1] + 1

    return play_with_table

def check_play_against(cur_schedule, num_of_teams):
    '''
        this is a 2D array that shows how many times each team play against another team
        for example: play_with_table[1][3]
        this shows the number of times team 2 play with team 4 
        note that all the index +1 = team number
        Also play_with_table[1][3] should = play_with_table[3][1]
    '''
    play_against_table = [[0 for i in range(num_of_teams)] for i in range(num_of_teams)]

    # iterate through each court and fill information into the play_against_table
    for game in cur_schedule:
        for court in game:
            # assumes if the very first slot is a 0 that game is left empty on purpose, so we skip it
            # which means our check_zeros function executed before this function and passed
            if court[0][0] == 0: continue
            for side_index, side in enumerate(court):
                for team in side:
                    # xor with 1 flips a 0 to 1, and a 1 to 0
                    # we use this to index the other side in the same court
                    # this assumes no teams play against itself, aka check_duplicate_teams already ran and passed
                    for team_2 in court[side_index^1]:
                        play_against_table[team-1][team_2-1] = play_against_table[team-1][team_2-1] + 1

    return play_against_table

# check that no team is numbered 0 by accident
# if there is a zero check that all the slots in court are 0s(empty court left on purpose)
def check_zeros(cur_schedule, num_of_total_games):
    games_with_error = [False for i in range(num_of_total_games)]

    for game_index, game in enumerate(cur_schedule):
        for court in game:
            empty_court_warning = False # true when we expect the current court is zero
            for side_index,side in enumerate(court):
                if games_with_error[game_index]: break # already detected error in this game, skip
                for team_index,team in enumerate(side):
                    if team == 0:
                        # team number 0 is detected
                        if team_index == 0 and side_index == 0:
                            # this is the first team of the first side when team number 0 is detected, don't report error yet
                            # set empty court warning
                            empty_court_warning = True
                        else:
                            if not empty_court_warning:
                                # zero is detected not at first side of first team, and we didn't anticipate this(warning is false)
                                # report error
                                games_with_error[game_index] = True
                                break
                    else:
                        # current team number is not zero
                        if empty_court_warning:
                            # but we're anticipating a zero
                            # report error
                            games_with_error[game_index] = True
                            break
    
    # the games with 1 at its index contain errors
    return games_with_error

    
# check that no one team is on two courts or two sides of the same court during the same game
def check_duplicated_teams(cur_schedule, num_of_total_games):
    games_with_error = [False for i in range(num_of_total_games)]

    for game_index, game in enumerate(cur_schedule):
        temp = set()
        for court in game:
            for side in court:
                for team in side:
                    if team in temp:
                        games_with_error[game_index] = True
                        break
                    else:
                        # remember that 0s are reserved for empty court on purpose
                        if team != 0: temp.add(team)
    
    # the games with 1 at its index contain errors
    return games_with_error

'''       
    check each team plays the same amount of games
    this is implemented separately from 'check_duplicated_teams' 
    in case we do want different number of games between each teams
    even though we basically run the same code to step through each team twice
'''
def check_num_of_games(cur_schedule, num_of_teams):
    num_of_games_each_team_dict = {key: 0 for key in range(num_of_teams)}

    # iterate through each team and count the number of times they appear
    for game_index, game in enumerate(cur_schedule):
        for court in game:
            for side in court:
                for team in side:
                    if team != 0: 
                        num_of_games_each_team_dict[team-1] = num_of_games_each_team_dict[team-1] + 1

    return num_of_games_each_team_dict


def main():
    input_file = sys.argv[1] # input file path           

    input_file = open(input_file, "rt")
    num_of_teams, num_of_total_games, n, schedule = parse_input_schedule_file(input_file)

    # sanity checks
    sanity_check_passed = True
    if num_of_total_games != len(schedule) :
        print("Number of games in the schedule not equal to number of total games specified")
        sanity_check_passed = False

    games_with_duplicate_teams = check_duplicated_teams(schedule, num_of_total_games)
    games_with_team_zero_error = check_zeros(schedule, num_of_total_games)

    sanity_check_passed = not(1 in games_with_team_zero_error or 1 in games_with_duplicate_teams)
    
    # open output file and start writing to it
    output_file = open("output.txt", "wt")
    write_output_header(output_file, num_of_teams, num_of_total_games, n, schedule)
    write_output_game_list(
        output_file,
        games_with_duplicate_teams,
        "Games marked with True has one team appearing in two different slots.\nThe duplicated number can be on the same side, opposite teams or different court"
    )
    write_output_game_list(
        output_file,
        games_with_team_zero_error,
        "Games marked with True has team 0 specified, but that game was not left empty intentionally.\nWhen team 0 is specified in one slot, all the other slots in that court should be 0 as well,\nshowing that that course is intentionally left empty"
   )

    # no need to run the rest of the tests if duplicate team error exists
    if sanity_check_passed:

        num_of_games_each_team_dict = check_num_of_games(schedule, num_of_teams)
        write_output_team_dict(
            output_file,
            num_of_games_each_team_dict,
            "Number of games played by each team is shown below"
        )

        play_with_table = check_play_with(schedule, num_of_teams)
        write_output_2d_array(
            output_file, 
            play_with_table, 
            "Play with table shown below.\nFor better readability copy the whole block and paste in to excel. T stands for Team"
        )

        play_against_table = check_play_against(schedule, num_of_teams)
        write_output_2d_array(
            output_file, 
            play_against_table, 
            "Play against table shown below.\nFor better readability copy the whole block and paste in to excel. T stands for Team"
        )

        # check thresholds if they are defined, run test if both defined, else just ignore
        if len(sys.argv) >= 4 and sys.argv[2].isnumeric() and sys.argv[3].isnumeric():
            play_with_threshold = int(sys.argv[2]) # max amount of games one team can play with another
            play_against_threshold = int(sys.argv[3]) # max amount of games one team can play aginst another
            play_with_threshold_test_failed = comp_num_in_2d_array(play_with_table, play_with_threshold)
            play_against_threshold_test_failed = comp_num_in_2d_array(play_against_table, play_against_threshold)
            write_output_threshold_tests(output_file, "play_with", play_with_threshold, play_with_threshold_test_failed)
            write_output_threshold_tests(output_file, "play_against", play_against_threshold, play_against_threshold_test_failed)

            # print to console
            print("play with test with max number " + str(play_with_threshold) + (" failed" if play_with_threshold_test_failed else " passed"))
            print("play against test with max number " + str(play_against_threshold) + (" failed" if play_against_threshold_test_failed else " passed"))
    else:
        output_file.write("\nSanity checks did not pass, other tests were not ran. Get rid of those errors first\n")

    print("script finished, output written to output.txt")
    output_file.close()
    input_file.close()
        
if __name__ == '__main__':
    main()