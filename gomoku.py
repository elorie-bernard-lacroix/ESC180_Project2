"""
ESC194_Project 2
Gomoku

Last modified on November 7, 2022 by Elorie Bernard-Lacroix and Chaewon Lim
"""

#from Lab 6: return True iff coordinate y x is actually a square that exists on the board
def is_sq_in_board(board, y, x):
    return y < len(board) and x < len(board[0])

#also from Lab 6: returns True if the sequence is exactly length
def is_sequence_complete(board, col, y_start, x_start, length, d_y, d_x):
    if is_sq_in_board(board, y_start-d_y, x_start-d_x):
        if board[y_start-d_y][x_start-d_x] == col:
            return False
    if is_sq_in_board(board, y_start + length*d_y, x_start + length*d_x):
        if board[y_start + length*d_y][x_start + length*d_x] == col:
            return False
    
    for i in range(length):
        if not is_sq_in_board(board, y_start+i*d_y, x_start+i*d_x):
            return False
        if board[y_start+i*d_y][x_start+i*d_x] != col:
            return False
    return True



def is_empty(board):
    ''' This function returns True iff there are no stones on the board "board".'''

    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] != " ":
                return False
    return True    
    
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    '''
    This function analyses the sequence of length length that ends at location (y end, x end). 
    The function returns "OPEN" if the sequence is open, "SEMIOPEN" if the sequence if semi-open, 
    and "CLOSED" if the sequence is closed.
    
    Assume that the sequence is complete (i.e., you are not just given a subsequence) and valid, and
    contains stones of only one colour.
    '''
    if board[y_end + d_y][x_end + d_x] == " " and board[y_end - length*d_y][x_end - length*d_x] == " ":
        return "OPEN"
    else: # if the sequence is valid, only the opposite colour can bound the sequence
        if board[y_end + d_y][x_end + d_x] == " " or board[y_end - length*d_y][x_end - length*d_x] == " ":
            return "SEMIOPEN"
        else:
            return "CLOSED"
    
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    '''
    This function analyses the row (let’s call it R) of squares that starts at the location (y start,x start)
    and goes in the direction (d y,d x). Note that this use of the word row is different from “a row in
    a table”. Here the word row means a sequence of squares, which are adjacent either horizontally,
    or vertically, or diagonally. The function returns a tuple whose first element is the number of open
    sequences of colour col of length length in the row R, and whose second element is the number of
    semi-open sequences of colour col of length length in the row R.

    Assume that (y start,x start) is located on the edge of the board. Only complete sequences count.
    For example, column 1 in Fig. 1 is considered to contain one open row of length 3, and no other
    rows.

    Assume length is an integer greater or equal to 2.
    '''

    num_of_semi = 0
    num_of_open = 0
    cur_run = 0
    open_ends = 2 #either 2, 1, or 0 ends open, meaning open, semiopen, and closed respectively
    for i in range(len(board)):
        
        if not is_sq_in_board(board, y_start+i*d_y, x_start+i*d_x):
            continue #takes care of out of bounds errors, kinda hacky
        if board[y_start+i*d_y][x_start+i*d_x] == col:
            cur_run += 1  
        elif board[y_start+i*d_y][x_start+i*d_x] == " ":
            if cur_run == length and open_ends == 2:
                num_of_open += 1
            elif cur_run == length and open_ends == 1:
                num_of_semi += 1
            open_ends = 2
            cur_run = 0
        else: #meaning this is the opposite colour
            if cur_run == length and open_ends == 2:
                num_of_semi += 1
            open_ends = 1
            cur_run = 0
    return num_of_open, num_of_semi

    return open_seq_count, semi_open_seq_count
    
def detect_rows(board, col, length):
    '''
    This function analyses the board board. The function returns a tuple, whose first element is the
    number of open sequences of colour col of length lengthon the entire board, and whose second
    element is the number of semi-open sequences of colour col of length length on the entire board.
    Only complete sequences count. For example, Fig. 1 is considered to contain one open row of length
    3, and no other rows.

    Assume length is an integer greater or equal to 2.
    '''
    open_seq_count, semi_open_seq_count = 0, 0
    for i in range(len(board)):
        a, b = detect_row(board, col, i, 0, length, 0, 1) #not sure how to best unpack tuples and add
        open_seq_count += a
        semi_open_seq_count += b
        a, b = detect_row(board, col, i, 0, length, 1, 1) #not sure how to best unpack tuples and add
        open_seq_count += a
        semi_open_seq_count += b
        a, b = detect_row(board, col, i, 0, length, 1, -1) #not sure how to best unpack tuples and add
        open_seq_count += a
        semi_open_seq_count += b
        a, b = detect_row(board, col, 0, i, length, 1, 0) #not sure how to best unpack tuples and add
        open_seq_count += a
        semi_open_seq_count += b
    for i in range(1, len(board)):
        a, b = detect_row(board, col, 0, i, length, 1, 1) #not sure how to best unpack tuples and add
        open_seq_count += a
        semi_open_seq_count += b
        a, b = detect_row(board, col, len(board)-1, i, length, 1, -1) #not sure how to best unpack tuples and add
        open_seq_count += a
        semi_open_seq_count += b
    return open_seq_count, semi_open_seq_count
    
def search_max(board):
    '''
    This function uses the function score() (provided) to find the optimal move for black. It finds the
    location (y,x), such that (y,x) is empty and putting a black stone on (y,x) maximizes the score of
    the board as calculated by score(). The function returns a tuple (y, x) such that putting a black
    stone in coordinates (y, x) maximizes the potential score (if there are several such tuples, you can
    return any one of them). After the function returns, the contents of board must remain the same.
    '''

    maxScore, move_y, move_x = -100001, -1, -1 #initialize with impossible values (somewhat for debugging purpose)
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == " ":
                board[y][x] = "b" #temporarily place 'b' counter (assumes computer is black)
                if score(board) > maxScore:
                    maxScore = score(board)
                    move_y = y
                    move_x = x
                board[y][x] = " "
    return move_y, move_x
    
def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

def is_win(board):
    '''
    This function determines the current status of the game, and returns one of
    ["White won", "Black won", "Draw", "Continue playing"], depending on the current status
    on the board. The only situation where "Draw" is returned is when board is full.
    '''
    winner = ""
    full = True
    for y in range(len(board)):
        for x in range(len(board[0])): #not using dectect_row() because closed sequences are also wins
            if is_sequence_complete(board, 'b', y, x, 5, 1, 0) \
            or is_sequence_complete(board, 'b', y, x, 5, 0, 1) \
            or is_sequence_complete(board, 'b', y, x, 5, 1, 1) \
            or is_sequence_complete(board, 'b', y, x, 5, 1, -1):
                return "Black won"
            if is_sequence_complete(board, 'w', y, x, 5, 1, 0) \
            or is_sequence_complete(board, 'w', y, x, 5, 0, 1) \
            or is_sequence_complete(board, 'w', y, x, 5, 1, 1) \
            or is_sequence_complete(board, 'w', y, x, 5, 1, -1):
                return "White won"
            if board[y][x] == " ":
                full = False
    if full:
        return "Draw"
    return "Continue playing"            
    pass


def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board
                


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
        
    
    

        
    
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            
            
        
        
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
            
            
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #     
    
    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);
    
    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #        
    #        
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0

            
if __name__ == '__main__':
    easy_testset_for_main_functions()
    play_gomoku(8)
    