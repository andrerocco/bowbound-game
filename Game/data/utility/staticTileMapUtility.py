from utility.exceptions.TileMapErrorException import TileMapErrorException
from pyexcel_ods import get_data
from typing import List
import sys

sys.path.append("..")
# https://pythonhosted.org/pyexcel-ods/#read-from-an-ods-file


class TileMapUtility:
    # Converts a level dictionary to a dictionary with the propper textures
    # Parameters level_dict should be a dictionary with the following exampled values:
    # 'level_name': 'name'
    # 'arrows': ['standard', 'bounce', 'fast', 'piercing'] < ordered list of arrows >
    # 'tile_map': < list of strings representing the map layout >
    @staticmethod
    def convert(level_dict: dict) -> dict:
        # Tratamento dos possíveis erros
        if 'level_name' not in level_dict:
            raise Exception("Key 'level_name' not found in level_dict.")
        elif 'arrows' not in level_dict:
            raise TileMapErrorException(
                "Key 'arrows' not found in level_dict.")
        elif 'tile_map' not in level_dict:
            raise TileMapErrorException(
                "Key 'tile_map' not found in level_dict.")

        if len(level_dict['arrows']) == 0:
            raise TileMapErrorException(
                "Value of 'arrows' is empty. It should be a list with at leat one arrow type.")
        for arrow in level_dict['arrows']:
            if arrow not in ['standard', 'bounce', 'fast', 'piercing']:
                raise TileMapErrorException(
                    f"Value 'arrows' contains an invalid arrow type: {arrow}.")

        if len(level_dict['tile_map']) <= 5 or len(level_dict['tile_map'][0]) <= 5:
            raise TileMapErrorException(
                "Value 'tile_map' is empty. It should be a list with at leat 5 rows and 5 columns.")

        # Converte o tile map
        try:
            converted_tile_map = TileMapUtility.convert_tile_map(
                level_dict['tile_map'])
        except Exception as e:
            raise e

        level_dict['textures'] = converted_tile_map
        return level_dict

    # Converts a list of tiles into a list of proper textures names.
    # Parameter tile_map should be a list of strings representing the map layout.
    @staticmethod
    def convert_tile_map(tile_map: List[str]) -> List[str]:

        st = tile_map.copy()
        st.insert(0, ["X" for _ in range((len(st[0])))])
        st.append(["X" for _ in range((len(st[0])))])

        return_list = [[] for _ in range(len(st) - 2)]

        for i in range(len(st)):
            item = list(st[i])
            item.insert(0, "X")
            item.append("X")
            st[i] = item

        for x in range(1, len(st[0]) - 1):
            for y in range(1, len(st) - 1):
                context = {
                    "up_left": False,
                    "up": False,
                    "up_right": False,
                    "left": False,
                    "right": False,
                    "down_left": False,
                    "down": False,
                    "down_right": False,
                }
                if st[y][x] == " ":
                    return_list[y - 1].append(" ")
                elif st[y][x] == "A":
                    return_list[y - 1].append("A")
                elif st[y][x] == "P":
                    return_list[y - 1].append("P")
                elif st[y][x] == "D":
                    return_list[y - 1].append("D")
                elif st[y][x] == "O":
                    return_list[y - 1].append(" O ")
                elif st[y][x] == "X":
                    if st[y - 1][x - 1] == "X":
                        context["up_left"] = True
                    if st[y][x - 1] == "X":
                        context["left"] = True
                    if st[y + 1][x - 1] == "X":
                        context["down_left"] = True
                    if st[y - 1][x] == "X":
                        context["up"] = True
                    if st[y + 1][x] == "X":
                        context["down"] = True
                    if st[y - 1][x + 1] == "X":
                        context["up_right"] = True
                    if st[y][x + 1] == "X":
                        context["right"] = True
                    if st[y + 1][x + 1] == "X":
                        context["down_right"] = True
                    return_list[y - 1].append(
                        "B_" + str(TileMapUtility.__get_tile(context))
                    )
                else:
                    return_list[y - 1].append(" ")

        return return_list

    @staticmethod
    def __get_tile(c: dict) -> int:
        if (c["left"] and c["up"] and c["right"] and c["down"]
                and not c["down_left"] and not c["down_right"] and not c["up_left"] and not c["up_right"]):
            return 17
        elif (c["up"] and c["right"] and c["left"] and c["down"]
                and c["up_left"] and c["up_right"] and c["down_left"] and c["down_right"]):
            return "black"  # black?
        elif (c["left"] and c["up"] and c["right"] and c["down"]
              and not c["down_right"] and not c["up_right"]):
            return 13
        elif (c["left"] and c["up"] and c["right"] and c["down"]
              and not c["down_right"] and not c["down_left"]):
            return 14
        elif (c["left"] and c["up"] and c["right"] and c["down"]
              and not c["down_left"] and not c["up_left"]):
            return 15
        elif (c["left"] and c["up"] and c["right"] and c["down"]
              and not c["up_right"] and not c["up_left"]):
            return 16
        elif c["up"] and c["left"] and not c["right"] and c["down"] and not c["up_left"] and not c["down_left"]:
            return 25
        elif c["up"] and c["left"] and c["right"] and not c["down"] and not c["up_left"] and not c["up_right"]:
            return 26
        elif c["up"] and not c["left"] and c["right"] and c["down"] and not c["up_right"] and not c["down_right"]:
            return 27
        elif not c["up"] and c["left"] and c["right"] and c["down"] and not c["down_left"] and not c["down_right"]:
            return 28
        elif not c["up"] and not c["left"] and c["right"] and c["down"] and not c["down_right"]:
            return 29
        elif not c["up"] and c["left"] and not c["right"] and c["down"] and not c["down_left"]:
            return 30
        elif c["up"] and not c["left"] and c["right"] and not c["down"] and not c["up_right"]:
            return 31
        elif c["up"] and c["left"] and not c["right"] and not c["down"] and not c["up_left"]:
            return 32
        elif (c["left"] and c["down"] and c["up"] and c["right"] and not c["down_right"]):
            return 9
        elif (c["left"] and c["down"] and c["up"] and c["right"] and not c["down_left"]):
            return 10
        elif (c["left"] and c["down"] and c["up"] and c["right"] and not c["up_right"]):
            return 11
        elif (c["left"] and c["down"] and c["up"] and c["right"] and not c["up_left"]):
            return 12
        elif (not c["left"] and not c["up"] and c["right"] and c["down"]):
            return 1
        elif (c["left"] and not c["up"] and not c["right"] and c["down"]):
            return 2
        elif (not c["left"] and c["up"] and c["right"] and not c["down"]):
            return 3
        elif (c["left"] and c["up"] and not c["right"] and not c["down"]):
            return 4
        elif (not c["left"] and c["up"] and c["right"] and c["down"]):
            return 5
        elif (c["left"] and not c["up"] and c["right"] and c["down"]):
            return 6
        elif (c["left"] and c["up"] and not c["right"] and c["down"]):
            return 7
        elif (c["left"] and c["up"] and c["right"] and not c["down"]):
            return 8
        elif not c["up"] and not c["down"] and not c["right"] and not c["left"]:
            return 18
        elif not c["up"] and not c["down"] and c["right"] and c["left"]:
            return 19
        elif c["up"] and c["down"] and not c["right"] and not c["left"]:
            return 20
        elif not c["up"] and not c["down"] and not c["right"] and c["left"]:
            return 21
        elif not c["up"] and not c["down"] and c["right"] and not c["left"]:
            return 22
        elif c["up"] and not c["down"] and not c["right"] and not c["left"]:
            return 23
        elif not c["up"] and c["down"] and not c["right"] and not c["left"]:
            return 24
        else:
            return " "

    @staticmethod
    def import_map_from_ods(path) -> None:
        # TODO Atualizar para novo formato
        # Recebe um path absoluto de um .ods relativo a um mapa, e retorna um dict formatado para inserir no LevelDAO
        try:

            map_file = get_data(path)['Sheet1']
            tile_map = []
            for y in range(1, 12):
                st = ""
                for x in range(1, 24):
                    cell = map_file[y][x]
                    if cell == "":
                        st += " "
                    else:
                        st += cell.upper()
                tile_map.append(st)

            arrs = {
                "S": "standard",
                "F": "fast",
                "P": "piercing",
                "B": "bounce"
            }

            arrows = list(map(lambda a: arrs[a], [x.replace(
                " ", "").upper() for x in map_file[14][0].split(",")]))
            level_name = map_file[0][-1]
            level = {
                'level_name': level_name,
                'arrows': arrows,
                'tile_map': tile_map,
                'textures': TileMapUtility.convert_tile_map(tile_map)
            }

            # TileMapUtility.__verify_map(level)
            return level
        except ValueError as e:
            print(e)
        except TileMapErrorException as e:
            print(e)
        except Exception as e:
            print(e)
