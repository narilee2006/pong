import pygame

pygame.init()
WIDTH = 900
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("마지막 프로젝트 Python Pong")
font20 = pygame.Font(None, 20)
clock = pygame.Clock()


class Paddle:
    def __init__(self, x, y, width, height, speed, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def display(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self, y_velocity):
        self.y += self.speed * y_velocity

        if self.y <= 0:
            self.y = 0
        elif self.y + self.height >= HEIGHT:
            self.y = HEIGHT - self.height

        self.rect = (self.x, self.y, self.width, self.height)

    def displayScore(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        screen.blit(text, textRect)


class Ball:
    def __init__(self, x, y, radius, speed, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.color = color
        self.x_velocity = 1
        self.y_velocity = -1
        self.rect = pygame.draw.circle(
            screen, self.color, (self.x, self.y), self.radius
        )
        self.firstTime = 1

    def display(self):
        self.rect = pygame.draw.circle(
            screen, self.color, (self.x, self.y), self.radius
        )

    def update(self):
        self.x += self.speed * self.x_velocity
        self.y += self.speed * self.y_velocity

        if self.y <= 0 or self.y >= HEIGHT:
            self.y_velocity *= -1

        if self.x <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.x >= WIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.x_velocity *= -1
        self.firstTime = 1

    def hit(self):
        self.x_velocity *= -1

player1 = Paddle(20, 0, 10, 100, 10, (0, 255, 255))
player2 = Paddle(WIDTH - 30, 0, 10, 100, 10, (0, 255, 255))
ball = Ball(WIDTH // 2, HEIGHT // 2, 7, 7, (255, 255, 255))

players = [player1, player2]

player1Score = 0
player2Score = 0
player1_y_velocity = 0
player2_y_velocity = 0

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player2_y_velocity = -1
            if event.key == pygame.K_DOWN:
                player2_y_velocity = 1
            if event.key == pygame.K_w:
                player1_y_velocity = -1
            if event.key == pygame.K_s:
                player1_y_velocity = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player2_y_velocity = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player1_y_velocity = 0

    for player in players:
        if pygame.Rect.colliderect(ball.rect, player.rect):
            ball.hit()

    player1.update(player1_y_velocity)
    player2.update(player2_y_velocity)

    point = ball.update()
    if point == -1:
        player1Score += 1
    elif point == 1:
        player2Score += 1

    if point:
        ball.reset()

    player1.display()
    player2.display()
    ball.display()

    player1.displayScore("Player 1 : ", player1Score, 100, 20, (255, 255, 255))
    player2.displayScore("Player 2 : ", player2Score, WIDTH - 100, 20, (255, 255, 255))

    pygame.display.update()
    clock.tick(60)
