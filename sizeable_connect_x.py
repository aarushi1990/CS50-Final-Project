from game import Game


class SizeableConnectX(Game):
    def __init__(self, row_amt=6, col_amt=7, connect_amt=4, state_and_player=None):
        self.row_amt = row_amt
        self.column_amt = col_amt
        self.connect_amt = connect_amt
        super().__init__(state_and_player)
    
    def get_initial_state(self):
        # self.column_amt slots per row, self.row_amt rows
        # first inner list represents the bottom row from left to right
        # return an empty board
        return [[-1] * self.column_amt for _ in range(self.row_amt)]

    def get_state_hash(self):
        '''Return a unique string for the state and active player'''
        string_list = ["O", "X", " "]
        ans = ""
        for row in self.state:
            for val in row:
                ans += string_list[val]
        return ans

    def get_json_dict(self):
        # follows the same general idea as tic_tac_toe
        # the dictionary we will return
        ans = {}
        # iterate down from top to bottom by row
        index = 0
        for row in reversed(self.state):
            for val in row:
                # the key is the slot number, the value is the player in that slot
                ans[str(index)] = val
                index += 1
        ans["active_player"] = self.active_player
        winner = self.who_won()
        if winner is None:
            ans["winner"] = -2
        else:
            ans["winner"] = winner
        return ans

    def swap_players(self):
        '''Swap the players in a game.'''
        self.state = [[Game.get_other_player(val)
                       if val >= 0 else -1 for val in row]
                      for row in self.state]

    def get_copy(self):
        '''Return a copy of the object'''
        return SizeableConnectX(self.row_amt, self.column_amt, self.connect_amt, ([row[:] for row in self.state], self.active_player))

    def get_possible_moves(self):
        '''Return a list of the possible actions that can be taken by self.active_player in the self.state state
        Behavior is undefined when the game is complete
        '''
        # return which slots are open on the top
        return [i for i in range(self.column_amt) if self.state[-1][i] == -1]

    def make_move(self, action):
        '''Change the state of the game and update the active player based on the action'''
        # the action specifies the column
        # start on the bottom row to see if there's an open space, and then move up if not
        for row in self.state:
            if row[action] == -1:
                row[action] = self.active_player
                break

        self.active_player = Game.get_other_player(self.active_player)

    def who_won(self):
        '''Return 0 if player 0 won, 1 if player 1 won, -1 if there was a tie, and None if the game has not finished'''

        ans = -1  # default to tie
        if -1 in self.state[-1]:
            ans = None  # game is not complete yet

        # the player we're checking to see if they won
        cur_player = None
        # upgrade: there's duplicate code here
        # check rows (left to right)
        for row_index in range(self.row_amt):
            for start_col_index in range(self.column_amt - self.connect_amt + 1):
                # how many columns to shift over from the start_col_index
                for col_shift in range(self.connect_amt):
                    if col_shift == 0:
                        cur_player = self.state[row_index][start_col_index + col_shift]
                        if cur_player == -1:
                            # no player has moved here yet
                            break
                    if self.state[row_index][start_col_index + col_shift] != cur_player:
                        # not enough in the series
                        break
                    else:
                        # found the next one in the series
                        if col_shift == self.connect_amt - 1:
                            # found an entire match
                            return cur_player
        # check columns (bottom to top)
        for col_index in range(self.column_amt):
            for start_row_index in range(self.row_amt - self.connect_amt + 1):
                # how many rows to shift over from the start_row_index
                for row_shift in range(self.connect_amt):
                    if row_shift == 0:
                        cur_player = self.state[start_row_index + row_shift][col_index]
                        if cur_player == -1:
                            # no player has moved here yet
                            break
                    if self.state[start_row_index + row_shift][col_index] != cur_player:
                        # not enough in the series
                        break
                    else:
                        # found the next one in the series
                        if row_shift == self.connect_amt - 1:
                            # found an entire match
                            return cur_player

        # check top left diagonals
        # iterate up through the rows
        for row_index in range(self.connect_amt - 1, self.row_amt):
            for start_col_index in range(self.column_amt - self.connect_amt + 1):
                # how many columns to shift over from the start_col_index
                for shift in range(self.connect_amt):
                    if shift == 0:
                        cur_player = self.state[row_index - shift][start_col_index + shift]
                        if cur_player == -1:
                            # no player has moved here yet
                            break
                    if self.state[row_index - shift][start_col_index + shift] != cur_player:
                        # not enough in the series
                        break
                    else:
                        # found the next one in the series
                        if shift == self.connect_amt - 1:
                            # found an entire match
                            return cur_player

        # check top right diagonals
        # iterate up through the rows
        for row_index in range(self.row_amt - self.connect_amt + 1):
            for start_col_index in range(self.column_amt - self.connect_amt + 1):
                # how many columns to shift over from the start_col_index
                for shift in range(self.connect_amt):
                    if shift == 0:
                        cur_player = self.state[row_index + shift][start_col_index + shift]
                        if cur_player == -1:
                            # no player has moved here yet
                            break
                    if self.state[row_index + shift][start_col_index + shift] != cur_player:
                        # not enough in the series
                        break
                    else:
                        # found the next one in the series
                        if shift == self.connect_amt - 1:
                            # found an entire match
                            return cur_player
        return ans

    def __str__(self):
        '''Return a human-understandable string representing the game'''
        # iterate from top to bottom
        # print the rows separated by a newline
        # replacing -1s with dashes
        return "Player {}'s turn:\n{}".format(self.active_player,
                                              "\n".join([str(row).replace("-1", "-")
                                                         for row in reversed(self.state)]))
