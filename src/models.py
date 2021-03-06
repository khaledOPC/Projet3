import random


class Game:
    def __init__(self):
        self.player = None
        self.boss = None
        self.items = []
        self.list_box = []
        self.width = 0
        self.load_map()
        self.random_items()

    def __repr__(self):
        return f"Game {self.game}"

    def message(self):
        return "il reste"

    def message_2(self):
        return "items"

    def and_message(self):
        if self.player.position == self.boss.position:
            if self.player.fight():
                return "j'ai gagné"
            else:
                return "j'ai perdu"

    def count_missing_items(self):
        return len(([1 for item in self.items if not item.is_taken]))

    def position_to_coordinate(self, position, offset):
        x = position // self.width
        y = position % self.width
        return (y * offset, x * offset)

    def load_map(self):
        """
        method for read the map.txt
        """
        file = open("map.txt", "r")

        lines = file.readlines()

        file.close()
        index = 0
        self.width = len(lines[0].strip())

        for line in lines:
            line = line.strip()

            for letter in line:
                if letter == "W":
                    self.list_box.append(Box(box_type="WHITE"))
                elif letter == "B":
                    self.list_box.append(Box(box_type="BLACK"))
                elif letter == "M":
                    self.list_box.append(Box(box_type="BLACK"))
                    self.player = Player(position=index)
                elif letter == "G":
                    self.list_box.append(Box(box_type="BLACK"))
                    self.boss = Boss(position=index)
                else:
                    continue
                index += 1

    def random_items(self):
        """
        method to randomly diplay items
        """
        place_disponible = []

        for i, box in enumerate(self.list_box):
            if (
                box.is_black()
                and not self.player.in_position(i)
                and not self.boss.in_position(i)
            ):  # noqa
                place_disponible.append(i)
        x = random.sample(place_disponible, k=3)
        self.items.append(Item(position=x[0], name="Ether"))
        self.items.append(Item(position=x[1], name="Aiguille"))
        self.items.append(Item(position=x[2], name="Sereingue"))

    def display_game(self):
        line = ""
        for i, box in enumerate(self.list_box):
            if i == self.player.position:
                line += "M"
            elif i == self.boss.position:
                line += "G"
            elif i == self.items[0].position and not self.items[0].is_taken:
                line += self.items[0].name[0]
            elif i == self.items[1].position and not self.items[1].is_taken:
                line += self.items[1].name[0]
            elif i == self.items[2].position and not self.items[2].is_taken:
                line += self.items[2].name[0]
            elif box.box_type == "WHITE":
                line += "W"
            else:
                line += "B"
            if (i + 1) % self.width == 0:
                line += "\n"

    def black_position(self, position):
        """
        method to know if we are in a BLACK or WHITE position
        """
        return self.list_box[position].box_type == "BLACK"

    def check_game(self):
        """
        method to verify if player have take all items and if he have won
        """
        for item in self.items:
            if self.player.position == item.position and not item.is_taken:
                self.player.add_item(item)
        if self.player.position == self.boss.position:
            if self.player.fight():
                return "j'ai gagné"
            else:
                return "j'ai perdu"

    def move_right(self):
        """
        We check if we can move right and if this is a black position or not
        """
        new_position = self.player.position + 1

        if self.player.position % self.width != 0 and self.black_position(
            new_position
        ):  # noqa
            self.player.position = new_position

    def move_left(self):
        """
        We check if we can move left and if this is a black position or not
        """
        new_position = self.player.position - 1

        if (self.player.position - 1) % self.width != 0 and self.black_position(
            new_position
        ):  # noqa
            self.player.position = new_position

    def move_down(self):
        """
        We check if we can move down and if this is a black position or not
        """
        new_position = self.player.position + self.width

        if new_position < (self.width * self.width) and self.black_position(
            new_position
        ):  # noqa
            self.player.position += self.width

    def move_up(self):
        """
        We check if we can move up and if this is a black position or not
        """
        new_position = self.player.position - self.width

        if new_position > 0 and self.black_position(new_position):
            self.player.position = new_position


class Player:
    def __init__(self, position):
        self.position = position
        self.items = []
        self.score_item = []

    def __repr__(self):
        return f"Player {self.position}"

    def add_item(self, item):
        """
        method to add items in a list when the player is in the same position as them # noqa
        """
        self.items.append(item)
        item.is_taken = True

    def fight(self):
        """
        if player have the 3 items he can fight with the boss and win
        """
        return len(self.items) == 3

    def in_position(self, position):
        return self.position == position


class Item:
    def __init__(self, name, position, is_taken=False):
        self.position = position
        self.is_taken = is_taken
        self.name = name

    def __repr__(self):
        return f"{self.name}"


class Box:
    def __init__(self, box_type):
        """
        instance of black or white box
        """
        self.box_type = box_type

    def __repr__(self):
        return f"Object {self.box_type}"

    def is_black(self):
        return self.box_type == "BLACK"


class Boss:
    def __init__(self, position):
        self.position = position

    def __repr__(self):
        return f"Boss {self.position}"

    def in_position(self, position):
        return self.position == position
