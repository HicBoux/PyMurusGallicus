import unittest
import pygame
from src.murus_gallicus.ui import UIRender
from src.murus_gallicus.constants import SPQR_RED, CELTIC_GREEN, ICON_PATH

class TestUI(unittest.TestCase):
    """Class of Unit Tests to check bugs in the UI Class."""

    image_path = ICON_PATH

    def test_if_ui_instance_well_initialized(self):
        """Test if the attributes of UIRender are well initialized."""
        ui = UIRender(TestUI.image_path)
        self.assertEqual(ui.run, True)
        self.assertIsInstance(ui.clock, type(pygame.time.Clock()))
        self.assertEqual(ui.game_mode, "UNKNOWN")
        self.assertEqual(ui.bottom_player_color, 0)
        self.assertEqual(ui.top_player_color, 0)


    def test_if_bottom_color_player_well_set(self):
        """Test if the UI has the right player colors when set_bottom_player_color() are called."""
        ui = UIRender(TestUI.image_path)
        ui.set_bottom_player_color(CELTIC_GREEN)
        self.assertEqual(ui.bottom_player_color, CELTIC_GREEN)
        self.assertEqual(ui.top_player_color, SPQR_RED)
        ui.set_bottom_player_color(SPQR_RED)
        self.assertEqual(ui.bottom_player_color, SPQR_RED)
        self.assertEqual(ui.top_player_color, CELTIC_GREEN)

    def test_if_row_col_well_retrieved_from_mouse_pos(self):
        """Test if the row/column of the board_grid are well deduced from the mouse position on the screen."""
        ui = UIRender(TestUI.image_path)
        row, col = ui.get_row_col_from_mouse((10,25))
        self.assertEqual(row, 0)
        self.assertEqual(col, 0)

if __name__ == '__main__':
    unittest.main()
