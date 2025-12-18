from random import randint, choice


def is_valid_position(ship_cells, existing_ships): # можно ли разместить корабль
    for x, y in ship_cells:
        if not (0 <= x < 10 and 0 <= y < 10):
            return False

        for ship in existing_ships:
            for sx, sy in ship:
                if abs(x - sx) <= 1 and abs(y - sy) <= 1:
                    return False
    return True


def ship_place(): # расставляет корабли(возвращает список)
    all_ships = []

    # 4х палубный корабль
    while True:
        ship_4 = []
        row = randint(0, 9)
        if choice([True, False]):
            column = randint(0, 6)
            for _ in range(4):
                ship_4.append((row, column))
                column += 1
        else:
            column = randint(0, 6)
            for _ in range(4):
                ship_4.append((column, row))
                column += 1

        if is_valid_position(ship_4, all_ships):
            all_ships.append(ship_4)
            break

    # 3х палубные корабли (2 штуки)
    for _ in range(2):
        while True:
            ship_3 = []
            row = randint(0, 9)

            if choice([True, False]):
                # Горизонтальный
                column = randint(0, 7)
                for _ in range(3):
                    ship_3.append((row, column))
                    column += 1
            else:
                # Вертикальный
                column = randint(0, 7)
                for _ in range(3):
                    ship_3.append((column, row))
                    column += 1

            if is_valid_position(ship_3, all_ships):
                all_ships.append(ship_3)
                break

    # 2х палубные корабли (3 штуки)
    for _ in range(3):
        while True:
            ship_2 = []
            row = randint(0, 9)

            if choice([True, False]):
                # Горизонтальный
                column = randint(0, 8)
                for _ in range(2):
                    ship_2.append((row, column))
                    column += 1
            else:
                # Вертикальный
                column = randint(0, 8)
                for _ in range(2):
                    ship_2.append((column, row))
                    column += 1

            if is_valid_position(ship_2, all_ships):
                all_ships.append(ship_2)
                break

    # 1х палубные корабли (4 штуки)
    for _ in range(4):
        while True:
            ship_1 = []
            row = randint(0, 9)
            column = randint(0, 9)
            ship_1.append((row, column))

            if is_valid_position(ship_1, all_ships):
                all_ships.append(ship_1)
                break

    return all_ships