class Pawn:
    def __init__(self, pawn_index, hp, atk, x, y,status, player, step):
        self.pawn_index = pawn_index
        self.hp = hp
        self.atk = atk
        self.x = x
        self.y = y
        self.status = status
        self.player = player
        self.step = step
        self.max_hp = hp
        self.dir = []
        self.dead = False
 

    def attack_enemy(self, enemy_pawn):
        enemy_pawn.hp -= self.atk
        if enemy_pawn.hp <= 0:
            enemy_pawn.hp = 0
            enemy_pawn.dead = True
            enemy_pawn.x = -2
            enemy_pawn.y = -2

     
    
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def possible_move(self, x, y):
        pass


    def __repr__(self):
        active = "a" if self.status ==1 else "i"
        return self.__class__.__name__[0:2] + str(self.player.color) + active + str(self.pawn_index) + 'A' + str(self.atk) + 'H' + str(self.hp) +  'S' + str(self.step)


class SoldierPawn(Pawn):
    def __init__(self, pawn_index, hp, atk, x, y, status, player, step):
        super().__init__(pawn_index, hp, atk, x, y, status, player, step)
        if player.color ==0:
            self.dir = [0, -1]
        else:
            self.dir = [0, 1]
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
    
    def possible_move(self):
        if self.status == 0:
            return {'possible' : []}
        possible_move_list = []
        possible_attack_list = []
        index_dir_counter = 0

        for i in range(self.step):
            if self.player.color == 0:
                possible_move_list.append((self.x,self.y-1-i, index_dir_counter)) # Move Up if White
                possible_attack_list.append((self.x,self.y-1-i))

            else: #Move bot if Black
                possible_move_list.append((self.x,self.y+1+i, index_dir_counter)) # Move Down if white
                possible_attack_list.append((self.x,self.y+1+i))
            index_dir_counter += 1
        return {'possible' : possible_move_list} 

class Knight(Pawn):
    def __init__(self, hp, atk, x, y, player):
        self.hp = hp
        self.atk = atk
        self.x = x
        self.y = y
        self.player = player
        self.step = 3
        self.status = True
        self.dir = [(1,0),(0,1),(0,-1),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]
        self.dead = False
        self.pawn_index = -1
        

    def attack_enemy(self, enemy_pawn):
        enemy_pawn.hp -= self.atk
        if enemy_pawn.hp <= 0:
            enemy_pawn.hp = 0
            enemy_pawn.dead = True
            enemy_pawn.x = -2
            enemy_pawn.y = -2

    
    def possible_move(self):
        possible_move_list = []
        direction_move = self.dir
        counter_dir_moves = 0
        for direction in direction_move:
            possible_move_list.append((self.x + direction[0],self.y + direction[1], counter_dir_moves))
            counter_dir_moves += 1
        return super()._possible_move_promoted_helper(self.x,self.y,direction_move)
    
