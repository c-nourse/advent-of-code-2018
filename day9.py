input = '477 players; last marble is worth 70851 points'

def play_game(num_players, final_marble):
    
    board = []
    scores = {}

    val = 0
    i = 0    
    while val <= final_marble:
    
        if val != 0 and val % 23 == 0:
            try:
                scores[str(player)] += val
            except KeyError:
                scores[str(player)] = val
            i_pre = i
            i = i - 7
            scores[str(player)] += board.pop(i)
            # If i is positive, shift it back on to be counter clockwise
            #if i >= 0:
            #    i -= 1s

            #print('{} --> {}'.format(i_pre, i))

        elif val == 1:
            board.append(val)
            i = 1
        
        elif val == 0:
            board.append(val)
    
        else:
            i = (i + 2) % len(board)
            #print(i)
            board.insert(i, val)
    
        player = (val) % num_players
        val += 1
        #print(player, ': ', board)
        if val % 10000 == 0:
            print(val)

    print(max(scores.values()))
    
    return board, scores


board, scores = play_game(9, 25)
board, scores = play_game(13, 7999)
board, scores = play_game(17, 1104)
board, scores = play_game(477, 7085100)