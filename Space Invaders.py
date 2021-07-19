import pygame
import sys

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60

COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)

class Attack:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Bunker:
    def __init__(self, x, y, times_hit):
        self.x = x
        self.y = y
        self.times_hit = times_hit

    def generate(self, x, y):
        self.blocks = []
        for i in range(0, 5):
            self.blocks.append(Bunker(x, y, 0))
            x += 35

    def render(self):
        for i in range(0, 5):
            if self.blocks[i].x != 0 and self.blocks[i].y != 0:
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.blocks[i].x, self.blocks[i].y, 30, 30))

    def destroy(self, rect1):
        for i in range(0, 5):
            # current = bunker block
            current = pygame.Rect(self.blocks[i].x, self.blocks[i].y, 30, 30)
            if current.colliderect(rect1) == 1:
                if self.blocks[i].times_hit < 2:
                    self.blocks[i].times_hit += 1
                    return 1
                elif self.blocks[i].times_hit == 2:
                    self.blocks[i].x = 0
                    self.blocks[i].y = 0
                    return 1


class Ship:
    def generate(self):
        x = 10
        y = 10
        self.rows = []
        self.ship_speed = 5
        for i in range(0, 5):
            invaders = []
            for j in range(0, 5):
                inv = Invader(x, y)
                invaders.append(inv)
                x += 50
            y += 50
            self.rows.append(invaders)
            x = 10

    def destroy(self, rect1):
        for i in range(0, 5):
            for j in range(0, 5):
                # current = ship invader
                current = pygame.Rect(self.rows[i][j].x, self.rows[i][j].y, 50, 50)
                if current.colliderect(rect1) == 1:
                    self.rows[i][j].x = 0
                    self.rows[i][j].y = 0
                    return 1
        return -1

    def update(self):
        i = 0
        j = 4
        while self.rows[0][i].x == 0 and self.rows[0][i].y == 0:
            if i < 4:
                i += 1
            else:
                break
        while self.rows[0][j].x == 0 and self.rows[0][j].y == 0:
            if j > 0:
                j -= 1
            else:
                break

        if self.rows[0][j].x + self.ship_speed > (WIDTH - 50) and self.ship_speed > 0 :
            self.ship_speed = -self.ship_speed
        elif self.rows[0][i].x + self.ship_speed < 20 and self.ship_speed < 0:
          self.ship_speed = -self.ship_speed

        for i in range(0,5):
            for j in range(0,5):
                if self.rows[i][j].x != 0 and self.rows[i][j].y != 0:
                     self.rows[i][j].x += self.ship_speed

    def render(self):
        for i in range(0, 5):
            for j in range(0, 5):
                if self.rows[i][j].x != 0 and self.rows[i][j].y != 0:
                    self.rows[i][j].render()

    def attacker(self):
        j = 0
        i = 4
        while self.rows[i][j].x == 0 and self.rows[i][j].y == 0 and j <= 4 and i >= 0:
            if j == 4:
                i -= 1
                j = 0
            j += 1
            # Game won
            if i == 0 and j == 4 and self.rows[i][j].x == self.rows[i][j].y == 0:
                return 99
        self.attacker_i = i
        self.attacker_j = j
        return 0


class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullet = pygame.image.load('bullet.png')
        self.bullet = pygame.transform.scale(self.bullet, (10, 20))

    def update(self, dir):
        # dir ia valorile 1 sau -1 in functie de sensul proiectilului
        self.y += dir * 10

    def render(self):
        screen.blit(self.bullet, (self.x, self.y))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lives = 3

    def render(self):
        player = pygame.image.load('player.png')
        player = pygame.transform.scale(player, (50, 50))
        screen.blit(player, (self.x, self.y))

    def destroy(self, rect1):
        # current = player
        current = pygame.Rect(self.x, self.y, 50, 50)
        if current.colliderect(rect1) == 1:
            self.lives -= 1
            return 1
        return -1


class Invader:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.invader = pygame.image.load('alien.png')
        self.invader = pygame.transform.scale(self.invader, (50, 50))

    def render(self):
        screen.blit(self.invader, (self.x, self.y))


def main(HighScore):
    # Initialize imported pygame modules
    pygame.init()
    pygame.font.init()

    #display score

    HighScore_font = pygame.font.SysFont('Comic Sans MS', 30)

    score_font = pygame.font.SysFont('Comic Sans MS', 30)
    score = 0

    #display lives
    lives_font = pygame.font.SysFont('Comic Sans MS', 30)

    # Set the window's caption
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()

    background = pygame.image.load('background.png')
    # background = pygame.Surface((WIDTH, HEIGHT))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    # background.fill(COLOR_BLACK)

    # Blit everything to screen
    screen.blit(background, (0, 0))

    # Update the screen
    pygame.display.flip()
    player = Player(50, HEIGHT - 50)

    ship = Ship
    ship.generate(ship)

    # bunkers

    bunker1 = Bunker(50, 50, 0)
    bunker1.generate(50, HEIGHT-200)

    bunker2 = Bunker(30, 30, 0)
    bunker2.generate(WIDTH-300, HEIGHT-200)


    # Main loop
    while True:
        clock.tick(FPS)

        if player.lives == 0:
            break

        # Erase everything drawn at last step by filling the background
        # with color black
        # background.fill(COLOR_BLACK)

        #score display

        HighScoreSurface = HighScore_font.render("High Score:%d" % (HighScore), False, (255, 255, 255))
        screen.blit(HighScoreSurface, (0, 40))


        textsurface = score_font.render("Score:%d" % (score), False, (255, 255, 255))
        screen.blit(textsurface, (0, 0))

        #display lives

        livesSurface = lives_font.render("Lives:%d" % (player.lives), True, (255, 255, 255))
        screen.blit(livesSurface, (0, HEIGHT - 50))

        # bunkers

        bunker1.render()
        bunker2.render()

        # spaceship

        ship.render(ship)

        player.render()

        # attacker


        try:
            bullet_attacker
        except NameError:
            has_won = ship.attacker(ship)
            if has_won == 99:
                break
            attacker = Attack(ship.rows[ship.attacker_i][ship.attacker_j].x, ship.rows[ship.attacker_i][ship.attacker_j].y)
            bullet_attacker = Projectile(attacker.x, attacker.y)

        try:
            bullet_attacker.render()
        except NameError:
            pass

        try:
            bullet.render()
        except NameError:
            pass

        # Check for Quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Check for key presses and update paddles accordingly
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a]:
            if player.x > 0:
                player.x -= 10
        if keys_pressed[pygame.K_d]:
            if player.x + 50 < WIDTH:
                player.x += 10
        if keys_pressed[pygame.K_SPACE]:
            try:
                bullet
            except NameError:
                bullet = Projectile(player.x, player.y)

        # Update game state

        ship.update(ship)

        try:
            bullet.update(-1)
            has_hit = 0
            has_hit = ship.destroy(ship, pygame.Rect(bullet.x, bullet.y, 10, 20))
            has_hit_bunker = 0
            has_hit_bunker = bunker1.destroy(pygame.Rect(bullet.x, bullet.y, 10, 20))
            has_hit_bunker = has_hit_bunker or bunker2.destroy(pygame.Rect(bullet.x, bullet.y, 10, 20))
            if has_hit == 1 or bullet.y == 0 or has_hit_bunker == 1:
                del bullet
                if has_hit == 1:
                    score += 10
        except NameError:
            pass

        try:
            bullet_attacker.update(1)
            has_hit = 0
            has_hit = player.destroy(pygame.Rect(bullet_attacker.x, bullet_attacker.y, 10, 20))
            has_hit_bunker = 0
            has_hit_bunker = bunker1.destroy(pygame.Rect(bullet_attacker.x, bullet_attacker.y, 10, 20))
            has_hit_bunker = has_hit_bunker or bunker2.destroy(pygame.Rect(bullet_attacker.x, bullet_attacker.y, 10, 20))
            if has_hit == 1 or bullet_attacker.y > HEIGHT or has_hit_bunker == 1:
                del bullet_attacker
        except NameError:
            pass

        # Render current game state

        pygame.display.flip()
        screen.blit(background, (0, 0))

    # game over screen
    over_font = pygame.font.SysFont('Comic Sans MS', 30)
    oversurface = over_font.render("Game over", False, (255, 255, 255))
    action_font = pygame.font.SysFont('Comic Sans MS', 30)
    actionsurface = action_font.render("Press Esc to start again", False, (255, 255, 255))
    while True:
        screen.blit(oversurface, (WIDTH/2 - 100, HEIGHT/2 - 65))
        screen.blit(actionsurface, ( WIDTH/2 - 135, HEIGHT/2 - 35))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_ESCAPE]:
                main(score)
        pygame.display.flip()



if __name__ == '__main__':
    main(0)