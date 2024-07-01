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
######################################################################################
######### Edit this section and nothing else if ur not modifying the script ##########
######################################################################################
num_of_teams = 14
num_of_total_games = 11
n = 2
schedule = [
[[[1,2],[3,4]],[[5,6],[7,8]]],
[[[9,10],[11,12]],[[13,14],[1,5]]],
[[[2,6],[9,13]],[[3,7],[10,14]]],
[[[4,8],[5,9]],[[6,10],[7,11]]],
[[[2,7],[6,12]],[[3,11],[5,14]]],
[[[2,12],[3,13]],[[4,14],[8,10]]],
[[[4,5],[8,9]],[[12,13],[1,14]]],
[[[2,3],[6,7]],[[1,4],[5,11]]],
[[[8,12],[9,13]],[[10,14],[1,11]]],
[[[3,13],[6,11]],[[4,12],[7,10]]],
[[[1,8],[2,9]],[[0,0],[0,0]]]
# add more rows if needed
# if one of the courts during the last game is purposely left open, write all 0s
]
######################################################################################
######### Edit this section and nothing else if ur not modifying the script ##########
######################################################################################

def check_play_with(cur_schedule):
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

def check_play_against(cur_schedule):
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
def check_zeros(cur_schedule):
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
def check_duplicated_teams(cur_schedule):
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
def check_num_of_games(cur_schedule):
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
    # sanity checks
    sanity_check_passed = True
    if num_of_total_games != len(schedule) :
        print("Number of games in the schedule not equal to number of total games specified")
        sanity_check_passed = False

    games_with_duplicate_teams = check_duplicated_teams(schedule)
    print(games_with_duplicate_teams)

    if 1 in games_with_duplicate_teams:
        print("Same team appeared twice in the same game")
        sanity_check_passed = False

    games_with_team_zero_error = check_zeros(schedule)
    print(games_with_team_zero_error)

    if 1 in games_with_team_zero_error:
        print("Team number 0 appeared in a game not left blank on purpose")
        sanity_check_passed = False

    # no need to run the rest of the tests if duplicate team error exists
    if sanity_check_passed:

        num_of_games_each_team_dict = check_num_of_games(schedule)
        print(num_of_games_each_team_dict)

        play_with_table = check_play_with(schedule)
        print(play_with_table)

        play_against_table = check_play_against(schedule)
        print(play_against_table)
        

if __name__ == '__main__':
    main()