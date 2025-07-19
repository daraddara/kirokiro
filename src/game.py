"""
Refactored Main Game Class - Pyxelアプリケーションの管理のみに集中
Requirements: 1.1, 1.2 - メインゲームループとPyxel統合
"""

import pyxel
from src.playfield import PlayField
from src.input_handler import InputHandler
from src.puyo_manager import PuyoManager
from src.score_manager import ScoreManager
from src.game_state import GameStateManager
from src.audio_manager import AudioManager, BGMType
from src.game_systems import GameSystems
from src.ui_renderer import UIRenderer
from src.game_controller import GameController
from src.debug_tools import DebugTools


class PuyoPuyoGame:
    """
    メインゲームクラス - Pyxelアプリケーションを管理
    Requirements: 1.1, 1.2
    """
    
    def __init__(self):
        """
        Pyxelアプリケーションの初期化
        """
        # 画面サイズの設定（320x380ピクセル - レイアウト最適化）
        pyxel.init(320, 380, title="Puyo Puyo Puzzle Game")
        
        # ゲーム状態の初期化
        self.initialize_game()
        
        # Pyxelアプリケーションの開始
        pyxel.run(self.update, self.draw)
    
    def initialize_game(self):
        """
        ゲームの初期化処理
        各システムの初期化と連携設定
        """
        # フレームカウンター
        self.frame_count = 0
        
        # デバッグモード設定
        self.debug_mode = False
        self.test_puyos = []  # テスト用ぷよ（デバッグモード時のみ使用）
        
        # 基本システムの初期化
        self.playfield = PlayField()
        self.input_handler = InputHandler()
        self.puyo_manager = PuyoManager()
        self.score_manager = ScoreManager()
        self.game_state_manager = GameStateManager()
        self.audio_manager = AudioManager()
        
        # 統合システムの初期化
        self.game_systems = GameSystems(
            self.playfield, self.puyo_manager, self.score_manager, 
            self.audio_manager, self.input_handler
        )
        
        self.ui_renderer = UIRenderer(
            self.game_state_manager, self.score_manager, 
            self.puyo_manager, self.audio_manager
        )
        
        self.game_controller = GameController(
            self.game_state_manager, self.playfield, self.game_systems,
            self.score_manager, self.audio_manager, self.input_handler
        )
        
        self.debug_tools = DebugTools(self.playfield, self.game_systems)
        
        # デバッグモードの同期
        self.game_systems.debug_mode = self.debug_mode
        self.debug_tools.debug_mode = self.debug_mode
        
        # 最初の落下ペアを設定
        self.game_systems.initialize_first_pair()
        
        # 初期化完了フラグを設定
        self.game_systems.is_initializing = False
        
        # ゲーム状態をPLAYINGに設定
        self.game_state_manager.start_game()
        
        # ゲーム開始時のBGM再生
        self.audio_manager.play_bgm(BGMType.GAME)
        
        print("Game initialized with refactored architecture")
    
    def update(self):
        """
        ゲーム状態の更新処理（毎フレーム呼び出される）
        Requirements: 1.1 - システムは対応するゲーム操作を実行する
        """
        # フレームカウンターの更新
        self.frame_count += 1
        
        # 入力処理の更新
        self.input_handler.update()
        
        # 音響システムの更新
        self.audio_manager.update()
        
        # 基本的なキー入力処理
        if self.input_handler.should_quit_game():
            pyxel.quit()
        
        # デバッグ機能（デバッグモード時のみ）
        if self.debug_mode:
            self.handle_debug_input()
        
        # ゲーム状態管理システムの更新
        self.game_state_manager.update()
        
        # ゲーム状態に応じた処理分岐
        self.game_controller.update_state_specific_logic()
        
        # スコア表示システムの更新
        self.game_controller.update_score_display_system()
        
        # ゲームシステムの更新（消去・重力・連鎖）
        self.game_systems.update_elimination_system()
        self.game_systems.update_gravity_system()
        self.game_systems.update_chain_display_system()
        
        # 通常のゲームプレイ処理（システムが非アクティブ時のみ）
        if not self.game_systems.is_systems_active():
            # 落下システムの更新
            self.game_systems.update_fall_system()
            
            # 現在のぷよペアに対する入力処理
            self.game_systems.handle_puyo_pair_input()
    
    def handle_debug_input(self):
        """
        デバッグ用入力処理
        """
        # 重力テスト機能（Gキー）
        if self.input_handler.should_test_gravity():
            self.debug_tools.test_gravity()
        
        # 連結判定テスト機能（Cキー）
        if self.input_handler.should_test_connection():
            self.debug_tools.test_connection_detection()
        
        # 消去処理テスト機能（Eキー）
        if self.input_handler.should_test_elimination():
            self.debug_tools.test_elimination_process()
        
        # 連鎖アニメーションテスト機能（Aキー）
        if self.input_handler.should_test_chain_animation():
            self.debug_tools.test_chain_animation()
    
    def draw(self):
        """
        画面描画処理（毎フレーム呼び出される）
        Requirements: 1.1 - システムはゲーム画面を表示する
        Requirements: 1.2 - システムはプレイフィールドとぷよを表示する
        """
        # 危険レベルを取得
        danger_level = self.game_controller.get_danger_level()
        
        # 背景の描画
        self.ui_renderer.draw_background(self.frame_count, danger_level)
        
        # タイトルの描画
        self.ui_renderer.draw_title()
        
        # プレイフィールドの枠線描画
        self.ui_renderer.draw_playfield_frame()
        
        # プレイフィールドの描画
        self.playfield.draw(self.ui_renderer.playfield_x, self.ui_renderer.playfield_y)
        
        # 危険レベルの視覚的警告表示
        self.ui_renderer.draw_danger_warnings(danger_level, self.frame_count)
        
        # 消去予定のぷよの点滅表示
        elimination_info = self.game_systems.get_elimination_info()
        self.ui_renderer.draw_elimination_effects(*elimination_info)
        
        # デバッグモードの場合のみテスト用ぷよを描画
        if self.debug_mode:
            for i, puyo in enumerate(self.test_puyos):
                screen_x = self.ui_renderer.playfield_x + (i * 24)
                screen_y = self.ui_renderer.playfield_y + 24
                puyo.draw(screen_x, screen_y)
        
        # 現在落下中のぷよペアの描画
        if self.game_systems.current_falling_pair is not None:
            self.game_systems.current_falling_pair.draw(
                self.ui_renderer.playfield_x, self.ui_renderer.playfield_y
            )
        
        # 次のぷよペアのプレビュー表示
        self.ui_renderer.draw_next_preview()
        
        # スコア表示エリア
        score_info = self.game_controller.get_score_display_info()
        self.ui_renderer.draw_score_area(*score_info)
        
        # 連鎖アニメーション表示
        chain_info = self.game_systems.get_chain_display_info()
        self.ui_renderer.draw_chain_animation(*chain_info)
        
        # 操作説明パネルの表示
        self.ui_renderer.draw_controls_panel(self.debug_mode)
        
        # 最終スコア表示
        self.ui_renderer.draw_final_score_display(self.game_controller.show_final_score)
    
    def restart_game(self):
        """
        ゲームを再開始する
        Requirements: 4.3 - ゲーム再開始機能
        """
        # 各システムの状態をリセット
        self.playfield = PlayField()
        self.puyo_manager = PuyoManager()
        self.score_manager = ScoreManager()
        
        # ゲームシステムを再初期化
        self.game_systems = GameSystems(
            self.playfield, self.puyo_manager, self.score_manager, 
            self.audio_manager, self.input_handler
        )
        
        # UIレンダラーを更新
        self.ui_renderer = UIRenderer(
            self.game_state_manager, self.score_manager, 
            self.puyo_manager, self.audio_manager
        )
        
        # ゲームコントローラーを更新
        self.game_controller = GameController(
            self.game_state_manager, self.playfield, self.game_systems,
            self.score_manager, self.audio_manager, self.input_handler
        )
        
        # デバッグツールを更新
        self.debug_tools = DebugTools(self.playfield, self.game_systems)
        
        # デバッグモードの同期
        self.game_systems.debug_mode = self.debug_mode
        self.debug_tools.debug_mode = self.debug_mode
        
        # 最初の落下ペアを設定
        self.game_systems.initialize_first_pair()
        
        # ゲーム開始時のBGM再生
        self.audio_manager.play_bgm(BGMType.GAME)
        
        print("Game restarted")


if __name__ == "__main__":
    # ゲームを開始
    game = PuyoPuyoGame()