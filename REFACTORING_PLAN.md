# Game.py Refactoring Plan

## Current Issues
- Single file with 1090+ lines
- Multiple responsibilities in one class
- Hard to maintain and test individual systems
- Violates Single Responsibility Principle

## Proposed Structure

### 1. Core Game Controller (`src/game.py`)
**Responsibilities:** Main game loop, Pyxel integration, system coordination
**Size:** ~200-300 lines
```python
class PuyoPuyoGame:
    def __init__(self)
    def initialize_game(self)
    def update(self)
    def draw(self)
    def restart_game(self)
```

### 2. Game Systems Manager (`src/game_systems.py`)
**Responsibilities:** Coordinate all game systems (fall, elimination, gravity, chain)
**Size:** ~300-400 lines
```python
class GameSystems:
    def __init__(self, playfield, puyo_manager, score_manager, audio_manager)
    def update_fall_system(self)
    def update_elimination_system(self)
    def update_gravity_system(self)
    def update_chain_system(self)
    def handle_puyo_pair_input(self)
```

### 3. UI Renderer (`src/ui_renderer.py`)
**Responsibilities:** All drawing operations and UI layout
**Size:** ~300-400 lines
```python
class UIRenderer:
    def __init__(self, game_state_manager, score_manager, puyo_manager)
    def draw_playfield(self)
    def draw_next_preview(self)
    def draw_score_display(self)
    def draw_controls(self)
    def draw_chain_animation(self)
    def draw_game_over_screen(self)
```

### 4. Game State Controller (`src/game_controller.py`)
**Responsibilities:** Game state transitions and state-specific logic
**Size:** ~200-300 lines
```python
class GameController:
    def __init__(self, game_state_manager)
    def update_state_logic(self)
    def update_menu_logic(self)
    def update_playing_logic(self)
    def update_game_over_logic(self)
    def check_game_over(self)
    def handle_game_over(self)
```

### 5. Debug Tools (`src/debug_tools.py`)
**Responsibilities:** All debug and test functions
**Size:** ~100-200 lines
```python
class DebugTools:
    def __init__(self, playfield, puyo_manager)
    def debug_print(self, message)
    def test_connection_detection(self)
    def test_elimination_process(self)
    def test_chain_animation(self)
```

## Benefits of This Refactoring

### ✅ Improved Maintainability
- Each class has a single, clear responsibility
- Easier to locate and fix bugs
- Simpler to add new features

### ✅ Better Testability
- Individual systems can be tested in isolation
- Mock dependencies more easily
- More focused unit tests

### ✅ Enhanced Readability
- Smaller, more focused files
- Clear separation of concerns
- Better code organization

### ✅ Easier Collaboration
- Multiple developers can work on different systems
- Reduced merge conflicts
- Clear module boundaries

## Implementation Steps ✅ COMPLETED

1. **✅ Create UIRenderer** - Extract all drawing methods (~300 lines)
2. **✅ Create GameSystems** - Extract game logic systems (~400 lines)
3. **✅ Create GameController** - Extract state management (~250 lines)
4. **✅ Create DebugTools** - Extract debug functions (~100 lines)
5. **✅ Refactor main Game class** - Keep only coordination logic (~200 lines)
6. **⏳ Update imports and dependencies** - In progress
7. **⏳ Run tests to ensure functionality** - Next step
8. **⏳ Update documentation** - Next step

## Actual Impact
- **Original game.py**: 1090+ lines
- **Refactored game_refactored.py**: ~200 lines (82% reduction)
- **Total new files**: 5 files created
- **File sizes**: 
  - `ui_renderer.py`: ~300 lines
  - `game_systems.py`: ~400 lines  
  - `game_controller.py`: ~250 lines
  - `debug_tools.py`: ~100 lines
  - `game_refactored.py`: ~200 lines
- **Maintainability**: Significantly improved ✅

## Files Created
- `src/ui_renderer.py` - All UI drawing operations
- `src/game_systems.py` - Game logic (fall, elimination, gravity, chain)
- `src/game_controller.py` - State management and game over logic
- `src/debug_tools.py` - Debug and test functions
- `src/game_refactored.py` - Clean main game class
- `REFACTORING_PLAN.md` - This documentation