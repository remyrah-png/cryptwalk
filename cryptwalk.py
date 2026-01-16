import sys
import os

from scripts.battle import SCREEN_WIDTH, SCREEN_HEIGHT
sys.path.append("..")  # For imports if needed

import pygame
# Game constants
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)
DARK_GRAY = (30, 30, 30)
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Dict
from pygame.math import Vector2

# Import user's modules (adjust paths if needed)
from player import Player
from enemies import create_enemy
from entity import CombatEntity
from combat import (
    attack, apply_defend, apply_poison, apply_taunt,
    process_effects, calculate_damage, is_alive
)
from items import healing_potion, iron_sword, leather_armor  # For future inv
import random
from random import choice


class GameState(Enum):
    OVERWORLD = 1
    COMBAT_POPUP = 2
    INVENTORY_POPUP = 3  # Bonus: Quick inv access

@dataclass
class Tween:
    start_pos: Vector2
    end_pos: Vector2
    start_scale: float
    end_scale: float
    duration: int  # frames
    progress: int = 0
    rotation: float = 0.0  # Total rotation

    def update(self) -> bool:
        self.progress += 1
        if self.progress >= self.duration:
            self.progress = self.duration
            t = 1.0
        else:
            t = self.progress / self.duration
        t_eased = 1 - (1 - t) ** 2  # Ease-out
        # rotation reflects current eased progress (0..360)
        self.rotation = 360 * t_eased
        return self.progress >= self.duration

class JumpSprite:
    def __init__(self, pos: Vector2, color: tuple, size: int = 32, image_path: Optional[str] = None):
        self.pos = pos.copy()
        self.target_pos = pos.copy()
        self.color = color
        self.size = size
        self.tween: Optional[Tween] = None
        self.scale = 1.0
        self.rotation = 0.0
        self.image = None
        if image_path and os.path.exists(image_path):
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (size, size))
        self.surface = pygame.Surface((size, size))
        self.surface.fill(color)  # Fallback rect

    def start_jump(self, end_pos: Vector2, duration: int = 30):
        self.tween = Tween(self.pos.copy(), end_pos, self.scale, 1.2, duration)
        self.target_pos = end_pos

    def update(self):
        if self.tween:
            done = self.tween.update()
            t = self.tween.progress / self.tween.duration
            # Interpolate position and scale manually
            self.pos = self.tween.start_pos + (self.tween.end_pos - self.tween.start_pos) * t
            self.scale = self.tween.start_scale + (self.tween.end_scale - self.tween.start_scale) * t
            # Tween.rotation is the current rotation for this progress
            self.rotation = self.tween.rotation
            if done:
                # finalize to exact end state
                self.pos = self.tween.end_pos.copy()
                self.scale = self.tween.end_scale
                self.rotation = self.tween.rotation
                self.tween = None

    def draw(self, screen: pygame.Surface, arena_offset: Vector2 = Vector2(0,0)):
        draw_pos = self.pos + arena_offset
        scaled_size = int(self.size * self.scale)
        if self.image:
            rotated = pygame.transform.rotozoom(self.image, self.rotation, self.scale)
            rect = rotated.get_rect(center=draw_pos)
            screen.blit(rotated, rect)
        else:
            rect = pygame.Rect(draw_pos.x - scaled_size//2, draw_pos.y - scaled_size//2, scaled_size, scaled_size)
            pygame.draw.rect(screen, self.color, rect)
            if self.tween:
                # Spin indicator
                spin_end = draw_pos + Vector2(scaled_size//2, 0).rotate(self.rotation)
                pygame.draw.line(screen, WHITE, draw_pos, spin_end, 3)

class Game:
    def __init__(self):
        self.font_large = pygame.font.SysFont('arial', 36)
        self.font_med = pygame.font.SysFont('arial', 24)
        self.font_small = pygame.font.SysFont('arial', 18)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cryptwalk: Popup Dungeon Crawler")
        self.clock = pygame.time.Clock()
        self.state = GameState.OVERWORLD
        
        # Use user's game structure!
        self.game_data = {
            "turn": 1,
            "combat_log": [],
            "active_turn": "player",
            "running": True,
            "player": Player(),
            "world": {
                "depth": 0,
                "current_room": {
                    "name": "Crypt Entrance",
                    "desc": "Cold air spills from a cracked stone doorway. The adventure begins."
                }
            },
            "enemy": None,
        }
        self.player = self.game_data["player"]
        self.player_sprite = JumpSprite(Vector2(100, 300), BLUE, 48)  # Hero blue
        self.player_hp_bar = Vector2(150, SCREEN_HEIGHT - 100)  # Fixed HUD pos

        self.current_enemy: Optional[CombatEntity] = None
        self.enemies: List[CombatEntity] = []
        self.enemy_sprites: Dict[str, JumpSprite] = {}
        self.spawn_test_enemy()

        self.popup_alpha = 0
        self.buttons: List[pygame.Rect] = []
        self.button_texts = ["ATTACK", "DEFEND", "POISON", "TAUNT"]
        self.selected_button = -1
        self.goblin_image = None

        # Room gen words (from cryptwalk.py)
        self.adjectives = ["Dark", "Forgotten", "Cursed", "Ancient"]
        self.nouns = ["Crypt", "Tomb", "Gallery"]

    def spawn_test_enemy(self):
        enemy_type = random.choice(["goblin", "skeleton", "orc"])
        enemy = create_enemy(enemy_type)
        pos = Vector2(600 + random.randint(-50, 50), 300 + random.randint(-50, 50))
        sprite_path = f"assets/{enemy_type}.png"
        color = GREEN if enemy_type == "goblin" else YELLOW if enemy_type == "skeleton" else RED
        sprite = JumpSprite(pos, color, 64, sprite_path)
        self.enemies.append(enemy)
        self.enemy_sprites[enemy.name] = sprite  # Key by name for now

    def handle_input(self):
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        if self.state == GameState.OVERWORLD:
            speed = 4
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: self.player_sprite.pos.x -= speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.player_sprite.pos.x += speed
            if keys[pygame.K_UP] or keys[pygame.K_w]: self.player_sprite.pos.y -= speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]: self.player_sprite.pos.y += speed
            if keys[pygame.K_i]: self.state = GameState.INVENTORY_POPUP
            # Bounds
            self.player_sprite.pos.x = max(0, min(self.player_sprite.pos.x, SCREEN_WIDTH))
            self.player_sprite.pos.y = max(0, min(self.player_sprite.pos.y, SCREEN_HEIGHT))

        if keys[pygame.K_ESCAPE]:
            if self.state != GameState.OVERWORLD:
                self.state = GameState.OVERWORLD
                self.popup_alpha = 0

        # Click buttons in popups
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_data["running"] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == GameState.COMBAT_POPUP:
                    for i, btn in enumerate(self.buttons):
                        if btn.collidepoint(mouse_pos):
                            self.handle_combat_action(i)
                            return

    def handle_combat_action(self, action_idx: int):
        # Use a stable 'enemy' key inside game_data for combat operations
        enemy_key = "enemy"
        player_key = "player"
        if self.current_enemy:
            self.game_data["enemy"] = self.current_enemy

        if action_idx == 0:  # Attack
            attack(self.game_data, player_key, enemy_key)
        elif action_idx == 1:  # Defend
            apply_defend(self.player)
            self.game_data["combat_log"].append("You brace for impact!")
        elif action_idx == 2:  # Poison
            apply_poison(self.current_enemy, dmg_per_turn=2, turns=3, game=self.game_data)
        elif action_idx == 3:  # Taunt (self for demo)
            apply_taunt(self.player, dmg_reduction=-3, turns=1, game=self.game_data)

        # Process effects
        process_effects(self.game_data, player_key)
        if self.current_enemy and is_alive(self.current_enemy):
            process_effects(self.game_data, enemy_key)

        # Enemy turn if alive
        if self.current_enemy and is_alive(self.current_enemy):
            attack(self.game_data, enemy_key, player_key)

        # Check win/lose
        if not self.current_enemy or not is_alive(self.current_enemy):
            self.game_data["combat_log"].append("Enemy defeated!")
            self.state = GameState.OVERWORLD
            self.current_enemy = None
            self.game_data["enemy"] = None
        elif not is_alive(self.player):
            self.game_data["combat_log"].append("You died!")
            self.state = GameState.OVERWORLD

    def update(self):
        self.player_sprite.update()
        for sprite in self.enemy_sprites.values():
            sprite.update()

        # Collision -> Jump to combat
        if self.state == GameState.OVERWORLD:
            for enemy in self.enemies:
                sprite = self.enemy_sprites.get(enemy.name)
                if sprite and self.player_sprite.pos.distance_to(sprite.pos) < 60:
                    self.current_enemy = enemy
                    # also set the active enemy in the game data for combat functions
                    self.game_data["enemy"] = enemy
                    # JUMP enemy to arena!
                    arena_pos = Vector2(SCREEN_WIDTH - 200, SCREEN_HEIGHT // 2)
                    sprite.start_jump(arena_pos, 45)
                    # Player jumps to left arena
                    self.player_sprite.start_jump(Vector2(200, SCREEN_HEIGHT // 2), 45)
                    self.state = GameState.COMBAT_POPUP
                    self.popup_alpha = 0
                    break

        if self.state != GameState.OVERWORLD:
            self.popup_alpha = min(255, self.popup_alpha + 8)

    def draw_overworld(self):
        self.screen.fill(DARK_GRAY)
        # Room walls
        pygame.draw.rect(self.screen, BLACK, (0, 0, SCREEN_WIDTH, 80))
        pygame.draw.rect(self.screen, BLACK, (0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80))
        # Depth label
        depth_text = self.font_med.render(f"Depth: {self.game_data['world']['depth']}", True, WHITE)
        self.screen.blit(depth_text, (10, 10))

        # Player & enemies
        self.player_sprite.draw(self.screen)
        for enemy in self.enemies:
            sprite = self.enemy_sprites.get(enemy.name)
            if sprite:
                sprite.draw(self.screen)
                # Mini HP
                hp_ratio = enemy.stats["hp"] / enemy.stats["max_hp"]
                bar_w = 40
                pygame.draw.rect(self.screen, RED, (sprite.pos.x - 20, sprite.pos.y - 50, bar_w, 4))
                pygame.draw.rect(self.screen, GREEN, (sprite.pos.x - 20, sprite.pos.y - 50, bar_w * hp_ratio, 4))

        # Player HUD (fixed)
        p_hp_ratio = self.player.stats["hp"] / self.player.stats["max_hp"]
        pygame.draw.rect(self.screen, RED, (self.player_hp_bar.x, self.player_hp_bar.y, 200, 20))
        pygame.draw.rect(self.screen, GREEN, (self.player_hp_bar.x, self.player_hp_bar.y, 200 * p_hp_ratio, 20))
        hp_text = self.font_small.render(f"HP: {int(self.player.stats['hp'])}/{self.player.stats['max_hp']}", True, WHITE)
        self.screen.blit(hp_text, (self.player_hp_bar.x, self.player_hp_bar.y + 25))

    def draw_popup_overlay(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
        overlay.fill((0, 0, 0, self.popup_alpha // 3))
        self.screen.blit(overlay, (0, 0))

    def draw_combat_popup(self):
        self.enemy_frames = []
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_rate = 100  # ms per frame
        self.player_image = None
        # Lazy-load goblin sprite (safe: attribute set in __init__)
        if getattr(self, "goblin_image", None) is None:
            try:
                self.goblin_image = pygame.image.load('assets/goblin.png')
                self.goblin_image = pygame.transform.scale(self.goblin_image, (200, 200))
            except Exception as e:
                print(f"Sprite load error: {e} - Check assets/goblin.png")
                self.goblin_image = None  # Fallback

        popup_rect = pygame.Rect(100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
        pygame.draw.rect(self.screen, DARK_GRAY, popup_rect)
        pygame.draw.rect(self.screen, WHITE, popup_rect, 5)

        # Draw sprite if loaded
        if self.goblin_image:
            self.screen.blit(self.goblin_image, (popup_rect.centerx - 100, popup_rect.y + 50))
        else:
            no_img_text = self.font_med.render("No sprite loaded", True, RED)
            self.screen.blit(no_img_text, (popup_rect.centerx - no_img_text.get_width()//2, popup_rect.y + 50))

        # Enemy name (prefer active enemy)
        enemy = self.game_data.get("enemy") or self.current_enemy
        enemy_name = enemy.name if enemy else "Enemy"
        title = self.font_large.render(enemy_name, True, WHITE)
        self.screen.blit(title, (popup_rect.centerx - title.get_width()//2, popup_rect.y + 10))

        # HP bar (if enemy present)
        if enemy:
            hp_bar_width = 400
            hp_bar_height = 40
            hp_ratio = enemy.stats["hp"] / enemy.stats["max_hp"]
            hp_bar_x = popup_rect.centerx - hp_bar_width // 2
            hp_bar_y = popup_rect.bottom - 100
            pygame.draw.rect(self.screen, RED, (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height))
            pygame.draw.rect(self.screen, GREEN, (hp_bar_x, hp_bar_y, hp_bar_width * hp_ratio, hp_bar_height))

            hp_text = self.font_med.render(f"HP: {enemy.stats['hp']}/{enemy.stats['max_hp']}", True, WHITE)
            self.screen.blit(hp_text, (hp_bar_x, hp_bar_y + hp_bar_height + 10))

        # Action menu (bottom)
        actions = self.font_med.render("1) Attack 2) Defend 3) Poison 4) Taunt", True, WHITE)
        self.screen.blit(actions, (popup_rect.x + 20, popup_rect.bottom - 50))

    def draw_inventory_popup(self):
        # Simple inv popup (expand later)
        inv_rect = pygame.Rect(200, 150, 400, 300)
        pygame.draw.rect(self.screen, WHITE, inv_rect, 5)
        title = self.font_large.render("INVENTORY", True, WHITE)
        self.screen.blit(title, (inv_rect.centerx - title.get_width()//2, 170))

        # List items (placeholder)
        y_off = 220
        for i, item in enumerate(self.player.inventory):
            item_text = self.font_med.render(f"{item.name} (+{item.value})", True, WHITE)
            self.screen.blit(item_text, (220, y_off + i * 35))

    def draw(self):
        if self.state == GameState.OVERWORLD:
            self.draw_overworld()
        else:
            self.draw_overworld()  # Dim background
            self.draw_popup_overlay()
            if self.state == GameState.COMBAT_POPUP:
                self.draw_combat_popup()
            elif self.state == GameState.INVENTORY_POPUP:
                self.draw_inventory_popup()

    def run(self):
        running = True
        while running and self.game_data["running"]:
            self.handle_input()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()