import unittest
from unittest.mock import patch
import sys
import pygame
from io import StringIO

from space_invaders import (
    game_over,
    create_enemies,
    create_blue_enemy,
    update_enemy_bullets,
    update_player_bullets,
    update_enemy_shooting,
    update_game_state,
    ENEMY_ROWS,
    ENEMY_BLOCKS,
    ENEMY_COUNT_IN_ROW,
    blue_enemy_list,
    enemy_list,
    player_lives,
    score,
    enemy_bullets,
    player_bullets
)

class TestSpaceInvaders(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_create_enemies(self):
        create_enemies()
        self.assertEqual(len(enemy_list), ENEMY_ROWS * ENEMY_BLOCKS * ENEMY_COUNT_IN_ROW)

    def test_create_blue_enemy(self):
        create_blue_enemy()
        self.assertEqual(len(blue_enemy_list), 1)

    def test_update_enemy_bullets(self):
        enemy_bullets = [[50, 50], [100, 100], [150, 150]]
        updated_bullets = update_enemy_bullets(enemy_bullets, 5, 400)
        self.assertEqual(len(updated_bullets), 3)
        updated_bullets = update_enemy_bullets(enemy_bullets, 5, 60)
        self.assertEqual(len(updated_bullets), 1)

    def test_update_player_bullets(self):
        player_bullets = [[50, 50], [100, 100], [150, 150]]
        updated_bullets = update_player_bullets(player_bullets, 5, 400)
        self.assertEqual(len(updated_bullets), 3)
        updated_bullets = update_player_bullets(player_bullets, 5, 60)
        self.assertEqual(len(updated_bullets), 1)

    def test_update_enemy_shooting(self):
        enemy_list = [[50, 50], [100, 100], [150, 150]]
        enemy_bullets = []
        max_enemy_bullets = 3
        updated_bullets = update_enemy_shooting(enemy_list, enemy_bullets, max_enemy_bullets)
        self.assertLessEqual(len(updated_bullets), max_enemy_bullets)
        updated_bullets = update_enemy_shooting([], enemy_bullets, max_enemy_bullets)
        self.assertEqual(len(updated_bullets), 0)

    def test_update_game_state(self):
        global player_lives, score, enemy_bullets, player_bullets, enemy_list, blue_enemy_list
        initial_lives, initial_score = player_lives, score
        initial_enemy_bullets, initial_player_bullets = list(enemy_bullets), list(player_bullets)
        initial_enemy_list, initial_blue_enemy_list = list(enemy_list), list(blue_enemy_list)

        update_game_state(player_lives, score, enemy_bullets, player_bullets, enemy_list, blue_enemy_list)

        self.assertEqual(player_lives, initial_lives)
        self.assertEqual(score, initial_score)
        self.assertEqual(enemy_bullets, initial_enemy_bullets)
        self.assertEqual(player_bullets, initial_player_bullets)
        self.assertEqual(enemy_list, initial_enemy_list)
        self.assertEqual(blue_enemy_list, initial_blue_enemy_list)

if __name__ == '__main__':
    unittest.main()
