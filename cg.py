import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sunrise and Sunset ")

# Colors
sky_color = (25, 25, 112)  # Dark blue
sunrise_color = (255, 255, 0)  # Yellow
sunset_color = (255, 165, 0)  # Orange
ground_color = (34, 139, 34)  # Forest green
cloud_color = (0, 255, 0)  # White
button_color = (70, 130, 180)  # Steel blue
button_hover_color = (100, 149, 237)  # Cornflower blue
text_color = (255, 255, 255)  # White

# Font
font = pygame.font.Font(None, 40)

# Initial sun position
sun_radius = 60
sun_x, sun_y = width // 2, height + sun_radius

# Cloud variables
clouds = []
num_clouds = 10
cloud_radius_range = (20, 50)
cloud_speed = 1

# Function to generate cloud composed of multiple circles
def generate_cloud():
    cloud_radius = random.randint(*cloud_radius_range)
    num_circles = random.randint(3, 6)
    cloud_circles = []
    for _ in range(num_circles):
        offset_x = random.randint(-cloud_radius, cloud_radius)
        offset_y = random.randint(-cloud_radius // 2, cloud_radius // 2)
        radius = random.randint(cloud_radius // 2, cloud_radius)
        cloud_circles.append((offset_x, offset_y, radius))
    return cloud_circles

# Generate initial clouds
def generate_initial_clouds():
    global clouds
    clouds = []
    for i in range(num_clouds):
        cloud_x = i * (width // num_clouds)
        cloud_y = random.randint(0, height // 4)
        cloud_circles = generate_cloud()
        clouds.append((cloud_x, cloud_y, cloud_circles))

# Function to draw a button
def draw_button(text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surface, text_rect)

# Menu functions
def start_game():
    global running, paused
    running = True
    paused = False

def restart_game():
    global sun_y, sunrise, paused
    sun_y = height + sun_radius
    sunrise = True
    paused = False
    generate_initial_clouds()

def pause_game():
    global paused
    paused = not paused

def increase_speed():
    global cloud_speed
    cloud_speed += 1

def decrease_speed():
    global cloud_speed
    if cloud_speed > 1:
        cloud_speed -= 1

def quit_game():
    pygame.quit()
    sys.exit()

# Animation variables
sunrise = True
running = False
paused = False

clock = pygame.time.Clock()

# Main menu loop
menu_running = True
while menu_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw the menu
    screen.fill(sky_color)
    draw_button("Start", width // 2 - 100, height // 2 - 60, 200, 50, button_color, button_hover_color, start_game)
    draw_button("Quit", width // 2 - 100, height // 2 + 10, 200, 50, button_color, button_hover_color, quit_game)
    pygame.display.flip()
    clock.tick(60)

    if running:
        menu_running = False
        generate_initial_clouds()

# Animation loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause_game()

    if not paused:
        # Clear the screen
        screen.fill(sky_color)

        # Draw the ground
        pygame.draw.rect(screen, ground_color, (0, height // 2, width, height // 2))

        # Draw the clouds
        new_clouds = []
        for cloud in clouds:
            cloud_x, cloud_y, cloud_circles = cloud
            for offset_x, offset_y, radius in cloud_circles:
                pygame.draw.circle(screen, cloud_color, (cloud_x + offset_x, cloud_y + offset_y), radius)

            # Update cloud position (simulate movement)
            cloud_x += cloud_speed
            if cloud_x > width + max(cloud_radius_range):
                cloud_x = -max(cloud_radius_range)
                cloud_y = random.randint(0, height // 4)
                cloud_circles = generate_cloud()
            new_clouds.append((cloud_x, cloud_y, cloud_circles))

        clouds = new_clouds

        # Interpolate sun color based on position
        sun_y_normalized = (sun_y - (height // 5)) / (height - (height // 5))
        sun_color = (
            int(sunrise_color[0] + sun_y_normalized * (sunset_color[0] - sunrise_color[0])),
            int(sunrise_color[1] + sun_y_normalized * (sunset_color[1] - sunrise_color[1])),
            int(sunrise_color[2] + sun_y_normalized * (sunset_color[2] - sunrise_color[2])),
        )

        # Draw the sun
        pygame.draw.circle(screen, sun_color, (sun_x, sun_y), sun_radius)

        # Update sun position
        if sunrise:
            sun_y -=1
            if sun_y <= height // 5:
                sunrise = False
        else:
            sun_y += 1
            if sun_y >= height + sun_radius:
                sunrise = True

    # Draw in-game menu buttons
    draw_button("Restart", 10, 10, 150, 50, button_color, button_hover_color, restart_game)
    draw_button("Pause" if not paused else "Resume", 10, 70, 150, 50, button_color, button_hover_color, pause_game)
    draw_button("Speed+", 10, 130, 150, 50, button_color, button_hover_color, increase_speed)
    draw_button("Speed-", 10, 190, 150, 50, button_color, button_hover_color, decrease_speed)
    draw_button("Quit", 10, 250, 150, 50, button_color, button_hover_color, quit_game)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
