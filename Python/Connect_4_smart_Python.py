
PLAYER, COM, MODE = "O", "X", "Undeclared"
ROWS, COLUMNS = 7, 7
BOARD = [["|"] * COLUMNS for i in range(ROWS)]
COM_MOVES, PL_MOVES = [], []
FUTURE2, FUTURE3, FUTURE2TO4, UNPROTECTED_COM, UNPROTECTED_PL = [], [], [], [], []
DANGEROUS3, DANGEROUS2, DANGEROUS2TO4 = [], [], []
CANT_WIN_MOVES = []

# def set_opponent()
# use class player

def set_difficulty_mode():
    valid = False
    while not valid:
        ans = input("CHOOSE DIFFICULTY MODE: \n --> Easy mode (press 1) \n" +
            " --> Competitive mode (press 2) \n --> Very competitive mode (press 3) \n...You pick: ")
        try:
            ans = int(ans)
            if ans != 1 and ans != 2 and ans != 3:  # self - sabotazing
                ans = "non valid"
                ans = int(ans)
            valid = True
        except:
            print("\nEither choose \"1\" or \"2\"")
    if ans == 1: return "Easy"
    elif ans == 2: return "Competitive"
    else: return "Very Competitive"

def print_board(BOARD):
    for i in range(ROWS):
        print(f"{i}  ", end="")
        for j in range(COLUMNS):
            print("    ", BOARD[i][j], end="")
        print("\n")
    print("-" * 7 * COLUMNS, end="\n"+"    ")
    for i in range(COLUMNS): print("     "+str(i),end="")
    print("\n")

def print_winner(BOARD, top_r, top_c, direction):
    print("GAME OVER...")
    if BOARD[top_r][top_c] == PLAYER:
        print("WOW, YOU WON!!!!")
    else:
        print("Computer won... TOLD YA")

def clear_terminal():
    import platform, os
    if platform.system() == "Windows": os.system("cls")
    else:  os.system("clear")

def clear_terminal3():
    import os
    os.system('cls' if os.name=='nt' else 'clear')

def doesnt_exist_on_list(element, a_list):
    not_in_list = True
    for el in a_list:
        if element==el:
            not_in_list = False
            break
    return not_in_list

def mark_crusial_positions(new_r, new_c, sequen, symbol):
    global DANGEROUS2, FUTURE2, DANGEROUS3, FUTURE3
    crucial_lists, i = [DANGEROUS2, FUTURE2, DANGEROUS3, FUTURE3], 2*(sequen - 2)

    if symbol == PLAYER and doesnt_exist_on_list([new_r, new_c], crucial_lists[i]):
            print(f"      symbol = {symbol}, seq = {sequen}, go into cr[{i}] for {new_r},{new_c}")
            crucial_lists[i].append([new_r, new_c])

    if symbol == COM and doesnt_exist_on_list([new_r, new_c], crucial_lists[i + 1]):
        print(f"      symbol = {symbol}, seq = {sequen}, go into cr[{i+1}] for {new_r},{new_c}")
        crucial_lists[i + 1].append([new_r, new_c])

    for i in range(0,2): #i = 0,1
        if not doesnt_exist_on_list([new_r, new_c], crucial_lists[i]) and not doesnt_exist_on_list([new_r, new_c], crucial_lists[i + 2]):
            crucial_lists[i].remove([new_r, new_c])


def diagonal(BOARD, sequen, symbol, slist, direction):
    if direction == "on a left diagonal":
        c_start, c_end, step = sequen - 1, COLUMNS, -1
    else:
        c_start, c_end, step = 0, COLUMNS - sequen + 1, 1

    for i in range(ROWS - sequen + 1):
        for j in range(c_start, c_end):
            if BOARD[i][j] == symbol:
                counter = 1
                while counter < sequen:
                    if BOARD[i][j] != BOARD[i + counter][j + counter * step]:
                        break
                    else:
                        counter = counter + 1
                if counter == sequen:
                    slist.append([direction, i, j])
    return slist


def straight(BOARD, sequen, symbol, slist, direction):
    if direction == "horizontally":
        outer, inter, r, c = ROWS, COLUMNS, 0, 1
    else:
        outer, inter, r, c = COLUMNS, ROWS, 1, 0

    for ii in range(outer):
        for jj in range(inter - sequen + 1):
            counter = 0
            if direction == "horizontally":
                i, j = ii, jj
            else:
                i, j = jj, ii
            if BOARD[i][j] == symbol:
                counter = 1
                while counter < sequen:
                    if BOARD[i][j] == BOARD[i + counter * r][j + counter * c]:
                        counter = counter + 1
                    else:
                        break
            if counter >= sequen :
                slist.append([direction, c*ii + r*jj, r*ii + c*jj])
    # counter also working as a flag (if counter!=sequen then NOT found)
    return slist

def check_sequency(BOARD, sequen, symbol):
    # 4 in sequence for the win
    # BOARD[top_r][top_c] 's value (symbol) indicates player/computer
    directions = ["horizontally", "on a left diagonal", "vertically", "on a right diagonal"]
    slist = []
    for i in range(0, 3, 2): #in range = [0,2]
        slist = straight(BOARD, sequen, symbol, slist, directions[i]) # check horizontally and vertically #0,2
        slist = diagonal(BOARD, sequen, symbol, slist, directions[i+1]) # check on diagonals #1,3

    return slist

def random_move(BOARD, symbol):
    played_yet = False
    while not played_yet:
        import random
        c = random.randint(0, COLUMNS - 1)
        for r in range(ROWS - 1, -1, -1):
            if BOARD[r][c] == "|":
                BOARD[r][c], played_yet = symbol, True
                break
    return r,c

def one_to_two(BOARD, possible):
    played_yet, r, c = False, -1, -1
    global COM_MOVES
    for move in COM_MOVES:
        r = ROWS - 1
        if move[0] != ROWS - 1: r = move[0] + 1

        if move[1] >= 1:  # left of symbol
            if BOARD[move[0]][move[1] - 1] == "|" and BOARD[r][move[1] - 1] != "|":
                played_yet, r, c = True, move[0], move[1] - 1
                if played_yet and doesnt_exist_on_list([r,c], possible):
                    possible.append([r,c])
        elif move[1] <= COLUMNS - 2:  # right of symbol
            if BOARD[move[0]][move[1] + 1] == "|" and BOARD[r][move[1] + 1] != "|":
                played_yet, r, c = True, move[0], move[1] + 1
                if played_yet and doesnt_exist_on_list([r,c], possible):
                    possible.append([r,c])
        elif move[0] >= 1:  # over the symbol
            played_yet, r, c = True, move[0] - 1, move[1]
            if played_yet and doesnt_exist_on_list([r, c], possible):
                possible.append([r, c])

    if len(possible) > 0: played_yet = True
    return played_yet, r, c, possible


def horizontal_set_up(lor, BOARD, top_r, top_c, sequen, next_to):
    place_bellow_filled, makes_a_sequen, new_r = True, False, top_r
    plus, max_c, extra_cond = 0, 1, True
    if next_to == "between":
        plus = 1
        if lor=="left of sequence": max_c = sequen - 1

    if lor=="left of sequence": #"neighbor" variable is useless for next_to == "consiquently"
        fits_size = top_c >= max_c
        new_c, neighbor = top_c - 1, -2
    else:
        fits_size = top_c <= COLUMNS - (sequen + 1)
        new_c, neighbor = top_c + sequen - plus, sequen

    if fits_size:
        if next_to == "between":
            extra_cond = BOARD[new_r][top_c + neighbor] == BOARD[new_r][top_c]
        makes_a_sequen = BOARD[new_r][new_c] == "|" and extra_cond
        if new_r != ROWS - 1:
            place_bellow_filled = (BOARD[new_r + 1][new_c] != "|")

    return fits_size, makes_a_sequen, place_bellow_filled, new_r, new_c


def try_horizontal_move(lor_of_sequence, BOARD, top_r, top_c, sequen, next_to):
    played_yet = False
    fits_size, makes_a_sequen, place_bellow_filled, new_r, new_c = horizontal_set_up(lor_of_sequence, BOARD, top_r, top_c, sequen, next_to)

    if fits_size:
        if makes_a_sequen:
            if place_bellow_filled:
                played_yet = True
                if new_r == ROWS - 1:
                    mark_crusial_positions(new_r, new_c, sequen, BOARD[top_r][top_c])
            else:
                mark_crusial_positions(new_r, new_c, sequen, BOARD[top_r][top_c])

    return played_yet, new_r, new_c

def diagonal_set_up(aob, direction, BOARD, top_r, top_c, sequen, next_to):
    place_bellow_filled, makes_a_sequen, fits_size, new_r, new_c = True, False, False, top_r, -1

    extra_cond, plus = True, 0
    if next_to == "between":
        extra_cond, plus = (sequen > 2) , 1

    if aob == "above sequence" and extra_cond:
        if direction == "on a left diagonal":
            fits_size = top_r >= 1 + plus and top_c <= COLUMNS - (2 + plus)
            new_r, new_c = top_r - 1, top_c + 1
        else:
            fits_size = top_r >= 1 and top_c >= 1
            new_r, new_c = top_r - 1, top_c - 1
    elif aob == "bellow sequence":  # above_or_bellow_sequence == "bellow sequence"
        if direction == "on a left diagonal":
            fits_size = top_r <= ROWS - (sequen + 1) and top_c >= sequen
            new_r, new_c = top_r + sequen - plus, top_c - sequen + plus
        else:
            fits_size = top_r <= ROWS - (sequen + 1) and top_c <= COLUMNS - (sequen + 1)
            new_r, new_c = top_r + sequen - plus, top_c + sequen - plus

    if fits_size:
        if next_to == "between":
            sign_r, sign_c = 1, 1
            if aob == "above sequence": sign_r = -1
            if direction == "on a right diagonal": sign_c = -1
            extra_cond = BOARD[new_r+sign_r][new_c+sign_c]==BOARD[top_r][top_c]
        makes_a_sequen = BOARD[new_r][new_c] == "|" and extra_cond
        if new_r != ROWS - 1:
            place_bellow_filled = (BOARD[new_r + 1][new_c] != "|")

    return fits_size, place_bellow_filled, makes_a_sequen, new_r, new_c


def try_diagonal_move(aob, direction, BOARD, top_r, top_c, sequen, next_to):
    played_yet = False
    fits_size, place_bellow_filled, makes_a_seq, new_r, new_c = diagonal_set_up(aob, direction, BOARD, top_r, top_c, sequen, next_to)
    if fits_size:
        if makes_a_seq:
            if place_bellow_filled:
                played_yet = True
            else:
                mark_crusial_positions(new_r, new_c, sequen, BOARD[top_r][top_c])

    return played_yet, new_r, new_c

def update_cant_win_moves(slist, sequen, win_at = 4):
    #slist[i][0] --> dir, slist[i][1] --> top_r, slist[i][2] --> top_c
    global CANT_WIN_MOVES
    for s in slist:
            if s[0] == "horizontally":
                if not (s[2] <= COLUMNS - win_at) and doesnt_exist_on_list([s[1], s[2] + 2], CANT_WIN_MOVES):
                    CANT_WIN_MOVES.append([s[1], s[2] + 2])
                    if sequen == 3 and doesnt_exist_on_list([s[1], s[2] + 3], CANT_WIN_MOVES):
                        CANT_WIN_MOVES.append([s[1], s[2] + 3])
            elif s[0] == "vertically":
                if not (s[1] >= win_at - sequen) and doesnt_exist_on_list([s[1] + 1, s[2]], CANT_WIN_MOVES):
                    CANT_WIN_MOVES.append([s[1] + 1, s[2]])
                    if sequen == 2 and doesnt_exist_on_list([s[1] + 2, s[2]], CANT_WIN_MOVES):
                        CANT_WIN_MOVES.append([s[1] + 2, s[2]])


def update_strategical(new_r, new_c, symbol):
    global DANGEROUS2TO4, FUTURE2TO4, BOARD
    STRATEGICAL = [DANGEROUS2TO4, FUTURE2TO4]
    #UPDATE strategical future moves
    j, sequen = 0, 2
    if symbol == COM: j = 1
    next_to = ["consequently", "between"]
    left_or_right, above_or_bellow = ["left", "right"], ["above", "bellow"]
    for lor in left_or_right:
        playable, r, c = try_horizontal_move(lor + " of sequence", BOARD, new_r, new_c, sequen, next_to[j])
        if r >= 0 and r <= ROWS - 1 and c >= 0 and c <= COLUMNS - 1:
            if BOARD[r][c] == "|" and doesnt_exist_on_list([r,c], STRATEGICAL[j]):
                STRATEGICAL[j].append([r, c])
        for aob in above_or_bellow:
            playable, r, c = try_diagonal_move(aob+" sequence", "on a " + lor + " diagonal", BOARD, new_r, new_c, sequen,
                                                next_to[j])
            if r >= 0 and r <= ROWS - 1 and c >= 0 and c <= COLUMNS - 1:
                if BOARD[r][c] == "|" and doesnt_exist_on_list([r,c], STRATEGICAL[j]):
                    STRATEGICAL[j].append([r, c])
    #REMOVE covered positions
    for j in range(len(STRATEGICAL)):
        for pos in STRATEGICAL[j]:
            if BOARD[pos[0]][pos[1]] != "|":
                STRATEGICAL[j].remove(pos)


def block_sequence_of(BOARD, sequen, s, next_to, possible):
    played_yet, r, c = False, -1, -1
    left_or_right, above_or_bellow = ["left", "right"] , ["above", "bellow"]

    for i in s:
        if i[0] == "vertically" and i[1] >= 1 and next_to == "consequently":
            if BOARD[i[1] - 1][i[2]] == "|":
                played_yet, r, c = True, i[1] - 1, i[2]
                if played_yet and doesnt_exist_on_list([r,c], possible):
                    possible.append([r,c])
                    mark_crusial_positions(r, c, sequen, BOARD[i[1]][i[2]])
        elif i[0] == "horizontally":
            for lor in left_or_right:
                played_yet, r, c = try_horizontal_move(lor + " of sequence", BOARD, i[1], i[2], sequen, next_to)
                #if (played_yet and doesnt_exist_on_list([r, c], possible)):
                if played_yet and doesnt_exist_on_list([r, c], possible):
                    possible.append([r, c])
        else:  # diagonal move
            for lor in left_or_right:
                if i[0] == "on a " + lor + " diagonal":
                    for aob in above_or_bellow:
                        played_yet, r, c = try_diagonal_move(aob + " sequence", "on a " + lor + " diagonal", BOARD, i[1],
                                                       i[2], sequen, next_to)
                        if played_yet and doesnt_exist_on_list([r, c], possible):
                            possible.append([r,c])
        #keep tracing the whole list to store all possible moves
    print("--> pos = ", possible)

    return played_yet, r, c, possible

def complete_a_sequence(BOARD, played_yet, possible, sequen, symbol):
    r, c, list1, list2 = -1, -1, [], []
    if not played_yet: # check if that {symbol} appears {sequen} times in a sequence and computer can block it
        list1 = check_sequency(BOARD, sequen, symbol)
        played_yet, r, c, possible = block_sequence_of(BOARD, sequen, list1, "consequently", possible)

    #if not played_yet: #{sequen-1} + 1 or 1+{sequen-1} moves in {symbol} next to each other
        list2 = check_sequency(BOARD, sequen - 1, symbol) #find 2 {symbol} next to each other
        played_yet, r, c, possible = block_sequence_of(BOARD, sequen, list2, "between", possible)

    if len(possible)>0:
        played_yet = True
        print(f"played on seq of {sequen} over ({symbol})")

    return played_yet, r, c, possible, list1, list2

def update_crusial_positions(new_r, new_c):
    new_position_covered = [new_r, new_c]
    global FUTURE3, FUTURE2, DANGEROUS3, DANGEROUS2, UNPROTECTED_COM, UNPROTECTED_PL
    crucial_lists = [FUTURE3, FUTURE2, DANGEROUS3, DANGEROUS2, UNPROTECTED_COM, UNPROTECTED_PL]

    for num, cord in enumerate(crucial_lists):
        if cord == new_position_covered:
            crucial_lists[num].remove(new_position_covered)
        if BOARD[cord[0]][cord[1]] != "|" and not doesnt_exist_on_list(cord, crusial_lists[num]):
                crucial_lists[num].remove(new_position_covered)


def remove_dangerous_options(possible, dang_list, pl_list3):
    safe = possible.copy()
    print("VIRG safe = ", safe)
    global DANGEROUS2TO4, FUTURE2TO4, DANGEROUS3
    STRATEGICAL = [DANGEROUS2TO4, FUTURE2TO4]
    for alist in STRATEGICAL:
        for cord in alist:
            if not doesnt_exist_on_list(cord, possible) and not doesnt_exist_on_list(cord, alist):
                if doesnt_exist_on_list(cord, safe):
                    safe.append(cord)
    print("BEF safe: ", safe)
    for dang in dang_list:
        for el in safe:
            print(f" {el} vs {dang} --> {el[1]} == {dang[1]} and {dang[0] + 2} > {el[0]} --> {el[1] == dang[1] and dang[0] + 2 > el[0]}")
            if el[1] == dang[1] and dang[0] + 2 > el[0] and doesnt_exist_on_list(el, DANGEROUS3):
                #if not (el == dang and BOARD[el[0]][el[1]] == COM):
                    safe.remove(el)
    print("AFTER rem, safe: ", safe)
    return safe

def find_max_in_list(alist):
    if len(alist) == 0:
        return -1
    max_value, max_pos = alist[0], 0
    for i in range(len(alist)):
        if alist[i] > max_value:
            max_value, max_pos = alist[i], i
    return max_value, max_pos

def seq_2_unprotected(BOARD, sequently2, UNPROTECTED, DANGEROUS2, FUTURE2):
    print(sequently2)
    for s in sequently2:
        valid, cord = False, []
        if s[0] == "horizontally" and s[2] >= 1 and s[2] <= ROWS -3:
            if BOARD[s[1]][s[2] + 1] != "|": #1 + 1 --> 2 consequently
                cord, valid = [s[1], s[2]-1, s[1], s[2]+2], True
            else: #1 + void + 1 --> 2 with space in between
                cord, valid = [s[1], s[2] - 1, s[1], s[2] + 1], True
        elif s[1] >= 1 and s[1]<= ROWS - 3 and s[2]>=1 and s[2] <= ROWS - 2:
            if s[0] == "on a left diagonal" and s[2] >= 2:
                cord, valid = [s[1] - 1, s[2] + 1, s[1] + 2, s[2] - 2], True
            elif s[0] == "on a right diagonal" and s[2] <= ROWS - 3:
                cord, valid = [s[1] - 1, s[2] - 1, s[1] + 2, s[2] + 2], True
        if valid:
            for i in range(len(cord)):
                if BOARD[cord[0]][cord[1]] == "|" and BOARD[cord[2]][cord[3]] == "|":
                    for i in range(0, 3, 2):
                        if doesnt_exist_on_list([cord[i],cord[i + 1]], UNPROTECTED):
                            UNPROTECTED.append([cord[i], cord[i + 1]])
                            if BOARD[s[1]][s[2]] == PLAYER and doesnt_exist_on_list([cord[i],cord[i + 1]], DANGEROUS2):
                                DANGEROUS2.append([cord[i], cord[i + 1]])
                            elif BOARD[s[1]][s[2]] == COM and doesnt_exist_on_list([cord[i],cord[i + 1]], FUTURE2):
                                FUTURE2.append([cord[i], cord[i + 1]])

def pick_best_move(safe, possible, player_list3):
    global DANGEROUS2, DANGEROUS2TO4, FUTURE3, FUTURE2, FUTURE2TO4
    global UNPROTECTED_COM, UNPROTECTED_PL, CANT_WIN_MOVES
    points, index, keep_searching = [0] * len(safe), 0, True
    r, c = safe[0][0], safe[0][1]
    for cord in possible:
        if not doesnt_exist_on_list(cord,DANGEROUS3) and not doesnt_exist_on_list(cord,possible):
            r, c, keep_searching = cord[0], cord[1], False
    if keep_searching:
        for cord in safe:
            if not doesnt_exist_on_list(cord,UNPROTECTED_COM):
                points[index] = points[index] + 4
            if not doesnt_exist_on_list(cord,UNPROTECTED_PL):
                points[index] = points[index] + 4
            if not doesnt_exist_on_list(cord,FUTURE3):
                points[index] = points[index] + 3
            if not doesnt_exist_on_list(cord,DANGEROUS2):
                points[index] = points[index] + 2
            if not doesnt_exist_on_list(cord,FUTURE2):
                points[index] = points[index] + 1
            if not doesnt_exist_on_list(cord,FUTURE2TO4):
                points[index] = points[index] + 1
            if not doesnt_exist_on_list(cord,DANGEROUS2TO4):
                points[index] = points[index] + 1
            if not doesnt_exist_on_list(cord,CANT_WIN_MOVES):
                points[index] = points[index] - 1
            index = index + 1
        print("POINTS: ", points)
        max, index = find_max_in_list(points)
        print(f"max points: {max}, found on safe[{index}] = {safe[index]}")
        r, c = safe[index][0], safe[index][1]
    return r, c

def consider_options(BOARD, possible, player_list3):
    played_yet, r, c, count, pl_list3 = False, -1, -1, 0, []
    global DANGEROUS3, DANGEROUS2, FUTURE3, FUTURE2, DANGEROUS2TO4, FUTURE2TO4, CANT_WIN_MOVES
    if len(player_list3) <= 1:
        safe = possible.copy()
    else:
        safe = remove_dangerous_options(possible, DANGEROUS3, pl_list3)
    print("POSSIBLE : ", possible)
    print("DANGEROUS3: ", DANGEROUS3)
    print("DANGEROUS2: ", DANGEROUS2)
    print("FUTURE3: ", FUTURE3)
    print("FUTURE2: ", FUTURE2)
    print("DANGEROUS2TO4: ", DANGEROUS2TO4)
    print("FUTURE2TO4: ", FUTURE2TO4)
    print("UNPROTECTED_PL = ", UNPROTECTED_PL)
    print("UNPROTECTED_COM = ", UNPROTECTED_COM)
    print("CANT_WIN_MOVES: ", CANT_WIN_MOVES)
    print("Safe: ", safe)
    if len(safe) > 0:
        r, c = pick_best_move(safe, possible, player_list3)
        played_yet = True
    return played_yet, r, c, safe

def very_competitive():
    global BOARD, UNPROTECTED_PL, UNPROTECTED_COM, DANGEROUS2, FUTURE2
    played_yet, useless_info, possible, safe, pl_list3 = False, False, [], [], []

    # check if computer can win (has a sequence of 3 or 2+1 or 1+2 that can turn into 4)
    played_yet, r, c, possible, com_list3, com_list2 = complete_a_sequence(BOARD, played_yet, possible, 3, COM)
    print("poss for 3 com : ", possible)
    update_cant_win_moves(com_list3, 3)
    update_cant_win_moves(com_list2, 2)
    player_list3 = pl_list3.copy()
    for pos, el in enumerate(pl_list3):
        player_list3[pos][0] = pl_list3[pos][1]
        player_list3[pos][1] = pl_list3[pos][2]
    if len(possible) > 0 :
        #played_yet, r, c = True, possible[0][0], possible[0][1]
        played_yet, r, c, safe = consider_options(BOARD, possible, player_list3)

    if not played_yet: # check if player has 3 in a sequence and computer can block it
        played_yet, r, c, possible, pl_list3, pl_list2 = complete_a_sequence(BOARD, played_yet, possible, 3, PLAYER)
        print("poss for 3 pl : ", possible)
        update_cant_win_moves(pl_list3, 3)
        update_cant_win_moves(pl_list2, 2)
        #if found at least one sequence of 3 on PLAYER, obviously, block it
        #BUT, after you do and the game - hopefully - will go on, you also need to make same "notes" of some positions
        useless_info, r, c, possible, com_list2, com_list1 = complete_a_sequence(BOARD, useless_info, possible, 2, COM)
        seq_2_unprotected(BOARD, com_list2, UNPROTECTED_COM, DANGEROUS2, FUTURE2)
        seq_2_unprotected(BOARD, pl_list2, UNPROTECTED_PL, DANGEROUS2, FUTURE2)
        print("...merged with poss for 2 com : ", possible)
        if len(possible) > 0:
            #played_yet, r, c = True, possible[0][0], possible[0][1]
            played_yet, r, c, safe = consider_options(BOARD, possible, player_list3)

    if not played_yet:
        played_yet, r, c, possible, pl_list2, pl_list1 = complete_a_sequence(BOARD, played_yet, possible, 2, PLAYER)
        print("poss for 2 pl : ", possible)
        #before taking the final decision, find COM sequence of 2, to also promote its interests
        if len(possible) > 0:
            played_yet, r, c, safe = consider_options(BOARD, possible, player_list3)

    if not played_yet: #1+1 symbols next to each other
        dir = ["horizontally", "on a left diagonal", "on a right diagonal"]
        global PL_MOVES
        for d in dir:
            pl_list1 = [[d, pl[0], pl[1]] for pl in PL_MOVES]
            #print(pl_list1)
            played_yet, r, c, possible = block_sequence_of(BOARD, 2, pl_list1, "between", possible)
            if len(possible) > 0:
                played_yet, r, c, safe = consider_options(BOARD, possible, player_list3)
                break

        print("poss for 1+1 pl : ", possible)
        if played_yet:
            print("played on seq 2 between (PL)")

    if not played_yet: # check if computer can turn a sequence of 2 into 3,
        com_list2 = check_sequency(BOARD, 2, COM)
        played_yet,r,c, possible = block_sequence_of(BOARD, 2, com_list2, "consequently", possible)
        if len(possible) > 0:
            played_yet, r, c, safe = consider_options(BOARD, possible, player_list3)

        print("poss for 2 com : ", possible)
        if played_yet:
            print("played on seq 2 conseq (COM)")

    if not played_yet: #2+1 or 1+2 symbols next to each other
        dir = ["horizontally", "on a left diagonal", "on a right diagonal"]
        global COM_MOVES
        for d in dir:
            com_list1 = [[d, pl[0], pl[1]] for pl in COM_MOVES]
            #print(com_list1)
            played_yet, r, c, possible = block_sequence_of(BOARD, 2, com_list1, "between", possible)
            if len(possible) > 0:
                played_yet, r, c, safe = consider_options(BOARD, possible, player_list3)
                break

        print(possible)
        if played_yet:
            print("played on seq 2 between (COM)")

    if not played_yet: # or a sequence of 1 to 2
        played_yet, r, c, possible = one_to_two(BOARD, possible)
        if len(possible) > 0:
            played_yet, r, c, safe = consider_options(BOARD, possible, player_list3)

        if played_yet:
            print("played on 1-to-2 (COM)")

    if not played_yet:
        trials, good_choice = 10, True
        for i in range(trials):
            r,c = random_move(BOARD, COM)
            for dang in DANGEROUS3:
                if c == dang[1] and dang[0] + 2 > r:
                    good_choice = False
                    break
            if good_choice: break
        print("random")

    BOARD[r][c] = COM
    return r, c


def competitive():
    played_yet, possible = False, []

    # check if computer can win (has a sequence of 3 or 2+1 or 1+2 that can turn into 4)
    played_yet, r, c, possible, com_list3, com_list2 = complete_a_sequence(BOARD, played_yet, possible, 3, COM)
    if played_yet: r,c = possible[0][0], possible[0][1]

    if not played_yet: # check if player has 3 in a sequence and computer can block it
        played_yet, r, c, possible, pl_list3, pl_list2 = complete_a_sequence(BOARD, played_yet, possible, 3, PLAYER)
        if played_yet: r, c = possible[0][0], possible[0][1]

    if not played_yet:
        played_yet, r, c, possible, pl_list2, pl_list1 = complete_a_sequence(BOARD, played_yet, possible, 2, PLAYER)
        if played_yet: r,c = possible[0][0], possible[0][1]

    if not played_yet:
        played_yet, r, c, possible, com_list2, com_list1 = complete_a_sequence(BOARD, played_yet, possible, 2, COM)
        if played_yet: r, c = possible[0][0], possible[0][1]

    if not played_yet: #1+1 symbols next to each other
        dir = ["horizontally", "on a left diagonal", "on a right diagonal"]
        global PL_MOVES
        for d in dir:
            pl_list1 = [[d, pl[0], pl[1]] for pl in PL_MOVES]
            played_yet, r, c, possible = block_sequence_of(BOARD, 2, pl_list1, "between", possible)
            if played_yet:
                r, c = possible[0][0], possible[0][1]
                break

    if not played_yet: # check if computer can turn a sequence of 2 into 3,
        com_list2 = check_sequency(BOARD, 2, COM)
        played_yet,r,c, possible = block_sequence_of(BOARD, 2, com_list2, "consequently", possible)
        if played_yet: r, c = possible[0][0], possible[0][1]

    if not played_yet: #2+1 or 1+2 symbols next to each other
        dir = ["horizontally", "on a left diagonal", "on a right diagonal"]
        global COM_MOVES
        for d in dir:
            com_list1 = [[d, pl[0], pl[1]] for pl in COM_MOVES]
            played_yet, r, c, possible = block_sequence_of(BOARD, 2, com_list1, "between", possible)
            if played_yet:
                r, c = possible[0][0], possible[0][1]
                break

    if not played_yet: # or a sequence of 1 to 2
        played_yet, r, c, possible = one_to_two(BOARD, possible)
        if played_yet:
            r, c = possible[0][0], possible[0][1]

    if not played_yet:
        r, c = random_move(BOARD, COM)

    BOARD[r][c] = COM
    return r, c

def easy(BOARD, COM):
    r,c = random_move(BOARD, COM)
    return r, c

def make_a_move(symbol, BOARD):
    global MODE
    if symbol == PLAYER:
        while True:
            c = input(" *YOUR TURN*\n    Insert column: ");
            valid_int = True
            try:
                c = int(c)
            except:
                print("Non valid move. Insert an INTEGER. Try again\n");
                valid_int = False
            if valid_int:
                if c >= 0 and c < COLUMNS:
                    for r in range(ROWS - 1, -1, -1):
                        if BOARD[r][c] == "|":
                            break
                    if r == 0 and BOARD[r][c] !="|":
                        print("Non valid move. COLUMN FULL. Insert again\n")
                    else:
                        break
                else:
                    print("Non valid move. Integer OUT OF BOARD LIMITS. Try again\n")
        BOARD[r][c] = symbol
        global PL_MOVES
        PL_MOVES.append([r,c])
    else:  # computer playing
        global MODE
        if MODE == "Easy":
            r,c = easy(BOARD, COM)
        elif MODE == "Competitive":
            r, c = competitive()
        else:
            r, c = very_competitive()
        global COM_MOVES
        COM_MOVES.append([r, c])
    if MODE == 3:
        update_crusial_positions(r, c)
        update_strategical(r, c, BOARD[r][c])


def game_intro():
    print("\n\n         C  O  N  N  E  C  T     F  O  U  R\n")
    print("Score 4 in a sequence (horizontally, vertically, diagonally)")
    print("...win, if you can\n\n")


def main():
    game_intro()
    global MODE
    MODE = set_difficulty_mode()
    #clear_terminal()
    quadruple, round = [], 0
    for round in range(ROWS * COLUMNS // 2):
        game_intro()
        print_board(BOARD)
        make_a_move(PLAYER, BOARD)
        quadruple = check_sequency(BOARD, 4, PLAYER)
        if len(quadruple) > 0: break
        make_a_move(COM, BOARD)
        quadruple = check_sequency(BOARD, 4, COM)
        #clear_terminal()
        if len(quadruple) > 0: break

    clear_terminal()
    game_intro()
    print_board(BOARD)
    if round == ROWS * COLUMNS // 2 - 1:
        print("Board full, no winner, you both lost")
    else:
        print_winner(BOARD, quadruple[0][1], quadruple[0][2], quadruple[0][0])


main()