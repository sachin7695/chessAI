from model.pawn import SoldierPawn

class Player():
    def __init__(self, color):
        self.color = color

    def activate_pawn(self, pawn):
        pawn.status = True
        
    def possible_move(self, list_pawn):
        list_possible_moves = []
        for pawn in list_pawn:
            if pawn.status == True:
                list_possible_moves.append(pawn.possible_move())
        return list_possible_moves

    def __repr__(self):
        return self.color