"""
Game Systems - ゲームロジックシステムの管理
Requirements: 2.1, 2.4, 2.5, 3.1, 3.3, 3.4 - 落下、消去、重力、連鎖システム
"""

import pyxel
from src.audio_manager import SoundType


class GameSystems:
    """
    ゲームシステム管理 - 落下、消去、重力、連鎖システムを統合管理
    """
    
    def __init__(self, playfield, puyo_manager, score_manager, audio_manager, input_handler):
        """
        GameSystemsの初期化
        
        Args:
            playfield: プレイフィールド
            puyo_manager: ぷよ管理システム
            score_manager: スコア管理システム
            audio_manager: 音響管理システム
            input_handler: 入力処理システム
        """
        self.playfield = playfield
        self.puyo_manager = puyo_manager
        self.score_manager = score_manager
        self.audio_manager = audio_manager
        self.input_handler = input_handler
        
        # 落下システムの設定
        self.fall_timer = 0
        self.fall_interval = 40  # 通常の落下間隔
        self.fast_fall_interval = 1  # 高速落下間隔
        
        # 現在操作中のぷよペア
        self.current_falling_pair = None
        
        # 重力処理システムの設定
        self.gravity_active = False
        self.gravity_timer = 0
        self.gravity_interval = 5
        
        # 消去システムの設定
        self.elimination_active = False
        self.elimination_timer = 0
        self.elimination_interval = 30
        self.elimination_groups = []
        
        # 連鎖システムの設定
        self.chain_level = 0
        self.chain_active = False
        self.total_chain_score = 0
        
        # 連鎖表示システムの設定
        self.chain_display_timer = 0
        self.chain_display_duration = 60
        self.chain_animation_phase = 0
        self.show_chain_text = False
        
        # デバッグモード
        self.debug_mode = False
        
        # ゲームオーバー関連
        self.trigger_game_over = False
        self.game_over_reason = ""
    
    def debug_print(self, message):
        """
        デバッグモードでのみメッセージを出力する
        
        Args:
            message (str): 出力するメッセージ
        """
        if self.debug_mode:
            print(message)
    
    def initialize_first_pair(self):
        """
        最初の落下ペアを設定
        """
        self.current_falling_pair = self.puyo_manager.get_current_pair()
    
    def update_fall_system(self):
        """
        落下システムの更新処理
        Requirements: 2.1, 2.4, 2.5 - 自動落下、高速落下、ぷよ固定
        """
        if self.current_falling_pair is None:
            return
        
        # 落下タイマーの更新
        self.fall_timer += 1
        
        # 高速落下中かどうかをチェック
        is_fast_dropping = pyxel.btn(pyxel.KEY_DOWN)
        
        # 落下間隔の決定
        current_fall_interval = self.fast_fall_interval if is_fast_dropping else self.fall_interval
        
        # 落下タイミングかどうかをチェック
        should_fall = self.fall_timer >= current_fall_interval
        
        if should_fall:
            # 下に移動できるかチェック
            if self.playfield.can_move_puyo_pair(self.current_falling_pair, 0, 1):
                # 下に移動
                self.current_falling_pair.move(0, 1)
                self.fall_timer = 0  # タイマーリセット
            else:
                # 移動できない場合はぷよペアを固定
                self.fix_puyo_pair()
    
    def fix_puyo_pair(self):
        """
        現在のぷよペアをプレイフィールドに固定する
        Requirements: 2.5 - ぷよが底面または他のぷよに接触する時の固定処理
        """
        if self.current_falling_pair is None:
            return
        
        # ぷよペアの両方のぷよをプレイフィールドに配置
        main_pos, sub_pos = self.current_falling_pair.get_puyo_positions()
        
        # メインぷよを配置
        main_puyo = self.current_falling_pair.get_main_puyo()
        self.playfield.place_puyo(main_pos[0], main_pos[1], main_puyo)
        
        # サブぷよを配置
        sub_puyo = self.current_falling_pair.get_sub_puyo()
        self.playfield.place_puyo(sub_pos[0], sub_pos[1], sub_puyo)
        
        # 着地音を再生
        self.audio_manager.play_sound(SoundType.LAND)
        
        # 消去処理を開始
        self.start_elimination_process()
        
        # 次のぷよペアに進む
        self.current_falling_pair = self.puyo_manager.advance_to_next_pair()
        
        # 新しいぷよペアが配置できるかチェック（ゲームオーバー判定）
        if not self.can_place_new_pair():
            self.trigger_game_over = True
            self.game_over_reason = "新しいぷよペアが配置できません"
        
        # 落下タイマーをリセット
        self.fall_timer = 0
    
    def start_elimination_process(self):
        """
        消去処理を開始
        Requirements: 3.1, 5.2 - ぷよ固定後の消去処理開始
        """
        # 消去可能なグループを検出
        erasable_groups = self.playfield.find_erasable_groups()
        
        if erasable_groups:
            # 連鎖レベルを増加（初回消去は連鎖レベル1）
            if not self.chain_active:
                self.chain_level = 1
                self.chain_active = True
                self.debug_print(f"連鎖開始！連鎖レベル: {self.chain_level}")
            else:
                self.chain_level += 1
                self.debug_print(f"連鎖継続！連鎖レベル: {self.chain_level}")
            
            # 連鎖表示を開始
            self.show_chain_text = True
            self.chain_display_timer = 0
            self.chain_animation_phase = 0
            
            # 消去処理を開始
            self.elimination_active = True
            self.elimination_timer = 0
            self.elimination_groups = erasable_groups
            
            # デバッグ情報
            self.debug_print(f"消去処理開始: {len(erasable_groups)}グループ、{sum(len(group) for group in erasable_groups)}個のぷよ")
        else:
            # 消去するものがない場合
            if self.chain_active:
                # 連鎖が終了
                self.end_chain()
            else:
                # 通常の重力処理に移行
                self.apply_gravity_after_fixation()
    
    def update_elimination_system(self):
        """
        消去システムの更新処理
        Requirements: 3.1, 5.2 - 消去アニメーションと処理の管理
        """
        if not self.elimination_active:
            return
        
        # 消去タイマーの更新
        self.elimination_timer += 1
        
        # 消去アニメーションの実行タイミングかチェック
        if self.elimination_timer >= self.elimination_interval:
            # 実際に消去を実行
            eliminated, total_erased, group_count = self.playfield.process_puyo_elimination()
            
            if eliminated:
                self.debug_print(f"ぷよ消去完了: {total_erased}個のぷよ、{group_count}グループ")
                
                # 消去音または連鎖音を再生
                if self.chain_level > 1:
                    # 連鎖時は連鎖音を再生（連鎖レベルに応じた音程変化）
                    self.audio_manager.play_sound(SoundType.CHAIN, self.chain_level)
                else:
                    # 通常の消去音を再生
                    self.audio_manager.play_sound(SoundType.CLEAR)
                
                # スコア計算と加算
                chain_score = self.score_manager.calculate_chain_score(self.elimination_groups, self.chain_level)
                self.score_manager.add_score(chain_score)
                self.total_chain_score += chain_score
                
                self.debug_print(f"スコア加算: {chain_score}点 (連鎖レベル: {self.chain_level})")
                self.debug_print(f"現在のスコア: {self.score_manager.get_score()}点")
                
                # 消去処理完了、重力処理に移行
                self.elimination_active = False
                self.elimination_timer = 0
                self.elimination_groups = []
                
                # 重力処理を開始
                self.apply_gravity_after_fixation()
            else:
                # 消去するものがなかった場合（エラー状態）
                self.elimination_active = False
                self.elimination_timer = 0
                self.elimination_groups = []
    
    def apply_gravity_after_fixation(self):
        """
        ぷよ固定後の重力処理を開始
        Requirements: 3.3 - ぷよ固定後の重力適用
        """
        # 重力処理を開始
        self.gravity_active = True
        self.gravity_timer = 0
    
    def update_gravity_system(self):
        """
        重力システムの更新処理
        Requirements: 3.3 - 浮いているぷよの落下処理、重力処理のアニメーション
        """
        if not self.gravity_active:
            return
        
        # 重力タイマーの更新
        self.gravity_timer += 1
        
        # 重力処理の実行タイミングかチェック
        if self.gravity_timer >= self.gravity_interval:
            # 重力を適用
            gravity_applied = self.playfield.apply_gravity()
            
            if gravity_applied:
                # ぷよが移動した場合、タイマーをリセットして継続
                self.gravity_timer = 0
            else:
                # ぷよが移動しなかった場合、重力処理を終了
                self.gravity_active = False
                self.gravity_timer = 0
                
                # 重力処理完了後、再度消去判定を行う（連鎖のため）
                self.check_for_chain_elimination()
    
    def check_for_chain_elimination(self):
        """
        連鎖のための消去判定をチェック
        Requirements: 3.4 - 連鎖判定の実装
        """
        # 重力処理後に新たな消去可能グループがあるかチェック
        erasable_groups = self.playfield.find_erasable_groups()
        
        if erasable_groups:
            # 連鎖発生！再度消去処理を開始
            self.debug_print(f"連鎖発生！{len(erasable_groups)}グループが新たに消去可能")
            self.start_elimination_process()
        else:
            # 連鎖終了、通常のゲーム状態に戻る
            if self.chain_active:
                self.end_chain()
            else:
                self.debug_print("消去・重力処理完了")
    
    def end_chain(self):
        """
        連鎖を終了し、連鎖関連の状態をリセットする
        Requirements: 3.4 - 連鎖の終了判定
        """
        if self.chain_active:
            self.debug_print(f"連鎖終了！最終連鎖レベル: {self.chain_level}")
            
            # 連鎖状態をリセット
            self.chain_active = False
            final_chain_level = self.chain_level
            self.chain_level = 0
            self.total_chain_score = 0
            
            # 連鎖表示を終了
            self.show_chain_text = False
            self.chain_display_timer = 0
            
            # 連鎖終了後の処理（将来的にスコア計算などを追加）
            self.debug_print(f"連鎖完了: {final_chain_level}連鎖")
        
        self.debug_print("通常のゲーム状態に戻る")
    
    def update_chain_display_system(self):
        """
        連鎖表示システムの更新処理
        Requirements: 5.3 - 連鎖数の視覚的表示
        """
        if not self.show_chain_text:
            return
        
        # 連鎖表示タイマーの更新
        self.chain_display_timer += 1
        
        # アニメーション位相の更新（サイン波でアニメーション）
        self.chain_animation_phase = (self.chain_animation_phase + 0.2) % (2 * 3.14159)
        
        # 表示時間が経過したら表示を終了
        if self.chain_display_timer >= self.chain_display_duration:
            self.show_chain_text = False
            self.chain_display_timer = 0
    
    def handle_puyo_pair_input(self):
        """
        現在のぷよペアに対する入力処理
        Requirements: 2.2, 2.3, 2.4 - 移動、回転、高速落下の入力処理
        """
        if self.current_falling_pair is None:
            return
        
        # 左右移動の処理
        if self.input_handler.should_move_left():
            if self.playfield.can_move_puyo_pair(self.current_falling_pair, -1, 0):
                self.current_falling_pair.move(-1, 0)
                # 移動音を再生
                self.audio_manager.play_sound(SoundType.MOVE)
        
        if self.input_handler.should_move_right():
            if self.playfield.can_move_puyo_pair(self.current_falling_pair, 1, 0):
                self.current_falling_pair.move(1, 0)
                # 移動音を再生
                self.audio_manager.play_sound(SoundType.MOVE)
        
        # 回転の処理（キックシステム付き）
        if self.input_handler.should_rotate_clockwise():
            if self.playfield.rotate_puyo_pair_with_kick(self.current_falling_pair, True):
                # 回転音を再生
                self.audio_manager.play_sound(SoundType.ROTATE)
        
        if self.input_handler.should_rotate_counterclockwise():
            if self.playfield.rotate_puyo_pair_with_kick(self.current_falling_pair, False):
                # 回転音を再生
                self.audio_manager.play_sound(SoundType.ROTATE)
        
        # 高速落下の処理（個別の下移動）
        if self.input_handler.should_fast_drop():
            if self.playfield.can_move_puyo_pair(self.current_falling_pair, 0, 1):
                self.current_falling_pair.move(0, 1)
                self.fall_timer = 0  # タイマーリセット
                
                # 高速落下時は小さな効果音を再生（移動音より小さく）
                self.audio_manager.play_sound(SoundType.MOVE)
    
    def is_systems_active(self):
        """
        システムが処理中かどうかを確認
        
        Returns:
            bool: 消去・重力処理中の場合True
        """
        return self.elimination_active or self.gravity_active
    
    def get_chain_display_info(self):
        """
        連鎖表示情報を取得
        
        Returns:
            tuple: (show_chain_text, chain_level, chain_animation_phase)
        """
        return self.show_chain_text, self.chain_level, self.chain_animation_phase
    
    def get_elimination_info(self):
        """
        消去処理情報を取得
        
        Returns:
            tuple: (elimination_active, elimination_timer, elimination_groups)
        """
        return self.elimination_active, self.elimination_timer, self.elimination_groups
    
    def can_place_new_pair(self):
        """
        新しいぷよペアが配置できるかチェック
        
        Returns:
            bool: 配置可能な場合True
        """
        if self.current_falling_pair is None:
            return True
        
        # 現在のぷよペアの位置を取得
        main_pos, sub_pos = self.current_falling_pair.get_puyo_positions()
        
        # メインぷよとサブぷよの位置が空いているかチェック
        main_empty = self.playfield.is_empty(main_pos[0], main_pos[1])
        sub_empty = self.playfield.is_empty(sub_pos[0], sub_pos[1])
        
        # 両方の位置が空いている場合のみ配置可能
        if not main_empty or not sub_empty:
            self.debug_print(f"ゲームオーバー: 新しいぷよペアが配置不可能")
            self.debug_print(f"メインぷよ位置 {main_pos} は空か: {main_empty}")
            self.debug_print(f"サブぷよ位置 {sub_pos} は空か: {sub_empty}")
            return False
        
        return True
    
    def get_game_over_status(self):
        """
        ゲームオーバー状態を取得
        
        Returns:
            tuple: (trigger_game_over, game_over_reason)
        """
        return self.trigger_game_over, self.game_over_reason
    
    def reset_game_over_flag(self):
        """
        ゲームオーバーフラグをリセット
        """
        self.trigger_game_over = False
        self.game_over_reason = ""