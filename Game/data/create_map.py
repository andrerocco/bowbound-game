from daos.LevelDAO import LevelDAO
from utility.finder import find_file

level_DAO = LevelDAO('default-levels.json')
# level_DAO.remove_level_by_name('Fast arrows???')

teste = {
    'level_name': 'A lot of arrows!?!?',
    'arrows': ['standard', 'standard', 'piercing'],
    'tile_map': ['XXXXXXXXXXXXXXXXXXXXXXXXX',
                 'X                       X',
                 'XP                      X',
                 'XXX XAX XXXXXXXXXXXXXXXXX',
                 'XXX XXXOXXXXXXXXXXXXXXXXX',
                 'XXX XXX XXXXXXXXXXXXXXXXX',
                 'XXX XXXOXXXXXXXXXXXXXXXXX',
                 'XXX XXX XXXXXXXXXXXXXXXXX',
                 'XXX XXXAXXXXXXXXXXXXXXXXX',
                 'XXXOXXXXXXXXXXXXXXXXXXXXX',
                 'XXXXXXXXXXXXXXXXXXXXXXXXX']
}

level_DAO.add_level(teste)