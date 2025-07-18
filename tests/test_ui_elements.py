"""
Test file for the UI elements implementation
Requirements: 4.1, 4.2 - Basic UI elements implementation test
"""

import sys
import os
# Add the parent directory to sys.path to allow imports from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.game import PuyoPuyoGame
import unittest.mock as mock


class MockPyxel:
    """Pyxel mock for testing"""
    
    def __init__(self):
        self.keys_pressed = set()
        self.keys_just_pressed = set()
        self.quit_called = False
        self.init_called = False
        self.run_called = False
        self.drawn_texts = []  # Record drawn texts
        self.drawn_rects = []  # Record drawn rectangles
        
        # Pyxel constants
        self.KEY_LEFT = 'LEFT'
        self.KEY_RIGHT = 'RIGHT'
        self.KEY_UP = 'UP'
        self.KEY_DOWN = 'DOWN'
        self.KEY_X = 'X'
        self.KEY_Z = 'Z'
        self.KEY_Q = 'Q'
        self.KEY_ESCAPE = 'ESCAPE'
        self.KEY_G = 'G'
        self.KEY_C = 'C'
        self.KEY_E = 'E'
        self.KEY_A = 'A'
        self.KEY_R = 'R'
    
    def init(self, width, height, title):
        self.init_called = True
        self.width = width
        self.height = height
        self.title = title
    
    def run(self, update_func, draw_func):
        self.run_called = True
        self.update_func = update_func
        self.draw_func = draw_func
    
    def btn(self, key):
        return key in self.keys_pressed
    
    def btnp(self, key):
        return key in self.keys_just_pressed
    
    def quit(self):
        self.quit_called = True
    
    def cls(self, color):
        pass
    
    def text(self, x, y, text, color):
        self.drawn_texts.append((x, y, text, color))
    
    def rect(self, x, y, w, h, color):
        self.drawn_rects.append(('rect', x, y, w, h, color))
    
    def rectb(self, x, y, w, h, color):
        self.drawn_rects.append(('rectb', x, y, w, h, color))
    
    def circ(self, x, y, r, color):
        pass
    
    def circb(self, x, y, r, color):
        pass


def test_ui_elements():
    """Test UI elements implementation"""
    print("Starting UI elements test...")
    mock_pyxel = MockPyxel()
    
    with mock.patch('src.game.pyxel', mock_pyxel), \
         mock.patch('src.input_handler.pyxel', mock_pyxel), \
         mock.patch('src.playfield.pyxel', mock_pyxel), \
         mock.patch('src.puyo.pyxel', mock_pyxel):
        
        # Initialize game
        game = PuyoPuyoGame.__new__(PuyoPuyoGame)
        mock_pyxel.init(320, 480, "Puyo Puyo Puzzle Game")
        game.initialize_game()
        
        # Execute draw method
        game.draw()
        
        # Check drawn UI elements
        
        # 1. Playfield frame
        playfield_background = False
        playfield_outer_frame = False
        playfield_inner_frame = False
        
        # 2. Next puyo preview area
        next_preview_background = False
        next_preview_frame = False
        next_label = False
        
        # 3. Score display area
        score_area_background = False
        score_area_frame = False
        score_label = False
        
        # 4. Controls panel
        controls_background = False
        controls_frame = False
        controls_title = False
        
        # 5. Game info panel
        info_background = False
        info_frame = False
        
        # Check drawn rectangles
        for rect_type, x, y, w, h, color in mock_pyxel.drawn_rects:
            # Playfield background (purple)
            if rect_type == 'rect' and w > 140 and h > 280 and color == 5:
                playfield_background = True
            
            # Playfield outer frame (white)
            if rect_type == 'rectb' and w > 140 and h > 280 and color == 7:
                playfield_outer_frame = True
            
            # Playfield inner frame (light purple)
            if rect_type == 'rectb' and w > 140 and h > 280 and color == 13:
                playfield_inner_frame = True
            
            # Next puyo preview area background (dark blue)
            if rect_type == 'rect' and w == 60 and h == 60 and color == 1:
                next_preview_background = True
            
            # Next puyo preview area frame (white)
            if rect_type == 'rectb' and w == 60 and h == 60 and color == 7:
                next_preview_frame = True
            
            # Score display area background (purple)
            if rect_type == 'rect' and w == 60 and h == 60 and color == 5:
                score_area_background = True
            
            # Score display area frame (white)
            if rect_type == 'rectb' and w == 60 and h == 60 and color == 7:
                score_area_frame = True
            
            # Controls panel background (dark blue)
            if rect_type == 'rect' and w == 300 and h == 90 and color == 1:
                controls_background = True
            
            # Controls panel frame (white)
            if rect_type == 'rectb' and w == 300 and h == 90 and color == 7:
                controls_frame = True
            
            # Game info panel background (dark blue)
            if rect_type == 'rect' and w == 70 and h == 60 and color == 1:
                info_background = True
            
            # Game info panel frame (white)
            if rect_type == 'rectb' and w == 70 and h == 60 and color == 7:
                info_frame = True
        
        # Check drawn texts
        for x, y, text, color in mock_pyxel.drawn_texts:
            # "NEXT" label
            if text == "NEXT" and color == 7:
                next_label = True
            
            # "SCORE" label
            if text == "SCORE" and color == 7:
                score_label = True
            
            # "CONTROLS:" title
            if text == "CONTROLS:" and color == 10:
                controls_title = True
        
        # Assert all UI elements are properly drawn
        assert playfield_background, "Playfield background not drawn"
        assert playfield_outer_frame, "Playfield outer frame not drawn"
        assert playfield_inner_frame, "Playfield inner frame not drawn"
        
        assert next_preview_background, "Next puyo preview area background not drawn"
        assert next_preview_frame, "Next puyo preview area frame not drawn"
        assert next_label, "NEXT label not drawn"
        
        assert score_area_background, "Score display area background not drawn"
        assert score_area_frame, "Score display area frame not drawn"
        assert score_label, "SCORE label not drawn"
        
        assert controls_background, "Controls panel background not drawn"
        assert controls_frame, "Controls panel frame not drawn"
        assert controls_title, "CONTROLS title not drawn"
        
        assert info_background, "Game info panel background not drawn"
        assert info_frame, "Game info panel frame not drawn"
        
        print("[OK] All UI elements are properly drawn")


if __name__ == "__main__":
    print("Running UI elements test...")
    try:
        test_ui_elements()
        print("UI elements test passed! [OK]")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()