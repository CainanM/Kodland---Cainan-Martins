import pgzrun
import math
import random
from pygame.rect import Rect
import os

WIDTH = 800
HEIGHT = 600
TITLE = "KODLAND TEST"
MENU = 0
PLAYING = 1
GAME_OVER = 2
VICTORY = 3
BACKGROUND_COLOR = (0, 127, 255)
PLAYER_COLOR = (30, 180, 50)
ENEMY1_COLOR = (220, 50, 50)
ENEMY2_COLOR = (220, 150, 50)
ENEMY3_COLOR = (180, 50, 220)
PLATFORM_COLOR = (255, 255, 255)
DOOR_COLOR = (128, 0, 0)
TEXT_COLOR = (240, 240, 240)
GRASS_COLOR = (128, 128, 128)
DIRT_COLOR = (0, 0, 0)
BUTTON_COLOR = (255, 255, 255)
BUTTON_HOVER_COLOR = (220, 220, 220)
MENU_BLUE = (10, 10, 60)
GRAVITY = 0.5
JUMP_STRENGTH = 12
PLAYER_SPEED = 5

class AnimatedActor:
    def __init__(self):
        self.animations = {}
        self.current_animation = "idle"
        self.animation_frame = 0
        self.animation_speed = 0.032
        self.animation_counter = 0
        self.facing_right = True
    def add_animation(self, name, frames):
        self.animations[name] = frames
    def set_animation(self, name):
        if name != self.current_animation and name in self.animations:
            self.current_animation = name
            self.animation_frame = 0
    def update_animation(self):
        if self.current_animation in self.animations:
            self.animation_counter += self.animation_speed
            if self.animation_counter >= 1:
                self.animation_counter = 0
                self.animation_frame = (self.animation_frame + 1) % len(self.animations[self.current_animation])
    def get_current_frame(self):
        if self.current_animation in self.animations:
            return self.animations[self.current_animation][self.animation_frame]
        return None

class Player:
    def __init__(self, x, y):
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_jumping = False
        self.on_ground = False
        self.animated_actor = AnimatedActor()
        self.rect = Rect(x, y, 15, 25)
        self.has_sprites = False
        try:
            try:
                Actor("hero_idle_0")
                sprite_exists = True
            except:
                sprite_exists = False
            if sprite_exists:
                self.animated_actor.add_animation("idle", [
                    Actor("hero_idle_0"),
                    Actor("hero_idle_1"),
                    Actor("hero_idle_2"),
                    Actor("hero_idle_3")
                ])
                self.animated_actor.add_animation("run", [
                    Actor("hero_run_0"),
                    Actor("hero_run_1"),
                    Actor("hero_run_2"),
                    Actor("hero_run_3"),
                    Actor("hero_run_4"),
                    Actor("hero_run_5")
                ])
                self.animated_actor.add_animation("run_left", [
                    Actor("hero_run_left_0"),
                    Actor("hero_run_left_1"),
                    Actor("hero_run_left_2"),
                    Actor("hero_run_left_3"),
                    Actor("hero_run_left_4"),
                    Actor("hero_run_left_5")
                ])
                self.animated_actor.add_animation("jump", [
                    Actor("hero_jump_0")
                ])
                for anim_name in self.animated_actor.animations:
                    for frame in self.animated_actor.animations[anim_name]:
                        frame.x = self.rect.x + self.rect.width / 2
                        frame.y = self.rect.y + self.rect.height / 2
                self.has_sprites = True
                print("Sprites do herói carregados com sucesso!")
            else:
                raise Exception("Sprites não encontrados")
        except Exception as e:
            print(f"Sprites do herói não encontrados, usando fallback: {e}")
            self.animated_actor.add_animation("idle", ["idle_frame"])
            self.animated_actor.add_animation("run", ["run_frame1", "run_frame2", "run_frame3"])
            self.animated_actor.add_animation("run_left", ["run_frame1", "run_frame2", "run_frame3"])
            self.animated_actor.add_animation("jump", ["jump_frame"])
    def update(self, platforms):
        self.velocity_y += GRAVITY
        self.rect.x += self.velocity_x
        for platform in platforms:
            platform_rect = platform.rect if hasattr(platform, 'rect') else platform
            if self.rect.colliderect(platform_rect):
                if self.velocity_x > 0:
                    self.rect.right = platform_rect.left
                elif self.velocity_x < 0:
                    self.rect.left = platform_rect.right
        self.rect.y += self.velocity_y
        self.on_ground = False
        for platform in platforms:
            platform_rect = platform.rect if hasattr(platform, 'rect') else platform
            if self.rect.colliderect(platform_rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform_rect.top
                    self.on_ground = True
                    self.is_jumping = False
                    self.velocity_y = 0
                elif self.velocity_y < 0:
                    self.rect.top = platform_rect.bottom
                    self.velocity_y = 0
        if not self.on_ground:
            self.animated_actor.set_animation("jump")
        elif self.velocity_x > 0:
            self.animated_actor.set_animation("run")
        elif self.velocity_x < 0:
            self.animated_actor.set_animation("run_left")
        else:
            self.animated_actor.set_animation("idle")
        if self.velocity_x > 0:
            self.animated_actor.facing_right = True
        elif self.velocity_x < 0:
            self.animated_actor.facing_right = False
        self.animated_actor.update_animation()
        if self.has_sprites:
            current_frame = self.animated_actor.get_current_frame()
            if current_frame:
                current_frame.x = self.rect.x + self.rect.width / 2
                current_frame.y = self.rect.y + self.rect.height / 2
    def move_left(self):
        self.velocity_x = -PLAYER_SPEED
    def move_right(self):
        self.velocity_x = PLAYER_SPEED
    def stop(self):
        self.velocity_x = 0
    def jump(self):
        if self.on_ground:
            self.velocity_y = -JUMP_STRENGTH
            self.is_jumping = True
            self.on_ground = False
            if game.sounds_on:
                sounds.jump.play()
    def draw(self):
        if self.has_sprites:
            current_frame = self.animated_actor.get_current_frame()
            if current_frame:
                current_frame.flip_x = not self.animated_actor.facing_right
                current_frame.draw()
        else:
            screen.draw.filled_rect(self.rect, PLAYER_COLOR)
            eye_x = self.rect.right - 10 if self.animated_actor.facing_right else self.rect.left + 10
            screen.draw.filled_circle((eye_x, self.rect.top + 15), 5, (255, 255, 255))

class Enemy:
    def __init__(self, x, y, width, height, color, enemy_type):
        self.rect = Rect(x, y, width, height)
        self.color = color
        self.enemy_type = enemy_type
        self.animated_actor = AnimatedActor()
        self.has_sprites = False
        self.hitbox_offset_x = 0
        self.hitbox_offset_y = 0
        try:
            if enemy_type == "patrol":
                try:
                    Actor("enemy_patrol_0")
                    patrol_exists = True
                except:
                    patrol_exists = False
                if patrol_exists:
                    self.animated_actor.add_animation("idle", [
                        Actor("enemy_patrol_0"),
                        Actor("enemy_patrol_1"),
                        Actor("enemy_patrol_2")
                    ])
                    self.animated_actor.add_animation("move", [
                        Actor("enemy_patrol_0"),
                        Actor("enemy_patrol_1"),
                        Actor("enemy_patrol_2")
                    ])
                    self.has_sprites = True
                    print(f"Sprites do inimigo {enemy_type} carregados com sucesso!")
                else:
                    raise Exception("Sprites não encontrados")
            elif enemy_type == "jumper":
                try:
                    Actor("enemy_jumper_0")
                    jumper_exists = True
                except:
                    jumper_exists = False
                if jumper_exists:
                    self.animated_actor.add_animation("idle", [
                        Actor("enemy_jumper_0"),
                        Actor("enemy_jumper_1")
                    ])
                    self.animated_actor.add_animation("move", [
                        Actor("enemy_jumper_0"),
                        Actor("enemy_jumper_1")
                    ])
                    self.has_sprites = True
                    print(f"Sprites do inimigo {enemy_type} carregados com sucesso!")
                else:
                    raise Exception("Sprites não encontrados")
            elif enemy_type == "chaser":
                try:
                    Actor("enemy_chaser_0")
                    chaser_exists = True
                except:
                    chaser_exists = False
                if chaser_exists:
                    self.animated_actor.add_animation("idle", [
                        Actor("enemy_chaser_0"),
                        Actor("enemy_chaser_1"),
                        Actor("enemy_chaser_2")
                    ])
                    self.animated_actor.add_animation("move", [
                        Actor("enemy_chaser_0"),
                        Actor("enemy_chaser_1"),
                        Actor("enemy_chaser_2")
                    ])
                    self.has_sprites = True
                    print(f"Sprites do inimigo {enemy_type} carregados com sucesso!")
                else:
                    raise Exception("Sprites não encontrados")
        except Exception as e:
            print(f"Sprites do inimigo {enemy_type} não encontrados, usando fallback: {e}")
            self.animated_actor.add_animation("idle", ["idle_frame"])
            self.animated_actor.add_animation("move", ["move_frame1", "move_frame2"])
        if self.has_sprites:
            for anim_name in self.animated_actor.animations:
                for frame in self.animated_actor.animations[anim_name]:
                    frame.x = self.rect.x + self.rect.width / 2
                    frame.y = self.rect.y + self.rect.height / 2
    def update(self, player, platforms):
        if self.has_sprites:
            current_frame = self.animated_actor.get_current_frame()
            if current_frame:
                current_frame.x = self.rect.x + self.rect.width / 2
                current_frame.y = self.rect.y + self.rect.height / 2
    def draw(self):
        if self.has_sprites:
            current_frame = self.animated_actor.get_current_frame()
            if current_frame:
                current_frame.flip_x = not self.animated_actor.facing_right
                current_frame.draw()
        else:
            screen.draw.filled_rect(self.rect, self.color)
        self.animated_actor.update_animation()

class EnemyPatrol(Enemy):
    def __init__(self, x, y, patrol_distance):
        super().__init__(x, y, 24, 32, ENEMY1_COLOR, "patrol")
        self.start_x = x
        self.patrol_distance = patrol_distance
        self.direction = 1
        self.speed = 2
    def update(self, player, platforms):
        self.rect.x += self.speed * self.direction
        if self.rect.x > self.start_x + self.patrol_distance:
            self.direction = -1
            self.animated_actor.facing_right = False
        elif self.rect.x < self.start_x:
            self.direction = 1
            self.animated_actor.facing_right = True
        if self.speed != 0:
            self.animated_actor.set_animation("move")
        else:
            self.animated_actor.set_animation("idle")
        super().update(player, platforms)

class EnemyJumper(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 24, 32, ENEMY2_COLOR, "jumper")
        self.jump_timer = 0
        self.jump_interval = 120
        self.on_ground = False
        self.hitbox_offset_x = 3
        self.hitbox_offset_y = 4
        self.velocity_y = 0
    def update(self, player, platforms):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        self.on_ground = False
        for platform in platforms:
            platform_rect = platform.rect if hasattr(platform, 'rect') else platform
            if self.rect.colliderect(platform_rect):
                if self.velocity_y > 0 and self.rect.bottom > platform_rect.top and self.rect.top < platform_rect.top:
                    self.rect.bottom = platform_rect.top
                    self.on_ground = True
                    self.velocity_y = 0
                elif self.velocity_y < 0 and self.rect.top < platform_rect.bottom and self.rect.bottom > platform_rect.bottom:
                    self.rect.top = platform_rect.bottom
                    self.velocity_y = 0
        self.jump_timer += 1
        if self.jump_timer >= self.jump_interval and self.on_ground:
            self.velocity_y = -JUMP_STRENGTH + 2
            self.on_ground = False
            self.jump_timer = 0
        if not self.on_ground:
            self.animated_actor.set_animation("move")
        else:
            self.animated_actor.set_animation("idle")
        if self.has_sprites:
            current_frame = self.animated_actor.get_current_frame()
            if current_frame:
                current_frame.x = self.rect.x + self.rect.width / 2 + self.hitbox_offset_x
                current_frame.y = self.rect.y + self.rect.height / 2 + self.hitbox_offset_y
        self.animated_actor.update_animation()

class EnemyChaser(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 24, 32, ENEMY3_COLOR, "chaser")
        self.speed = 1.5
        self.chase_range = 90
    def update(self, player, platforms):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        distance = math.sqrt(dx*dx + dy*dy)
        if distance < self.chase_range:
            if dx > 0:
                self.rect.x += self.speed
                self.animated_actor.facing_right = True
            else:
                self.rect.x -= self.speed
                self.animated_actor.facing_right = False
            self.animated_actor.set_animation("move")
        else:
            self.animated_actor.set_animation("idle")
        super().update(player, platforms)

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)
    def draw(self):
        screen.draw.filled_rect(self.rect, PLATFORM_COLOR)

class Door:
    def __init__(self, x, y):
        self.rect = Rect(x, y, 40, 60)
        self.has_sprite = False
        self.sprite = None
        try:
            temp_sprite = Actor("door")
            visual_height = self.rect.height * 1.5
            temp_sprite.height = visual_height
            self.sprite = temp_sprite
            self.sprite.midbottom = self.rect.midbottom
            self.has_sprite = True
            print("Sprite da porta carregado com sucesso!")
        except Exception as e:
            print(f"Sprite 'door.png' não encontrado, usando fallback de retângulo: {e}")
    def draw(self):
        if self.has_sprite and self.sprite:
            self.sprite.draw()
        else:
            screen.draw.filled_rect(self.rect, DOOR_COLOR)
            screen.draw.rect(self.rect, (220, 220, 100))

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
    def draw(self):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        screen.draw.filled_rect(self.rect, color)
        screen.draw.rect(self.rect, MENU_BLUE)
        screen.draw.text(
            self.text, 
            center=(self.rect.centerx, self.rect.centery),
            color=MENU_BLUE,
            fontsize=30,
            fontname="upheaval"
        )
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
    def check_click(self, pos):
        return self.rect.collidepoint(pos)

class Game:
    def __init__(self):
        self.state = MENU
        self.music_on = True
        self.sounds_on = True
        self.setup_menu()
        try:
            music.set_volume(0.4)
            music.play('background')
        except Exception as e:
            print(f"Não foi possível tocar a música de fundo: {e}")
    def setup_menu(self):
        center_x = WIDTH // 2
        self.menu_buttons = [
            Button(center_x - 100, 200, 200, 50, "Start Game", self.start_game),
            Button(center_x - 100, 270, 200, 50, "Music: On", self.toggle_music),
            Button(center_x - 100, 340, 200, 50, "Sounds: On", self.toggle_sounds),
            Button(center_x - 100, 410, 200, 50, "Exit", self.exit_game)
        ]
        self.game_over_buttons = [
            Button(center_x - 100, 300, 200, 50, "Try Again", self.start_game),
            Button(center_x - 100, 370, 200, 50, "Exit", self.go_to_menu)
        ]
        self.menu_hero = Player(150, HEIGHT - 80)
        self.menu_hero.velocity_x = 2
        self.menu_hero.on_ground = True
    def start_game(self):
        self.state = PLAYING
        self.setup_level_1()
        volume_efeitos = 0.5
        try:
            sounds.jump.set_volume(volume_efeitos)
            sounds.death.set_volume(volume_efeitos)
        except:
            print("Arquivos de som não encontrados para ajustar o volume.")
        if self.music_on and not music.is_playing('background'):
            music.play('background')
    def go_to_menu(self):
        self.state = MENU
        if self.music_on and not music.is_playing('background'):
            music.play('background')
    def toggle_music(self):
        self.music_on = not self.music_on
        self.menu_buttons[1].text = "Music: On" if self.music_on else "Music: Off"
        if self.music_on:
            music.unpause()
        else:
            music.pause()
    def toggle_sounds(self):
        self.sounds_on = not self.sounds_on
        self.menu_buttons[2].text = "Sounds: On" if self.sounds_on else "Sounds: Off"
    def exit_game(self):
        exit()
    def setup_level_1(self):
        self.player = Player(100, 300)
        self.platforms = [
            Platform(0, 550, 800, 50),
            Platform(-10, 0, 10, 600),
            Platform(800, 0, 10, 600),
            Platform(200, 450, 150, 20),
            Platform(400, 380, 150, 20),
            Platform(550, 290, 150, 20)
        ]
        self.enemies = [
            EnemyPatrol(300, 410, 100),
            EnemyJumper(450, 330),
            EnemyChaser(600, 520)
        ]
        self.door = Door(700, 516)
    def update(self):
        if self.state == MENU:
            self.menu_hero.rect.x += self.menu_hero.velocity_x
            if self.menu_hero.rect.left < 150 or self.menu_hero.rect.right > WIDTH - 150:
                self.menu_hero.velocity_x *= -1
            if self.menu_hero.velocity_x > 0:
                self.menu_hero.animated_actor.set_animation("run")
                self.menu_hero.animated_actor.facing_right = True
            else:
                self.menu_hero.animated_actor.set_animation("run_left")
                self.menu_hero.animated_actor.facing_right = False
            self.menu_hero.animated_actor.update_animation()
            if self.menu_hero.has_sprites:
                current_frame = self.menu_hero.animated_actor.get_current_frame()
                if current_frame:
                    current_frame.center = self.menu_hero.rect.center
        if self.state == PLAYING:
            self.player.update(self.platforms)
            for enemy in self.enemies:
                enemy.update(self.player, self.platforms)
                if self.player.rect.colliderect(enemy.rect):
                    if self.sounds_on:
                        sounds.death.play()
                    self.state = GAME_OVER
                    return 
            if self.player.rect.colliderect(self.door.rect):
                self.state = VICTORY
    def draw(self):
        if self.state == MENU:
            screen.fill(MENU_BLUE)
            self.draw_menu()
        else:
            screen.blit('background', (0, 0))
            if self.state == PLAYING:
                self.draw_level()
            elif self.state == GAME_OVER:
                self.draw_level()
                screen.draw.text(
                    "GAME OVER", 
                    center=(WIDTH//2, HEIGHT//2 - 100),
                    color=(220, 50, 50),
                    fontsize=48
                )
                for button in self.game_over_buttons:
                    button.draw()
            elif self.state == VICTORY:
                self.draw_level()
                screen.draw.text(
                    "VICTORY!", 
                    center=(WIDTH//2, HEIGHT//2),
                    color="yellow",
                    fontsize=80,
                    fontname="upheaval"
                )
    def draw_menu(self):
        screen.draw.text(
            "KODLAND TEST", 
            center=(WIDTH//2, 100),
            color=TEXT_COLOR,
            fontsize=60,
            fontname="upheaval"
        )
        for button in self.menu_buttons:
            button.draw()
        screen.draw.filled_rect(Rect(0, HEIGHT - 50, WIDTH, 50), MENU_BLUE)
        self.menu_hero.draw()
    def draw_level(self):
        self.draw_ground()
        for platform in self.platforms[1:]:
            platform.draw()
        self.door.draw()
        for enemy in self.enemies:
            enemy.draw()
        self.player.draw()
    def draw_ground(self):
        screen.draw.filled_rect(Rect(0, 550, 800, 50), DIRT_COLOR)
        screen.draw.filled_rect(Rect(0, 550, 800, 10), GRASS_COLOR)
    def on_mouse_move(self, pos):
        if self.state == MENU:
            for button in self.menu_buttons:
                button.check_hover(pos)
        elif self.state == GAME_OVER:
            for button in self.game_over_buttons:
                button.check_hover(pos)
    def on_mouse_down(self, pos):
        if self.state == MENU:
            for button in self.menu_buttons:
                if button.check_click(pos):
                    button.action()
        elif self.state == GAME_OVER:
            for button in self.game_over_buttons:
                if button.check_click(pos):
                    button.action()
        elif self.state == VICTORY:
            self.go_to_menu()

game = Game()

def update():
    game.update()

def draw():
    game.draw()

def on_mouse_move(pos):
    game.on_mouse_move(pos)

def on_mouse_down(pos):
    game.on_mouse_down(pos)

def on_key_down(key):
    if game.state == PLAYING:
        if key == keys.SPACE:
            game.player.jump()
        elif key == keys.LEFT or key == keys.A:
            game.player.move_left()
        elif key == keys.RIGHT or key == keys.D:
            game.player.move_right()

def on_key_up(key):
    if game.state == PLAYING:
        if (key == keys.LEFT or key == keys.A) and game.player.velocity_x < 0:
            game.player.stop()
        elif (key == keys.RIGHT or key == keys.D) and game.player.velocity_x > 0:
            game.player.stop()

pgzrun.go()