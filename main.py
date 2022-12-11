# Complete your game here
import pygame
from random import randint
from math import sin, cos

class CollectingCoins:
    def __init__(self, window_width: int = 800, window_height: int = 600) -> None:
        pygame.init()
        self.window_width = window_width
        self.window_height = window_height
        self.load_images()
        self.inactive_screen_height = 50
        self.game_font = pygame.font.SysFont("Arial", 24)

        self.new_game() 

        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Collecting Coins")

        self.main_loop()

    def load_images(self) -> None:
        img_list = ["robot", "coin", "monster", "door"]
        self.images = [pygame.image.load(f"{name}.png") for name in img_list]
        

    def new_game(self) -> None:
        self.game_font = pygame.font.SysFont("Arial", 24)
        self.points = 0
        self.lives = 3
        self.monster_x = None
        self.monster_y = None
        self.monster_angle_speed = 0.02
        self.monster_speed = 0.5
        self.monster_angle = 0
        self.door_x = None
        self.door_y = None
        self.init_robot()
        self.init_coin()

    def main_loop(self) -> None:
        while True:
            self.check_events()
            self.draw_window()
            if not self.game_is_over():
                self.move_robot()
            self.move_monster()
            self.monster_angle += self.monster_angle_speed
            self.clock.tick()

    def game_is_over(self) -> bool:
        return self.lives <= 0 or self.points >= 20
        
    def init_robot(self) -> None:
        self.robot_width = self.images[0].get_width()
        self.robot_height = self.images[0].get_height()
        while True:
            self.robot_x = randint(0, self.window_width - self.robot_width)
            self.robot_y = randint(self.inactive_screen_height, self.window_height - self.robot_height)
            # if no monster has been initialized
            if self.monster_x == None and self.monster_y == None:
                break
            # else if if monster has already been initialized and it is far enough from robot
            elif self.robot_far_enough_from_monster():
                break

        self.robot_to_right = False
        self.robot_to_left = False
        self.robot_up = False
        self.robot_down = False

    def robot_far_enough_from_monster(self) -> bool:
        return (self.monster_x + 2 * self.monster_width < self.robot_x or self.robot_x + self.robot_width < self.monster_x - 2 * self.monster_width) and \
                (self.monster_y + 2 * self.monster_height < self.robot_y or self.robot_y + self.robot_height < self.monster_y - 2 * self.monster_height)

    def init_coin(self) -> None:
        self.coin_width = self.images[1].get_width()
        self.coin_height = self.images[1].get_height()
        self.monster_width = self.images[2].get_width()
        self.monster_height = self.images[2].get_height()
        while True:
            self.coin_x = randint(0, self.window_width - self.coin_width)
            self.coin_y = randint(self.inactive_screen_height, self.window_height - self.coin_height)
            # we must make sure that the coin will not overlap the robot and the distance takes into account the dimensions of the rotating monster
            if (self.coin_x + self.coin_width + self.monster_width < self.robot_x or self.robot_x + self.robot_width < self.coin_x - self.monster_width) and \
                (self.coin_y + self.coin_height + self.monster_height< self.robot_y or self.robot_y + self.robot_height < self.coin_y - self.monster_height):
                self.init_monster()
                break

    def init_monster(self) -> None:
        self.coin_center = (self.coin_x + self.coin_width / 2, self.coin_y + self.coin_height / 2)
        while True:
            self.monster_x = randint(0, self.window_width - self.monster_width)
            self.monster_y = randint(self.inactive_screen_height, self.window_height - self.monster_height)
            # we must make sure that the attacking monster will be far enough from the robot
            if self.robot_far_enough_from_monster():
                self.move_monster()
                break

    def init_door(self) -> None:
        self.door_width = self.images[3].get_width()
        self.door_height = self.images[3].get_height()
        while True:
            door_attempt_x = randint(0, self.window_width - self.monster_width)
            door_attempt_y = randint(self.inactive_screen_height, self.window_height - self.monster_height)
            # we must make sure that the door is far enough from the cicling monster
            if (self.coin_center[0] + 4 * self.monster_width < door_attempt_x or door_attempt_x + self.door_width < self.coin_center[0] - 4 * self.monster_width) and \
                (self.coin_center[1] + 3 * self.monster_height < door_attempt_y or door_attempt_y + self.door_height < self.coin_center[1] - 3 * self.monster_height):
                self.door_x = door_attempt_x
                self.door_y = door_attempt_y
                break
        
    def move_monster(self) -> None:
        # make a monster move round and round a coin
        self.monster_circle_x =  self.coin_center[0] + cos(self.monster_angle) * self.coin_width * 1.5 - self.monster_width / 2
        self.monster_circle_y =  self.coin_center[1] + sin(self.monster_angle) * self.coin_height * 1.5 - self.monster_height / 2
        # make another monster approach the robot
        if self.robot_x < self.monster_x:
            self.monster_x -= self.monster_speed
        if self.robot_x > self.monster_x:
            self.monster_x += self.monster_speed
        if self.robot_y < self.monster_y:
            self.monster_y -= self.monster_speed
        if self.robot_y > self.monster_y:
            self.monster_y += self.monster_speed

    def check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.robot_to_left = True
                if event.key == pygame.K_RIGHT:
                    self.robot_to_right = True
                if event.key == pygame.K_UP:
                    self.robot_up = True
                if event.key == pygame.K_DOWN:
                    self.robot_down = True
                # pressing 2 restarts the game
                if event.key == pygame.K_2:
                    self.new_game()
                # pressing 0 quits the game
                if event.key == pygame.K_0:
                    exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.robot_to_left = False
                if event.key == pygame.K_RIGHT:
                    self.robot_to_right = False
                if event.key == pygame.K_UP:
                    self.robot_up = False
                if event.key == pygame.K_DOWN:
                    self.robot_down = False

    def draw_window(self) -> None:
        if self.game_is_over() and self.points < 20:
            self.game_font = pygame.font.SysFont("Arial", 48)
            game_text = self.game_font.render(f"GAME OVER!!! Points: {self.points}", True, (0, 255, 0 ))
            self.window.blit(game_text, (self.window_width / 2 - game_text.get_width() / 2, self.window_height / 2 - game_text.get_height()))
            pygame.display.flip()
            return
        if self.game_is_over():
            self.game_font = pygame.font.SysFont("Arial", 48)
            game_text = self.game_font.render(f"You WON the GAME!!! Points: {self.points}", True, (0, 255, 0 ))
            self.window.blit(game_text, (self.window_width / 2 - game_text.get_width() / 2, self.window_height / 2 - game_text.get_height()))
            pygame.display.flip()
            return
        robot = self.images[0]
        coin = self.images[1]
        monster = self.images[2]
        door = self.images[3]
        self.window.fill((128, 128, 128))
        # display the door
        if self.door_x is not None and self.door_y is not None:
            self.window.blit(door, (self.door_x, self.door_y))
        # display the robot
        self.window.blit(robot, (self.robot_x, self.robot_y))
        # display the coin
        self.window.blit(coin, (self.coin_x, self.coin_y))
        # display the approaching monster
        self.window.blit(monster, (self.monster_x, self.monster_y))
        # display the circling monster 
        self.window.blit(monster, (self.monster_circle_x, self.monster_circle_y))
        # display points, information and lives remaining
        game_text = self.game_font.render(f"Points: {self.points}", True, (0, 255, 0 ))
        self.window.blit(game_text, (25, 10))
        self.game_font = pygame.font.SysFont("Arial", 12)
        game_text = self.game_font.render("2 = new game", True, (0, 0, 255))
        self.window.blit(game_text, (self.window_width / 2 - 120, 10))
        game_text = self.game_font.render("0 = quit game", True, (0, 0, 255))
        self.window.blit(game_text, (self.window_width / 2, 10))
        self.game_font = pygame.font.SysFont("Arial", 30)
        game_text = self.game_font.render(f"{self.lives * '♥'}", True, (255, 0, 0))
        self.window.blit(game_text, (self.window_width - self.lives * 20, 10))
        self.game_font = pygame.font.SysFont("Arial", 24)
        
        pygame.display.flip()

    def move_robot(self) -> None:
        robot_speed = 2
        if self.robot_to_right:
            self.robot_x += robot_speed
            self.robot_x = min(self.robot_x, self.window_width - self.images[0].get_width())
        if self.robot_to_left:
            self.robot_x -= robot_speed
            self.robot_x = max(self.robot_x, 0)
        if self.robot_down:
            self.robot_y += robot_speed
            self.robot_y = min(self.robot_y, self.window_height - self.images[0].get_height())
        if self.robot_up:
            self.robot_y -= robot_speed
            self.robot_y = max(self.robot_y, self.inactive_screen_height)
        # if robot touches the coin
        if self.robot_touches_entity(self.coin_x, self.coin_y, self.coin_width, self.coin_height):
            self.points += 1
            # for every 2 points achieved we display the door which enables the robot to gain an extra life if it makes through it
            if self.points % 2 == 0 and self.points > 0:
                self.init_door()
            # increase the speed of circling monster
            if self.monster_angle_speed < 0.05:
                self.monster_angle_speed += 0.005
            # re-init the coin
            self.init_coin()
        # if robot touches any of the monsters
        if self.robot_touches_entity(self.monster_x, self.monster_y, self.monster_width, self.monster_height) or self.robot_touches_entity(self.monster_circle_x, self.monster_circle_y, self.monster_width, self.monster_height):
            self.lives -= 1
            if not self.game_is_over():
                self.init_robot()
        # if door is displayed and the robot makes it through
        if self.door_x is not None and self.door_y is not None and self.robot_touches_entity(self.door_x, self.door_y, self.door_width, self.door_height):
            # add an Xtra life to robot
            self.lives += 1
            # make the door disappear
            self.door_x = None
            self.door_y = None
            # increase monster speed by 10% if it is below 1.2
            if self.monster_speed < 1.2:
                self.monster_speed *= 1.1


    def robot_touches_entity(self, object_x, object_y, object_width, object_height) -> bool:
        return object_x + object_width >= self.robot_x and object_x <= self.robot_x + self.robot_width and \
            object_y + object_height >= self.robot_y and object_y <= self.robot_y + self.robot_height



if __name__ == '__main__':
    print("\nWelcome to Collecting Coins Game!")
    print("\nTry to collect 20 coins to win the game")
    print('You can move the robot character with the arrow keys on the keyboard')
    print("Take advantage of the doors, which will give you an extra life, but watch out for monsters....")
    print("""
    Please choose preferred resolution:
        
        1. 1024x760 (medium difficulty)
        2. 800x600 (default)
        3. 640x480 (most difficult, might be buggy)
        4. 1280x1024 (easy)
        5. 1980x1080 (easiest)
        """)
    try:
        command = int(input("Enter your choice: "))
        if command == 1:
            CollectingCoins(1024, 768)
        elif command == 2:
            CollectingCoins()
        elif command == 3:
            CollectingCoins(640, 480)
        elif command == 4:
            CollectingCoins(1280, 1024)
        elif command == 5:
            CollectingCoins(1980, 1080)
    except:
        ValueError
        print("Bye... Quitting...")