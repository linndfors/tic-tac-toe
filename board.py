'''
Here we create a board
'''
from btree import LinkedBST
from bstnode import BSTNode
import copy

class Board():
    '''
    board for the xo game
    '''
    def __init__(self) -> None:
        '''
        create a board
        '''
        self.matrix = [['', '', ''], ['', '', ''], ['', '', '']]
        # self.priority = []
        self.priority = self.find_priorities()
        # self.priority = self.priority if self.priority.__len__() <= 2 else self.priority[:2]
        self.moves = []
        self.winer = False
    def find_priorities(self):
        res = []
        for ind1 in range(3):
            for ind2 in range(3):
                if not self.matrix[ind1][ind2]:
                    res.append((ind1, ind2))
        res = res if res.__len__() <= 2 else res[:2]
        return res

    def create_matrix(self, board):
        self.matrix = board
        list_variants = self.find_priorities()
        self.priority = list_variants
        # for ind1 in range(3):
        #     for ind2 in range(3):
        #         if not self.matrix[ind1][ind2]:
        #             list_variants.append((ind1, ind2))
        # if len(list_variants) >= 2:
        #     self.priority = list_variants[:2]
        #     return
        # else:
        #     self.priority = list_variants

    def win(self, argument):
        '''
        check if somebody has won, if yes return True
        '''
        for row in self.matrix:
            if row[0] == row[1] == row[2] == argument:
                return True
        for ind, _ in enumerate(self.matrix):
                if self.matrix[0][ind] == self.matrix[1][ind] == self.matrix[2][ind] == argument:
                    return True
        if self.matrix[0][0] == self.matrix[1][1] == self.matrix[2][2] == argument:
            return True
        if self.matrix[2][0] == self.matrix[1][1] == self.matrix[0][2] == argument:
            return True

    def draw(self):
        '''
        if board is full, but nobody have won
        '''
        counter = 0
        for row in self.matrix:
            for elem in row:
                if elem != '':
                    counter += 1
        if self.winer == False and counter == 9:
            return True

    def get_status(self):
        '''
        get a game status
        '''
        if self.win('O'):
            self.winer = True
            return 'O'
        elif self.win('x'):
            self.winer = True
            return 'x'
        elif self.draw():
            return 'draw'
        else:
            return 'continue'

    def check_move(self, row, col):
        '''
        check if cell is empty, if no return IndexError
        '''
        if self.matrix[row][col]:
            raise IndexError

    @staticmethod
    def swap_symbol(symbol):
        if symbol == 'O':
            symbol = 'x'
        elif symbol == 'x':
            symbol = 'O'
        return symbol

    def make_move(self, position, turn):
        '''
        make a move, if it's valid
        '''
        row, col = position
        try:
            self.check_move(row, col)
            self.matrix[row][col] = turn
            self.moves.append((position, turn))
        except IndexError:
            print(f"{row, col} isn't empty")
            return True

    def __str__(self) -> str:
        res = ""
        for row in self.matrix:
            res += str(row) +"\n"
        return res[:-1]

    def make_computer_move(self):
        bin_tree1 = LinkedBST()
        bin_tree1.root = self.matrix
        bin_tree1.left = LinkedBST()
        bin_tree1.right = LinkedBST()
        new_board = copy.deepcopy(self.matrix)
        symbol = 'O'

        def main_logic(node, symbol, matrix, index, points):
            counter = 0
            for x in range(3):
                for y in range(3):
                    if not matrix[x][y]:
                        if counter == index:
                            new_matrix = copy.deepcopy(matrix)
                            
                            new_board = Board()
                            new_board.create_matrix(new_matrix)
                            new_board.make_move((x, y), symbol)
                            node.root = new_board.matrix
                            checking = Board()
                            checking.matrix = new_matrix
                            if checking.draw():
                                if checking.win('O'):
                                    points += 1
                                else:
                                    points -= 1
                            symbol = Board.swap_symbol(symbol)

                            node.left = LinkedBST()
                            node.right = LinkedBST()
                            points = main_logic(node.left, symbol, new_board.matrix, 0, points)
                            points = main_logic(node.right, symbol, new_board.matrix, 1, points)
                            len(bin_tree1)
                            return points
                        else:
                            counter += 1
            return points
                

        points_left = main_logic(bin_tree1.left, symbol, new_board, 0, points = 0)
        points_right = main_logic(bin_tree1.right, symbol, new_board, 1, points = 0)
        if self.draw():
            exit()
        if points_left < points_right:
            vars = self.find_priorities()
            good_move = vars[1]
            # self.priority.remove(good_move)
            self.make_move(good_move, 'O')
        else:
            vars = self.find_priorities()
            good_move = vars[0]
            self.make_move(good_move, 'O')
        # self.count_combination(bin_tree1.left)
        # self.count_combination(bin_tree1.right)

        # return bin_tree1

board = Board()
while not board.draw():
    while True:
        x_cord = int(input('x = '))
        y_cord = int(input('y = '))
        if not board.make_move((x_cord, y_cord), 'x'):
            break
    if board.get_status() == 'x':
        print('You win!')
        print(board)
        break
    board.make_computer_move()
    if board.get_status() == 'O':
        print('You lose!')
        print(board)
        break
    print(board)
