import pygame

pygame.init()

# Game parameters
GAME_WIDTH = 800
GAME_HEIGHT = 600

screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("AI Pong")

# Score system
score = [0, 0]
font = pygame.font.Font(None, 36)
WINNING_SCORE = 5
game_over = False

# Game clock
clock = pygame.time.Clock()

# Paddle parameters
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100

# Ball
BALL_SIZE = 10
BALL_SPEED = [5, 5]
ball = pygame.Rect(GAME_WIDTH / 2 - BALL_SIZE / 2, GAME_HEIGHT / 2 - BALL_SIZE / 2, BALL_SIZE, BALL_SIZE)

# Player paddle
player_paddle = pygame.Rect(50, GAME_HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
PLAYER_SPEED = 0

# AI paddle
ai_paddle = pygame.Rect(GAME_WIDTH - 50 - PADDLE_WIDTH, GAME_HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
AI_SPEED = 4.55

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                PLAYER_SPEED = -5
            elif event.key == pygame.K_s:
                PLAYER_SPEED = 5
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                PLAYER_SPEED = 0
    
    # Paddle movement
    player_paddle.y += PLAYER_SPEED
    player_paddle.y = max(0, min(GAME_HEIGHT - PADDLE_HEIGHT, player_paddle.y))

    # AI paddle movement
    if ai_paddle.centery < ball.centery:
        ai_paddle.y += AI_SPEED
    elif ai_paddle.centery > ball.centery:
        ai_paddle.y -= AI_SPEED

    ai_paddle.y = max(0, min(GAME_HEIGHT - PADDLE_HEIGHT, ai_paddle.y))

    # Ball movement
    ball.x += BALL_SPEED[0]
    ball.y += BALL_SPEED[1]

    # Ball collision with top/bottom walls
    if ball.top <= 0 or ball.bottom >= GAME_HEIGHT:
        BALL_SPEED[1] *= -1

    # Ball collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(ai_paddle):
        BALL_SPEED[0] *= -1

    # Ball out of bounds
    if ball.left <= 0:
        ball.x = GAME_WIDTH / 2 - BALL_SIZE / 2
        ball.y = GAME_HEIGHT / 2 - BALL_SIZE / 2
        BALL_SPEED[0] *= -1
        score[1] += 1
        if score[1] == WINNING_SCORE:
            game_over = True
    elif ball.right >= GAME_WIDTH:
        ball.x = GAME_WIDTH / 2 - BALL_SIZE / 2
        ball.y = GAME_HEIGHT / 2 - BALL_SIZE / 2
        BALL_SPEED[0] *= -1
        score[0] += 1
        if score[0] == WINNING_SCORE:
            game_over = True


    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), player_paddle)
    pygame.draw.rect(screen, (255, 255, 255), ai_paddle)
    pygame.draw.ellipse(screen, (255, 255, 255), ball)
    pygame.draw.aaline(screen, (255, 255, 255), (GAME_WIDTH / 2, 0), (GAME_WIDTH / 2, GAME_HEIGHT))

    player_score = font.render(str(score[0]), True, (255, 255, 255))
    screen.blit(player_score, (GAME_WIDTH / 2 - 50, 20))
    ai_score = font.render(str(score[1]), True, (255, 255, 255))
    screen.blit(ai_score, (GAME_WIDTH / 2 + 25, 20))

    if game_over:
        game_over_text = font.render("Game Over! Restarting...", True, (255, 255, 255))
        screen.blit(game_over_text, (GAME_WIDTH / 2 - 150, GAME_HEIGHT / 2 - 50))
        pygame.display.flip()
        pygame.time.wait(2000)
        score = [0, 0]
        game_over = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()