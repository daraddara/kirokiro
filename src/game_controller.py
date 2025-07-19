"""
Game Controller - ゲーム状態制御とゲームオーバー判定
Requirements: 4.3, 4.4 - ゲーム状態管理とゲームオーバー処理
"""

import pyxel
from src.game_state import GameState
from src.audio_manager import BGMType


class GameController:
    """
    ゲーム制御システム - 状態遷移とゲームオーバー判定を管理
    """
    
    def __init__(self, game_state_manager, playfield, game_systems, score_manager, audio_manager, input_handler):
        """
        GameControllerの初期化
        
        Args:
            game_state_manager: ゲーム状態管理システム
            playfield: プレイフィールド
            game_systems: ゲームシステム管理
            score_manager: スコア管理システム
            audio_manager: 音響管理システム
            input_handler: 入力処理システム
        """
        self.game_state_manager = game_state_manager
        self.playfield = playfield
        self.game_systems = game_systems
        self.score_manager = score_manager
        self.audio_manager = audio_manager
        self.input_handler = input_handler
        
        # ゲームオーバー関連
        self.game_over_reason = ""
        self.show_final_score = False
        
        # スコア表示システム
        self.score_animation_active = False
        self.score_animation_timer = 0
        self.score_animation_phase = 0.0
        self.last_displayed_score = 0
        self.score_increment_amount = 0
    
    def update_state_specific_logic(self):
        """
        ゲーム状態に応じた処理分岐
        Requirements: 4.3, 4.4 - 各状態での処理分岐
        """
        current_state = self.game_state_manager.get_current_state()
        
        if current_state == GameState.MENU:
            self.update_menu_logic()
        elif current_state == GameState.PLAYING:
            self.update_playing_logic()
        elif current_state == GameState.GAME_OVER:
            self.update_game_over_logic()
    
    def update_menu_logic(self):
        """
        メニュー状態での処理
        Requirements: 4.3 - メニュー状態の処理
        """
        # メニュー状態での入力処理
        if self.input_handler.should_start_game():
            # ゲーム開始
            self.game_state_manager.start_game()
        
        if self.input_handler.should_quit_game():
            # ゲーム終了
            pyxel.quit()
        
        # メニュー状態でのBGM再生
        if not self.audio_manager.is_bgm_playing():
            self.audio_manager.play_bgm(BGMType.MENU)
        
        # エンターキーまたはスペースキーでゲーム開始
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            self.game_state_manager.start_game()
    
    def update_playing_logic(self):
        """
        プレイ中状態での処理
        Requirements: 4.3 - プレイ中状態の処理とゲームオーバー判定
        """
        # ゲームオーバー判定
        is_game_over, reason = self.check_game_over_advanced()
        
        if is_game_over:
            # ゲームオーバー処理
            self.handle_game_over(reason)
            return
        
        # プレイ中のBGM再生
        if not self.audio_manager.is_bgm_playing():
            self.audio_manager.play_bgm(BGMType.GAME)
        
        # リスタート処理
        if self.input_handler.should_restart_game():
            self.restart_game()
        
        # ここでは追加のチェックは不要
    
    def update_game_over_logic(self):
        """
        ゲームオーバー状態での処理
        Requirements: 4.3 - ゲームオーバー状態の処理
        """
        # ゲームオーバー状態でのBGM停止
        if self.audio_manager.is_bgm_playing():
            self.audio_manager.stop_bgm()
        
        # リスタート処理
        if self.input_handler.should_restart_game():
            self.restart_game()
        
        # メニューに戻る処理
        if self.input_handler.should_quit_game():
            self.game_state_manager.return_to_menu()
    
    def check_game_over(self):
        """
        ゲームオーバー判定
        Requirements: 4.3, 4.4 - ゲームオーバー判定と最終スコア表示
        
        Returns:
            bool: ゲームオーバーの場合True
        """
        # プレイフィールドの上端（y=0）にぷよがある場合はゲームオーバー
        for x in range(6):
            if not self.playfield.is_empty(x, 0):
                return True
        return False
    
    def check_game_over_advanced(self):
        """
        高度なゲームオーバー判定
        Requirements: 4.3, 4.4 - より詳細なゲームオーバー判定
        
        Returns:
            tuple: (is_game_over: bool, reason: str)
        """
        from src.debug_utils import print_playfield_state, analyze_game_over_state
        
        # 基本的な上端到達判定
        for x in range(6):
            if not self.playfield.is_empty(x, 0):
                print("\n*** ゲームオーバー検出: 上端到達 ***")
                analyze_game_over_state(self)
                print_playfield_state(self.playfield, self.game_systems.current_falling_pair)
                return True, f"プレイフィールド上端到達 (列 {x})"
        
        # 新しいぷよペアが配置できない場合の判定
        if self.game_systems.current_falling_pair is not None:
            # 現在のぷよペアの位置を取得
            main_pos, sub_pos = self.game_systems.current_falling_pair.get_puyo_positions()
            
            # 初期位置（メインぷよのY座標が0）の場合のみチェック
            if main_pos[1] == 0:
                # 現在の位置に既にぷよがあるかチェック
                main_empty = self.playfield.is_empty(main_pos[0], main_pos[1])
                sub_empty = self.playfield.is_empty(sub_pos[0], sub_pos[1])
                
                if not main_empty or not sub_empty:
                    print("\n*** ゲームオーバー検出: 新しいぷよペアが配置不可能 ***")
                    print(f"メインぷよ位置 {main_pos} は空か: {main_empty}")
                    print(f"サブぷよ位置 {sub_pos} は空か: {sub_empty}")
                    analyze_game_over_state(self)
                    print_playfield_state(self.playfield, self.game_systems.current_falling_pair)
                    return True, "新しいぷよペアが配置不可能"
        
        # 危険レベルの判定（上から3行以内にぷよがある場合）
        danger_level = self.get_danger_level()
        if danger_level >= 3:
            # 危険レベルが高い場合の警告（ゲームオーバーではない）
            return False, f"危険レベル: {danger_level} - 上部にぷよが積まれています"
        
        # 正常状態
        return False, "正常"
    
    def get_danger_level(self):
        """
        危険レベルを取得する（上部にどれだけぷよが積まれているか）
        Requirements: 4.3, 4.4 - ゲームオーバー警告の判定
        
        Returns:
            int: 危険レベル（0-6、上から3行以内のぷよの数）
        """
        danger_count = 0
        for y in range(3):  # 上から3行をチェック
            for x in range(6):
                if not self.playfield.is_empty(x, y):
                    danger_count += 1
        return danger_count
    
    def handle_game_over(self, reason="ゲームオーバー"):
        """
        ゲームオーバー処理
        Requirements: 4.3, 4.4 - ゲームオーバー処理と最終スコア表示
        
        Args:
            reason (str): ゲームオーバーの理由
        """
        # ゲーム状態をゲームオーバーに変更
        self.game_state_manager.game_over()
        
        # ゲームオーバーの理由を記録
        self.game_over_reason = reason
        
        # 最終スコア表示を有効化
        self.show_final_score_screen()
        
        # ゲームオーバー音を再生
        self.audio_manager.stop_bgm()
        # self.audio_manager.play_sound(SoundType.GAME_OVER)  # 実装時にコメントアウト解除
        
        # デバッグ出力
        print(f"\n=== GAME OVER ===")
        print(f"理由: {reason}")
        print(f"最終スコア: {self.score_manager.get_score()}")
        print("Press R to restart")
    
    def show_final_score_screen(self):
        """
        最終スコア画面を表示する
        Requirements: 4.4 - 最終スコア画面の表示
        """
        self.show_final_score = True
    
    def restart_game(self):
        """
        ゲームを再開始する
        Requirements: 4.3 - ゲーム再開始機能
        """
        # ゲーム状態をリセット
        self.game_state_manager.start_game()
        
        # 最終スコア表示を無効化
        self.show_final_score = False
        self.game_over_reason = ""
        
        # スコア表示システムをリセット
        self.score_animation_active = False
        self.score_animation_timer = 0
        self.score_animation_phase = 0.0
        self.last_displayed_score = 0
        self.score_increment_amount = 0
        
        print("ゲームを再開始しました")
    
    def update_score_display_system(self):
        """
        スコア表示システムの更新処理
        Requirements: 4.1, 4.4 - スコア表示とアニメーション
        """
        current_score = self.score_manager.get_score()
        
        # スコアが変更された場合、アニメーションを開始
        if current_score != self.last_displayed_score:
            self.score_increment_amount = current_score - self.last_displayed_score
            self.last_displayed_score = current_score
            self.score_animation_active = True
            self.score_animation_timer = 0
            self.score_animation_phase = 0.0
        
        # アニメーションの更新
        if self.score_animation_active:
            self.score_animation_timer += 1
            self.score_animation_phase += 0.3  # アニメーション速度
            
            # アニメーション終了判定（60フレーム = 1秒）
            if self.score_animation_timer >= 60:
                self.score_animation_active = False
                self.score_animation_timer = 0
    
    def get_score_display_info(self):
        """
        スコア表示情報を取得
        
        Returns:
            tuple: スコア表示に必要な情報
        """
        return (self.score_animation_active, self.score_animation_timer,
                self.score_animation_phase, self.score_increment_amount)