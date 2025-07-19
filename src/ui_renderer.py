"""
UI Renderer - ゲーム画面の描画を担当
Requirements: 4.1, 4.4, 5.3 - UI要素の描画とアニメーション
"""

import pyxel
import math


class UIRenderer:
    """
    UI描画システム - 全ての画面描画処理を管理
    """
    
    def __init__(self, game_state_manager, score_manager, puyo_manager, audio_manager):
        """
        UIRendererの初期化
        
        Args:
            game_state_manager: ゲーム状態管理システム
            score_manager: スコア管理システム
            puyo_manager: ぷよ管理システム
            audio_manager: 音響管理システム
        """
        self.game_state_manager = game_state_manager
        self.score_manager = score_manager
        self.puyo_manager = puyo_manager
        self.audio_manager = audio_manager
        
        # 画面レイアウト設定
        self.playfield_x = 88
        self.playfield_y = 60
        self.playfield_width = 144  # 6 * 24ピクセル
        self.playfield_height = 288  # 12 * 24ピクセル
        
        # NEXT表示エリア設定
        self.next_preview_x = self.playfield_x + self.playfield_width + 20
        self.next_preview_y = self.playfield_y + 20
        self.preview_width = 70
        self.preview_height = 80
        
        # スコア表示エリア設定
        self.score_area_x = self.next_preview_x - 5
        self.score_area_y = self.next_preview_y + self.preview_height - 15
        self.score_area_width = self.preview_width
        self.score_area_height = 60
    
    def draw_background(self, frame_count, danger_level):
        """
        背景の描画
        
        Args:
            frame_count: フレームカウンター
            danger_level: 危険レベル
        """
        # 画面をクリア（黒色）
        pyxel.cls(0)
        
        # 危険レベルに応じた背景色の変更（ゲームオーバー警告）
        if danger_level >= 3 and frame_count % 30 < 15:  # 0.5秒ごとに点滅
            # 画面の上部に赤い警告帯を表示
            pyxel.rect(0, 0, 320, 10, 8)  # 赤色の警告帯
    
    def draw_title(self):
        """
        ゲームタイトルの描画
        """
        title_text = "Puyo Puyo Puzzle Game"
        title_x = (320 - len(title_text) * 4) // 2  # 中央揃え
        pyxel.text(title_x, 50, title_text, 7)  # 白色で表示
    
    def draw_playfield_frame(self):
        """
        プレイフィールドの枠線描画
        """
        # プレイフィールドの背景と枠線を描画
        pyxel.rect(self.playfield_x - 2, self.playfield_y - 2, 
                  self.playfield_width + 4, self.playfield_height + 4, 5)  # 紫色の背景
        pyxel.rectb(self.playfield_x - 3, self.playfield_y - 3, 
                   self.playfield_width + 6, self.playfield_height + 6, 7)  # 白色の外枠
        pyxel.rectb(self.playfield_x - 1, self.playfield_y - 1, 
                   self.playfield_width + 2, self.playfield_height + 2, 13)  # 薄い紫色の内枠
    
    def draw_danger_warnings(self, danger_level, frame_count):
        """
        危険レベルの視覚的警告表示
        
        Args:
            danger_level: 危険レベル
            frame_count: フレームカウンター
        """
        if danger_level >= 3:
            # 上部3行に警告表示（点滅効果）
            if frame_count % 30 < 15:  # 0.5秒ごとに点滅
                for y in range(3):
                    # 上部3行に半透明の赤い警告エリアを表示
                    warning_y = self.playfield_y + y * 24
                    pyxel.rect(self.playfield_x, warning_y, self.playfield_width, 2, 8)  # 赤色の警告線
    
    def draw_elimination_effects(self, elimination_active, elimination_timer, elimination_groups):
        """
        消去予定のぷよの点滅表示
        
        Args:
            elimination_active: 消去処理中フラグ
            elimination_timer: 消去タイマー
            elimination_groups: 消去予定グループ
        """
        if elimination_active and elimination_groups:
            # 点滅効果（フレーム数に基づく）
            if (elimination_timer // 5) % 2 == 0:  # 5フレームごとに点滅
                for group in elimination_groups:
                    for x, y in group:
                        screen_x = self.playfield_x + x * 24
                        screen_y = self.playfield_y + y * 24
                        # 白い枠で強調表示
                        pyxel.rectb(screen_x, screen_y, 24, 24, 7)
    
    def draw_next_preview(self):
        """
        次のぷよペアのプレビュー表示
        """
        # 次のぷよペアの表示エリアの背景と枠線
        pyxel.rect(self.next_preview_x - 5, self.next_preview_y - 25, 
                  self.preview_width, self.preview_height, 1)  # 暗い青色の背景
        pyxel.rectb(self.next_preview_x - 5, self.next_preview_y - 25, 
                   self.preview_width, self.preview_height, 7)  # 白色の枠線
        
        # "NEXT" ラベルの表示（中央揃え）
        pyxel.text(self.next_preview_x + 15, self.next_preview_y - 20, "NEXT", 7)
        
        # 次のペアのプレビューを描画（中央に配置）
        self.puyo_manager.draw_next_pair_preview(self.next_preview_x + 11, self.next_preview_y + 10)
    
    def draw_score_area(self, score_animation_active, score_animation_timer, 
                       score_animation_phase, score_increment_amount):
        """
        スコア表示エリアの描画
        
        Args:
            score_animation_active: スコアアニメーション中フラグ
            score_animation_timer: アニメーションタイマー
            score_animation_phase: アニメーション位相
            score_increment_amount: スコア増加量
        """
        # スコア表示エリアの背景と枠線
        pyxel.rect(self.score_area_x, self.score_area_y, 
                  self.score_area_width, self.score_area_height, 5)  # 紫色の背景
        pyxel.rectb(self.score_area_x, self.score_area_y, 
                   self.score_area_width, self.score_area_height, 7)  # 白色の枠線
        
        # 強化されたスコア表示
        self.draw_enhanced_score_display(self.score_area_x + 5, self.score_area_y + 5,
                                       score_animation_active, score_animation_timer,
                                       score_animation_phase, score_increment_amount)
    
    def draw_enhanced_score_display(self, x, y, score_animation_active, score_animation_timer,
                                  score_animation_phase, score_increment_amount):
        """
        強化されたスコア表示の描画
        
        Args:
            x, y: 表示座標
            score_animation_active: アニメーション中フラグ
            score_animation_timer: アニメーションタイマー
            score_animation_phase: アニメーション位相
            score_increment_amount: スコア増加量
        """
        current_score = self.score_manager.get_score()
        
        # スコアラベルの表示
        pyxel.text(x, y, "SCORE", 7)
        
        # スコア値の表示
        score_text = self.score_manager.format_score(current_score)
        score_y = y + 10
        
        # アニメーション効果
        if score_animation_active:
            # 点滅効果
            blink_intensity = abs(math.sin(score_animation_phase * 2))
            if blink_intensity > 0.5:
                score_color = 10  # 明るい緑色
            else:
                score_color = 11  # 通常の緑色
            
            # 拡大効果
            scale_factor = 1.0 + 0.2 * math.sin(score_animation_phase)
            
            # スコア増加量の表示
            if score_increment_amount > 0:
                increment_text = f"+{self.score_manager.format_score(score_increment_amount)}"
                increment_y = score_y - 10 - int(5 * math.sin(score_animation_phase))
                pyxel.text(x + 50, increment_y, increment_text, 8)  # 赤色で増加量表示
        else:
            score_color = 7  # 通常の白色
        
        # スコア値の描画
        pyxel.text(x, score_y, score_text, score_color)
        
        # スコアの背景枠（見やすさ向上）
        text_width = len(score_text) * 4
        pyxel.rectb(x - 2, y - 2, max(text_width + 4, 50), 22, 7)
    
    def draw_chain_animation(self, show_chain_text, chain_level, chain_animation_phase):
        """
        連鎖アニメーション表示
        
        Args:
            show_chain_text: 連鎖テキスト表示フラグ
            chain_level: 連鎖レベル
            chain_animation_phase: アニメーション位相
        """
        if show_chain_text and chain_level > 0:
            # アニメーション効果（サイン波による拡大縮小）
            scale_factor = 1.0 + 0.3 * math.sin(chain_animation_phase)
            
            # 連鎖テキストの表示位置（画面中央）
            chain_text = f"{chain_level} CHAIN!"
            text_width = len(chain_text) * 4
            text_x = (320 - text_width) // 2
            text_y = 200
            
            # 背景の描画（黒い矩形）
            bg_width = int(text_width * scale_factor) + 8
            bg_height = int(8 * scale_factor) + 4
            bg_x = text_x - (bg_width - text_width) // 2 - 4
            bg_y = text_y - (bg_height - 8) // 2 - 2
            pyxel.rect(bg_x, bg_y, bg_width, bg_height, 0)
            pyxel.rectb(bg_x, bg_y, bg_width, bg_height, 7)
            
            # 連鎖数に応じた色の選択
            chain_colors = [7, 8, 9, 10, 11, 12, 13, 14, 15]  # 白から様々な色
            color_index = min(chain_level - 1, len(chain_colors) - 1)
            chain_color = chain_colors[color_index]
            
            # 連鎖テキストの描画
            pyxel.text(text_x, text_y, chain_text, chain_color)
    
    def draw_controls_panel(self, debug_mode):
        """
        操作説明パネルの描画
        
        Args:
            debug_mode: デバッグモードフラグ
        """
        controls_x = 10
        controls_y = 380
        controls_width = 300
        controls_height = 90
        
        # 操作説明パネルの背景と枠線
        pyxel.rect(controls_x, controls_y, controls_width, controls_height, 1)  # 暗い青色の背景
        pyxel.rectb(controls_x, controls_y, controls_width, controls_height, 7)  # 白色の枠線
        
        # 操作説明のタイトル
        pyxel.text(controls_x + 10, controls_y + 5, "CONTROLS:", 10)  # 緑色のタイトル
        
        # 操作説明の表示
        col1_x = controls_x + 10
        col2_x = controls_x + 160
        
        # 基本操作（常に表示）
        pyxel.text(col1_x, controls_y + 20, "Arrow Keys: Move/Drop", 7)
        pyxel.text(col1_x, controls_y + 30, "X/UP: Rotate CW", 7)
        pyxel.text(col1_x, controls_y + 40, "Z: Rotate CCW", 7)
        pyxel.text(col1_x, controls_y + 50, "R: Restart Game", 7)
        pyxel.text(col1_x, controls_y + 60, "Q/ESC: Quit Game", 7)
        
        # デバッグ用操作（デバッグモード時のみ表示）
        if debug_mode:
            pyxel.text(col2_x, controls_y + 20, "G: Test Gravity", 6)
            pyxel.text(col2_x, controls_y + 30, "C: Test Connection", 6)
            pyxel.text(col2_x, controls_y + 40, "E: Test Elimination", 6)
            pyxel.text(col2_x, controls_y + 50, "A: Test Chain", 6)
    
    def draw_final_score_display(self, show_final_score):
        """
        最終スコア表示の描画
        
        Args:
            show_final_score: 最終スコア表示フラグ
        """
        if not show_final_score:
            return
        
        # 最終スコア画面の背景
        screen_width = 320
        screen_height = 480
        
        # 半透明の黒い背景
        pyxel.rect(0, 0, screen_width, screen_height, 0)
        
        # 最終スコア表示エリア
        final_score_x = 60
        final_score_y = 150
        final_score_width = 200
        final_score_height = 180
        
        # 最終スコア表示の背景と枠線
        pyxel.rect(final_score_x, final_score_y, final_score_width, final_score_height, 5)  # 紫色の背景
        pyxel.rectb(final_score_x, final_score_y, final_score_width, final_score_height, 7)  # 白色の枠線
        pyxel.rectb(final_score_x + 2, final_score_y + 2, final_score_width - 4, final_score_height - 4, 13)  # 内側の枠線
        
        # タイトル
        title_text = "GAME OVER"
        title_x = final_score_x + (final_score_width - len(title_text) * 4) // 2
        pyxel.text(title_x, final_score_y + 20, title_text, 8)  # 赤色
        
        # 最終スコア
        final_score = self.score_manager.get_score()
        score_text = f"FINAL SCORE: {self.score_manager.format_score(final_score)}"
        score_x = final_score_x + (final_score_width - len(score_text) * 4) // 2
        pyxel.text(score_x, final_score_y + 50, score_text, 7)  # 白色
        
        # 操作説明
        restart_text = "Press R to Restart"
        restart_x = final_score_x + (final_score_width - len(restart_text) * 4) // 2
        pyxel.text(restart_x, final_score_y + 80, restart_text, 10)  # 緑色
        
        menu_text = "Press ESC for Menu"
        menu_x = final_score_x + (final_score_width - len(menu_text) * 4) // 2
        pyxel.text(menu_x, final_score_y + 100, menu_text, 7)  # 白色