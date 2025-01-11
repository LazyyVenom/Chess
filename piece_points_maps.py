# Making point maps for pieces to follow in the board

pawn_points_map = [
        [0,10,0,10,20,0,0,0],
        [0,0,0,0,10,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
    ]

knight_points_map =[
        [0,1,1,2,2,1,1,0],
        [0,1,2,2,2,2,1,0],
        [1,2,3,3,3,3,2,1],
        [1,3,4,5,5,4,3,1],
        [1,3,4,5,5,4,3,1],
        [1,2,3,3,3,3,2,1],
        [0,1,2,2,2,2,1,0],
        [0,1,1,2,2,1,1,0],
    ]


bishop_points_map = [
        [0,1,1,1,1,1,1,0],
        [1,1,2,2,2,2,1,1],
        [1,1,2,2,2,2,1,1],
        [1,2,2,3,3,2,1,1],
        [1,1,4,3,3,4,1,1],
        [1,3,3,2,2,3,3,1],
        [1,3,0,0,0,0,0,1],
        [3,1,1,1,1,1,1,3],
    ]

rook_points_map = [
        [2,2,3,3,3,3,2,2],
        [2,4,4,4,4,4,4,2],
        [0,1,1,1,1,1,1,0],
        [0,1,1,1,1,1,1,0],
        [0,1,1,1,1,1,1,0],
        [0,1,1,1,1,1,1,0],
        [0,1,1,1,1,1,1,0],
        [1,1,2,3,3,2,1,1],
    ]

queen_points_map = [
        [0,1,1,1,1,1,1,0],
        [1,2,2,2,2,2,2,1],
        [1,2,2,3,3,2,2,1],
        [2,2,3,4,4,3,2,2],
        [2,3,3,4,4,3,3,2],
        [1,2,3,3,3,3,2,1],
        [1,2,2,2,2,2,2,1],
        [0,1,1,1,1,1,1,0],
    ]

king_points_map = [
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1],
        [2,2,1,0,0,1,1,1],
        [2,2,1,0,0,1,2,2],
        [4,3,1,0,0,1,3,4],
        [5,5,1,1,1,1,5,5],
    ]

pieces_points_map = {
    "p" : pawn_points_map,
    "n" : knight_points_map,
    "b" : bishop_points_map,
    "r" : rook_points_map,
    "q" : queen_points_map,
    "k" : king_points_map,
}