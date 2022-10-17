from turtle import screensize


levels = {
    1 : [
'XXXXXXXXXXXXXXXXXXXXXXXXX',
'X                X      X',
'X                X      X',
'XXXX             X      X',
'X                X      X',
'X        XX      X      X',
'X        X       X      X',
'X        X              X',
'X        X              X',
'X   P    X              X',
'XXXXXXXXXXXXXXXXXXXXXXXXX'
    ],
    2 : [
'                         ',
'                         ',
'                         ',
'                         ',
'                         ',
'     X             X     ',
'    X               X    ',
'    X      X        X    ',
'     X             X     ',
' XX         P         XX ',
'XXXXXXXXXXXXXXXXXXXXXXXXX'
    ]
}

level_tile_size = 48 # Definir tamanho de cada bloco em pixels

screen_width = 1200
screen_height = 600