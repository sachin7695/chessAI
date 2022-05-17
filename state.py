from model.player import Player
from model.pawn import SoldierPawn, Knight, Pawn
from model.rune import Rune
from copy import deepcopy
from pprint import pprint
import random
from IPython.display import display, HTML
import pandas as pd


class State:
    def __init__(self):
        self.boardsize = 8
        self.white_pawn
        self.black_pawn_list = []
        self.white_knight = None
        self.black_knight = None
        self.rune_list = []
        self.turn = 0
        self.player_list = []
        self.board = [[None for i in range(self.board_size)] for j in range(self.board_size)] # board to show the position of our pawns
        self.PAWN_HP_DEFAULT = 5
        self.PAWN_ATK_DEFAULT = 1
        self.PAWN_STEP_DEFAULT = 1
        self.KNIGHT_HP_DEFAULT = 15
        self.KNIGHT_ATK_DEFAULT = 3
    def is_terminal(self):
        if self.white_knight.dead or self.black_knight.dead:
            return True
        boolean_white = True
        boolean_black = True
        for pawnw, pawnb in zip(self.white_paawn_list, self.black_pawn_list):
            if not pawnw.dead:
                boolean_white = False
            if not pawnb.dead:
                boolean_black = False
        return boolean_white or boolean_black


    def total_eval(self, player_color):
            
        (player_knight, enemy_knight) = (self.white_knight, self.black_knight) if player_color == 0 else (self.black_knight, self.white_knight)
        (current_player_pawn_list, enemy_pawn_list) = (self.white_pawn_list, self.black_pawn_list) if player_color == 0 else (self.black_pawn_list, self.white_pawn_list)

        if self.is_terminal():
            if player_knight.dead:
                return -120
            elif enemy_knight.dead:
                return 120
            else:
                util_value = 0
                for player_pawn, enemy_pawn in zip(current_player_pawn_list,enemy_pawn_list):
                    util_value += (int(enemy_pawn.dead) - int(player_pawn.dead))
                if util_value < 0:
                    util_value = -120
                else:
                    util_value = 120
                return util_value


    def sparse_eval(self, player_color):
        (player_knight, enemy_knight) = (self.white_knight, self.black_knight) if player_color == 0 else (self.black_knight, self.white_knight)
        (current_player_pawn_list, enemy_pawn_list) = (self.white_pawn_list, self.black_pawn_list) if player_color == 0 else (self.black_pawn_list, self.white_pawn_list)

        if self.is_terminal():
            if player_knight.dead:
                return -1
            elif enemy_knight.dead:
                return 1
            else:
                util_value = 0
                for player_pawn, enemy_pawn in zip(current_player_pawn_list,enemy_pawn_list):
                    util_value += (int(enemy_pawn.dead) - int(player_pawn.dead))
                if util_value < 0:
                    util_value = -1
                else:
                    util_value = 1
                return util_value

        return 0

    def initial_state(self):
        self.player_list.append(Player(0))
        self.player_list.append(Player(1))

        self.white_knight = Knight(self.KNIGHT_HP_DEFAULT, self.KNIGHT_ATK_DEFAULT,2,7, self.player_list[0])
        self.board[2][7] = self.white_knight
        self.black_knight = Knight(self.KNIGHT_HP_DEFAULT, self.KNIGHT_ATK_DEFAULT,2,0, self.player_list[1])

        self.white_pawn_list.append(SoldierPawn(0,self.PAWN_HP_DEFAULT, self.PAWN_ATK_DEFAULT,4,7,False,self.player_list[0],self.PAWN_STEP_DEFAULT))
        self.board[4][7] = self.white_pawn_list[0]
        self.black_pawn_list.append(SoldierPawn(0,self.PAWN_HP_DEFAULT,self.PAWN_ATK_DEFAULT,3,1,False,self.player_list[1],self.PAWN_STEP_DEFAULT))
        self.board[3][1] = self.black_pawn_list[0]


    def refresh_board(self):
        self.board = [[None for i in range(self.board_size)] for j in range(self.board_size)]
        self.board[2][7] = self.white_knight
        self.board[2][0] = self.black_knight
        for pawn in self.white_pawn_list:
            if not pawn.dead:
                self.board[pawn.y][pawn.x] = pawn
        for pawn in self.black_pawn_list:
            if not pawn.dead:
                self.board[pawn.y][pawn.x] = pawn


    def print_board(self):
        df_pr = [[None for i in range(self.board_size)] for j in range(self.board_size)]
        pd.options.display.max_columns = 10
        pd.options.display.max_rows = 1000
        pd.options.display.width = 1000

        for i in range(self.board_size):
            for j in range(self.board_size):
                need_to_pass = False
                if not need_to_pass:
                    if self.board[j][i] is not None and self.board[j][i].dead ==False:
                        df_pr[i][j] = self.board[j][i].__repr__()
                    else:
                        df_pr[i][j] = "Nones"
        display(pd.DataFrame(df_pr))


    def get_possible_action_player(self):
        possible_action = []
                
        player_possible_action = {}
        player = self.player_list[self.turn%2]
        # print(player.__dict__)
        player_string = "White Player" if player.color == 0 else "Black Player"
        player_possible_action["actor"] = player_string
        ref_pawn = self.white_pawn_list if player.color == 0 else self.black_pawn_list
        # print(ref_pawn[0].__dict__)
        dict_action = {}
        p_moves = player.possible_move(ref_pawn)
        for move in p_moves:
            key_name = ""
            action_type = move[0]
            pawn_index = move[1]
            if action_type == 'promote':
                key_name += 'p'
            else:
                key_name += 'a'

            action_params = {}
            targetted_pawn = ref_pawn[pawn_index]
            key_name += "*" + str(targetted_pawn.y) + "," +  str(targetted_pawn.x)

            if not targetted_pawn.dead:
                action_params['pawn_hp'] = targetted_pawn.hp
                action_params['pawn_atk'] = targetted_pawn.atk
                action_params['pawn_step'] = targetted_pawn.step
                action_params['pawn_x'] = targetted_pawn.x
                action_params['pawn_y'] = targetted_pawn.y
                action_params['action'] = action_type
                action_params['pawn_index'] = pawn_index
                action_params['player_index'] = player.color
                if action_type == 'promote':
                    promoted_choice = move[2]
                    action_params['promoted_choice'] = promoted_choice
                    key_name += "*" + promoted_choice[0]

                dict_action[key_name] = action_params
        player_possible_action["action"] = dict_action
        possible_action.append(deepcopy(player_possible_action))
        return possible_action

    def get_possible_action_pawn(self):
        possible_action = []
        pawn_possible_action = {}
        player = self.player_list[self.turn%2]
        ref_pawn = self.white_pawn_list if player.color == 0 else self.black_pawn_list
                # print(player)
        # print(ref_pawn[0].__dict__)
        for pawn in ref_pawn:
            if not pawn.dead:
                dict_action = {}
                possible_action_iter = pawn.possible_move()['possible']
                key_name_move_start = 'mp*'
                key_name_atk_start = 'mp*'
                counter_loop_moves = 0
                x_start = pawn.x
                y_start = pawn.y
                step = pawn.step
                for possible_moves in possible_action_iter:
                    action_params = {}
                    x_end = possible_moves[0]
                    y_end = possible_moves[1]
                    dir_index = possible_moves[2]
                    counter_loop_moves += 1
                    if self._is_valid_moves(x_end, y_end):

                        if self._is_occupied_by_enemy(x_end, y_end): #attack
                            pawn_target = self.board[x_end][y_end]

                            action_params = {
                                'player_index' : player.color,
                                'pawn_x' : x_start,
                                'actor' : pawn.__class__.__name__ + ' ' + ("White" if player.color == 0 else "Black") + " No. " + str(pawn.pawn_index),
                                'pawn_y' : y_start,
                                'pawn_hp' : pawn.hp,
                                'pawn_atk' : pawn.atk,
                                'pawn_step' : pawn.step,
                                'x_end' : x_end,
                                'y_end' : y_end,
                                'dir_index' : dir_index,
                                'step' : step,
                                'isKnight' : pawn_target.__class__.__name__ == "Knight",
                                'enemy_pawn_index' : pawn_target.pawn_index,
                                'enemy_hp' : pawn_target.hp,
                                'enemy_step' : pawn_target.step,
                                'pawn_index' : pawn.pawn_index,
                                'action' : "attack",
                                'enemy_hp_after_attack' : pawn_target.hp - pawn.atk,
                                'enemy_name' : pawn_target.__class__.__name__ + ' ' + ("White" if pawn_target.player.color == 0 else "Black") + " No. " + str(pawn_target.pawn_index)
                            }
                            y_dir = y_end - y_start
                            x_dir = x_end - x_start
                            key_name_atk = key_name_atk_start + str(y_start) + ',' + str(x_start) + "*"
                            key_name_atk += str(y_dir) + "," + str(x_dir)
                            dict_action[key_name_atk] = deepcopy(action_params)
                        elif not self._is_occupied_by_ally(x_end, y_end):
                            action_params = {
                                'player_index' : player.color,
                                'pawn_x' : x_start,
                                'actor' : pawn.__class__.__name__ + ' ' + ("White" if player.color == 0 else "Black") + " No. " + str(pawn.pawn_index),
                                'pawn_hp' : pawn.hp,
                                'pawn_atk' : pawn.atk,
                                'pawn_step' : pawn.step,
                                'pawn_y' : y_start,
                                'pawn_index' : pawn.pawn_index,
                                'x_end' : x_end,
                                'y_end' : y_end,
                                'dir_index' : dir_index,
                                'step' : step,
                                'action' : 'move'
                            }
                            y_dir = y_end - y_start
                            x_dir = x_end - x_start
                            key_name_move = key_name_move_start + str(y_start) + ',' + str(x_start) + "*"
                            key_name_move += str(y_dir) + "," + str(x_dir)
                            dict_action[key_name_move] = deepcopy(action_params)

                pawn_possible_action['actor'] = pawn.__class__.__name__ + ' ' + ("White" if player.color == 0 else "Black") + " No. " + str(pawn.pawn_index)
                pawn_possible_action['action'] = deepcopy(dict_action)
            possible_action.append(deepcopy(pawn_possible_action))
        return possible_action


        def get_dict_value_state(self):

            returned_dict = {}

            # Return all of white pawns
            white_pawn_list_dict = []
            for pawn in self.white_pawn_list:
                white_pawn_list_dict.append(pawn.__dict__)
            returned_dict['white_pawn_list'] = white_pawn_list_dict

            # Return all of black pawns
            black_pawn_list_dict = []
            for pawn in self.black_pawn_list:
                black_pawn_list_dict.append(pawn.__dict__)
            returned_dict['black_pawn_list'] = black_pawn_list_dict

            player_list_dict = []
            for player in self.player_list:
                player_list_dict.append(player.__dict__)
            returned_dict['player_list'] = player_list_dict

            rune_list_dict = []
            for rune in self.rune_list:
                rune_list_dict.append(rune.__dict__)
            returned_dict['rune_list'] = rune_list_dict

            returned_dict['white_knight'] = self.white_knight.__dict__
            returned_dict['black_knight'] = self.black_knight.__dict__

            return returned_dict