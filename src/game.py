import pyxel
from src.puyo import Puyo
from src.puyo_pair import PuyoPair
from src.playfield import PlayField
from src.input_handler import InputHandler
from src.puyo_manager import PuyoManager
from src.score_manager import ScoreManager
from src.game_state import GameStateManager, GameState
from src.audio_manager import AudioManager, SoundType, BGMType
from src.ui_elements import Button, Slider, Label, Panel, UIManager


class PuyoPuyoGame:
    """
    メインゲームクラス - Pyxelアプリケーションを管理
    Requirements: 1.1, 1.2
    """
    
    def __init__(self):
        """
        Pyxelアプリケーションの初期化
        """
        # 画面サイズの設定（320x480ピクセル - デザイン文書に基づく）
        pyxel.init(320, 480, title="Puyo Puyo Puzzle Game")
        
        # ゲーム状態の初期化
        self.initialize_game()
        
        # Pyxelアプリケーションの開始
        pyxel.run(self.update, self.draw)
    
    def initialize_game(self):
        """
        ゲームの初期化処理
        基本的なゲーム状態変数を設定
        """
        # ゲーム実行状態
        self.game_running = True
        
        # フレームカウンター（デバッグ用）
        self.frame_count = 0
        
        # 落下システムの設定
        # Requirements: 2.1 - 重力に従ってぷよを移動させる
        # Requirements: 14.2 - 操作感の調整、アニメーション速度の最適化
        self.fall_timer = 0  # 自動落下タイマー
        self.fall_interval = 40  # 通常の落下間隔（45→40フレームに短縮 = 約0.67秒）- 操作感改善
        self.fast_fall_interval = 1  # 高速落下間隔（2→1フレームに短縮）- より素早い高速落下
        
        # 現在操作中のぷよペア
        self.current_falling_pair = None
        
        # プレイフィールドを作成
        self.playfield = PlayField()
        
        # デバッグモード設定
        self.debug_mode = False
        self.test_puyos = []  # テスト用ぷよ（デバッグモード時のみ使用）
        
        # 入力処理システムを作成（InputHandlerクラスの動作確認用）
        self.input_handler = InputHandler()
        
        # ぷよ管理システムを作成（PuyoManagerクラスの動作確認用）
        self.puyo_manager = PuyoManager()
        
        # スコア管理システムを作成（ScoreManagerクラスの動作確認用）
        self.score_manager = ScoreManager()
        
        # スコア表示システムの初期化
        # Requirements: 4.1, 4.4 - スコア表示とアニメーション
        self.score_animation_active = False  # スコア更新アニメーションが進行中かどうか
        self.score_animation_timer = 0  # スコアアニメーションのタイマー
        self.score_animation_phase = 0.0  # スコアアニメーションの位相
        self.last_displayed_score = 0  # 最後に表示されたスコア（アニメーション用）
        self.score_increment_amount = 0  # スコア増加量（アニメーション用）
        self.show_final_score = False  # 最終スコア表示フラグ
        
        # ゲーム状態管理システムの初期化
        # Requirements: 4.3, 4.4 - ゲーム状態の管理と遷移制御
        self.game_state_manager = GameStateManager()
        
        # 最初の落下ペアを設定
        self.current_falling_pair = self.puyo_manager.get_current_pair()
        
        # 重力処理システムの設定
        # Requirements: 3.3 - 重力処理のアニメーション
        self.gravity_active = False  # 重力処理中フラグ
        self.gravity_timer = 0  # 重力アニメーションタイマー
        self.gravity_interval = 5  # 重力処理の間隔（フレーム数）
        
        # 消去システムの設定
        # Requirements: 3.1, 5.2 - ぷよ消去処理とアニメーション
        self.elimination_active = False  # 消去処理中フラグ
        self.elimination_timer = 0  # 消去アニメーションタイマー
        self.elimination_interval = 30  # 消去アニメーションの間隔（フレーム数）
        self.elimination_groups = []  # 消去予定のグループ
        
        # 連鎖システムの設定
        # Requirements: 3.4 - 連鎖判定の実装
        self.chain_level = 0  # 現在の連鎖レベル
        self.chain_active = False  # 連鎖処理中フラグ
        self.total_chain_score = 0  # 連鎖による総スコア
        
        # 連鎖表示システムの設定
        # Requirements: 5.3 - 連鎖数の視覚的表示
        self.chain_display_timer = 0  # 連鎖表示タイマー
        self.chain_display_duration = 60  # 連鎖表示の持続時間（フレーム数）
        self.chain_animation_phase = 0  # アニメーション位相
        self.show_chain_text = False  # 連鎖テキスト表示フラグ
        
        # ゲームオーバー関連の設定
        # Requirements: 4.3, 4.4 - ゲームオーバー判定と表示
        self.game_over_reason = ""  # ゲームオーバーの理由
        
        # 音響システムの初期化
        # Requirements: 12.1 - AudioManagerクラスの実装
        self.audio_manager = AudioManager()
        
        # ゲーム開始時のBGM再生
        self.audio_manager.play_bgm(BGMType.GAME)
        
        # デバッグ: 初期状態を確認
        print(f"Game initialized - gravity_active: {self.gravity_active}")
    
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
        # Requirements: 12.2 - ぷよ着地時の効果音
        self.audio_manager.play_sound(SoundType.LAND)
        
        # Start elimination process after puyo fixation
        # Requirements: 3.1, 5.2 - Elimination process after puyo fixation
        self.start_elimination_process()
        
        # 次のぷよペアに進む
        self.current_falling_pair = self.puyo_manager.advance_to_next_pair()
        
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
                print(f"連鎖開始！連鎖レベル: {self.chain_level}")
            else:
                self.chain_level += 1
                print(f"連鎖継続！連鎖レベル: {self.chain_level}")
            
            # 連鎖表示を開始
            # Requirements: 5.3 - 連鎖数の視覚的表示
            self.show_chain_text = True
            self.chain_display_timer = 0
            self.chain_animation_phase = 0
            
            # 消去処理を開始
            self.elimination_active = True
            self.elimination_timer = 0
            self.elimination_groups = erasable_groups
            
            # デバッグ情報
            print(f"消去処理開始: {len(erasable_groups)}グループ、{sum(len(group) for group in erasable_groups)}個のぷよ")
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
                print(f"ぷよ消去完了: {total_erased}個のぷよ、{group_count}グループ")
                
                # 消去音または連鎖音を再生
                # Requirements: 12.2 - ぷよ消去時・連鎖時の効果音
                if self.chain_level > 1:
                    # 連鎖時は連鎖音を再生（連鎖レベルに応じた音程変化）
                    self.audio_manager.play_sound(SoundType.CHAIN, self.chain_level)
                else:
                    # 通常の消去音を再生
                    self.audio_manager.play_sound(SoundType.CLEAR)
                
                # スコア計算と加算
                # Requirements: 3.2 - スコア加算
                chain_score = self.score_manager.calculate_chain_score(self.elimination_groups, self.chain_level)
                self.score_manager.add_score(chain_score)
                self.total_chain_score += chain_score
                
                print(f"スコア加算: {chain_score}点 (連鎖レベル: {self.chain_level})")
                print(f"現在のスコア: {self.score_manager.get_score()}点")
                
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
            print(f"連鎖発生！{len(erasable_groups)}グループが新たに消去可能")
            self.start_elimination_process()
        else:
            # 連鎖終了、通常のゲーム状態に戻る
            if self.chain_active:
                self.end_chain()
            else:
                print("消去・重力処理完了")
    
    def end_chain(self):
        """
        連鎖を終了し、連鎖関連の状態をリセットする
        Requirements: 3.4 - 連鎖の終了判定
        """
        if self.chain_active:
            print(f"連鎖終了！最終連鎖レベル: {self.chain_level}")
            
            # 連鎖状態をリセット
            self.chain_active = False
            final_chain_level = self.chain_level
            self.chain_level = 0
            self.total_chain_score = 0
            
            # 連鎖表示を終了
            self.show_chain_text = False
            self.chain_display_timer = 0
            
            # 連鎖終了後の処理（将来的にスコア計算などを追加）
            print(f"連鎖完了: {final_chain_level}連鎖")
        
        print("通常のゲーム状態に戻る")
    
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
                # Requirements: 12.2 - ぷよ移動時の効果音
                self.audio_manager.play_sound(SoundType.MOVE)
        
        if self.input_handler.should_move_right():
            if self.playfield.can_move_puyo_pair(self.current_falling_pair, 1, 0):
                self.current_falling_pair.move(1, 0)
                # 移動音を再生
                # Requirements: 12.2 - ぷよ移動時の効果音
                self.audio_manager.play_sound(SoundType.MOVE)
        
        # 回転の処理（キックシステム付き）
        if self.input_handler.should_rotate_clockwise():
            if self.playfield.rotate_puyo_pair_with_kick(self.current_falling_pair, True):
                # 回転音を再生
                # Requirements: 12.2 - ぷよ回転時の効果音
                self.audio_manager.play_sound(SoundType.ROTATE)
        
        if self.input_handler.should_rotate_counterclockwise():
            if self.playfield.rotate_puyo_pair_with_kick(self.current_falling_pair, False):
                # 回転音を再生
                # Requirements: 12.2 - ぷよ回転時の効果音
                self.audio_manager.play_sound(SoundType.ROTATE)
        
        # 高速落下の処理（個別の下移動）
        if self.input_handler.should_fast_drop():
            if self.playfield.can_move_puyo_pair(self.current_falling_pair, 0, 1):
                self.current_falling_pair.move(0, 1)
                self.fall_timer = 0  # タイマーリセット
                
                # 高速落下時は小さな効果音を再生（移動音より小さく）
                # Requirements: 12.2 - 高速落下時の効果音
                self.audio_manager.play_sound(SoundType.MOVE)
    
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
        # Requirements: 12.1 - AudioManagerの更新処理
        self.audio_manager.update()
        
        # 基本的なキー入力処理
        if self.input_handler.should_quit_game():
            pyxel.quit()
        
        # 重力テスト機能（Gキー）
        if self.input_handler.should_test_gravity():
            self.apply_gravity_after_fixation()
        
        # 連結判定テスト機能（Cキー）
        if self.input_handler.should_test_connection():
            self.test_connection_detection()
        
        # 消去処理テスト機能（Eキー）
        if self.input_handler.should_test_elimination():
            self.test_elimination_process()
        
        # 連鎖アニメーションテスト機能（Aキー）
        if self.input_handler.should_test_chain_animation():
            self.test_chain_animation()
        
        # 消去システムの更新
        # Requirements: 3.1, 5.2 - 消去処理とアニメーション
        self.update_elimination_system()
        
        # 重力システムの更新
        # Requirements: 3.3 - 浮いているぷよの落下処理、重力処理のアニメーション
        self.update_gravity_system()
        
        # 連鎖表示システムの更新
        # Requirements: 5.3 - 連鎖数の視覚的表示
        self.update_chain_display_system()
        
        # スコア表示システムの更新
        # Requirements: 4.1, 4.4 - スコア表示とアニメーション
        self.update_score_display_system()
        
        # ゲーム状態管理システムの更新
        # Requirements: 4.3, 4.4 - ゲーム状態の管理と遷移制御
        self.game_state_manager.update()
        
        # ゲーム状態に応じた処理分岐
        # Requirements: 4.3, 4.4 - 各状態での処理分岐
        self.update_state_specific_logic()
        
        # 消去・重力処理中でない場合のみ通常の落下システムと入力処理を実行
        if not self.elimination_active and not self.gravity_active:
            # 落下システムの更新
            # Requirements: 2.1, 2.4, 2.5 - 自動落下、高速落下、ぷよ固定
            self.update_fall_system()
            
            # 現在のぷよペアに対する入力処理
            # Requirements: 2.2, 2.3, 2.4 - 移動、回転、高速落下の入力処理
            self.handle_puyo_pair_input()
    
    def test_connection_detection(self):
        """
        連結判定のテスト機能
        Requirements: 3.1 - 連結グループの検出とデバッグ表示
        """
        # 連結グループを検出
        connected_groups = self.playfield.find_connected_groups()
        erasable_groups = self.playfield.find_erasable_groups()
        
        print(f"=== 連結判定テスト結果 ===")
        print(f"全連結グループ数: {len(connected_groups)}")
        print(f"消去可能グループ数: {len(erasable_groups)}")
        
        # 各グループの詳細を表示
        for i, group in enumerate(connected_groups):
            if len(group) >= 4:
                print(f"グループ {i+1}: {len(group)}個 (消去可能)")
            else:
                print(f"グループ {i+1}: {len(group)}個")
            
            # グループ内のぷよの色を確認
            if group:
                x, y = group[0]
                puyo = self.playfield.get_puyo(x, y)
                if puyo:
                    color_names = {1: "赤", 2: "オレンジ", 3: "緑", 4: "青"}
                    color_name = color_names.get(puyo.get_color(), "不明")
                    print(f"  色: {color_name}, 座標: {group}")
        
        print("========================")
    
    def test_elimination_process(self):
        """
        消去処理のテスト機能
        Requirements: 3.1, 5.2 - 消去処理のテストとデバッグ表示
        """
        # テスト用の消去可能なぷよを配置
        # 4つの赤いぷよを2x2で配置
        test_positions = [(0, 8), (0, 9), (1, 8), (1, 9)]
        for x, y in test_positions:
            if self.playfield.is_empty(x, y):
                self.playfield.place_puyo(x, y, Puyo(1))  # 赤いぷよ
        
        # 消去処理を開始
        self.start_elimination_process()
        
        print("=== 消去処理テスト実行 ===")
        print("4つの赤いぷよを左上に配置して消去処理を開始しました")
    
    def test_chain_animation(self):
        """
        連鎖アニメーションのテスト機能
        Requirements: 5.3 - 連鎖数の視覚的表示のテスト
        """
        # 連鎖レベルを循環させる（1-5連鎖）
        if not self.show_chain_text:
            # アニメーションが表示されていない場合、1連鎖から開始
            self.chain_level = 1
        else:
            # 既に表示中の場合、次のレベルに進む
            self.chain_level += 1
            if self.chain_level > 5:
                self.chain_level = 1
        
        # 連鎖アニメーションを開始
        self.show_chain_text = True
        self.chain_display_timer = 0
        self.chain_animation_phase = 0
        
        print(f"=== 連鎖アニメーションテスト実行 ===")
        print(f"{self.chain_level}連鎖のアニメーションを表示します")
    
    def draw(self):
        """
        画面描画処理（毎フレーム呼び出される）
        Requirements: 1.1 - システムはゲーム画面を表示する
        Requirements: 1.2 - システムはプレイフィールドとぷよを表示する
        """
        # 画面をクリア（黒色 - デザイン文書の色定義に基づく）
        pyxel.cls(0)
        
        # 危険レベルに応じた背景色の変更（ゲームオーバー警告）
        # Requirements: 4.3, 4.4 - ゲームオーバー警告の視覚的表示
        danger_level = self.get_danger_level()
        if danger_level >= 3 and self.frame_count % 30 < 15:  # 0.5秒ごとに点滅
            # 画面の上部に赤い警告帯を表示
            pyxel.rect(0, 0, 320, 10, 8)  # 赤色の警告帯
        
        # ゲームタイトルの表示
        title_text = "Puyo Puyo Puzzle Game"
        title_x = (320 - len(title_text) * 4) // 2  # 中央揃え
        pyxel.text(title_x, 50, title_text, 7)  # 白色で表示
        
        # プレイフィールドの枠を描画（デザイン文書の座標に基づく）
        # プレイフィールド位置: x=88-232, y=60-348
        playfield_x = 88
        playfield_y = 60
        playfield_width = 144  # 6 * 24ピクセル
        playfield_height = 288  # 12 * 24ピクセル
        
        # プレイフィールドの背景と枠線を描画
        # Requirements: 4.1 - プレイフィールドの枠線表示
        pyxel.rect(playfield_x - 2, playfield_y - 2, playfield_width + 4, playfield_height + 4, 5)  # 紫色の背景
        pyxel.rectb(playfield_x - 3, playfield_y - 3, playfield_width + 6, playfield_height + 6, 7)  # 白色の外枠
        pyxel.rectb(playfield_x - 1, playfield_y - 1, playfield_width + 2, playfield_height + 2, 13)  # 薄い紫色の内枠
        
        # プレイフィールドの描画
        self.playfield.draw(playfield_x, playfield_y)
        
        # 危険レベルの視覚的表示（上部3行の警告表示）
        # Requirements: 4.3, 4.4 - ゲームオーバー警告の視覚的表示
        danger_level = self.get_danger_level()
        if danger_level >= 3:
            # 上部3行に警告表示（点滅効果）
            if self.frame_count % 30 < 15:  # 0.5秒ごとに点滅
                for y in range(3):
                    # 上部3行に半透明の赤い警告エリアを表示
                    warning_y = playfield_y + y * 24
                    pyxel.rect(playfield_x, warning_y, playfield_width, 2, 8)  # 赤色の警告線
        
        # 消去予定のぷよを点滅表示（アニメーション効果）
        if self.elimination_active and self.elimination_groups:
            # 点滅効果（フレーム数に基づく）
            if (self.elimination_timer // 5) % 2 == 0:  # 5フレームごとに点滅
                for group in self.elimination_groups:
                    for x, y in group:
                        screen_x = playfield_x + x * 24
                        screen_y = playfield_y + y * 24
                        # 白い枠で強調表示
                        pyxel.rectb(screen_x, screen_y, 24, 24, 7)
        
        # デバッグモードの場合のみテスト用ぷよを描画
        if self.debug_mode:
            for i, puyo in enumerate(self.test_puyos):
                # プレイフィールド内の位置に描画
                screen_x = playfield_x + (i * 24)  # 24ピクセル間隔で配置
                screen_y = playfield_y + 24  # プレイフィールドの上から2行目
                puyo.draw(screen_x, screen_y)
        
        # 現在落下中のぷよペアの描画
        if self.current_falling_pair is not None:
            self.current_falling_pair.draw(playfield_x, playfield_y)
        
        # 次のぷよペアのプレビュー表示エリア
        # Requirements: 4.2 - 次のぷよペアの表示エリア
        next_preview_x = playfield_x + playfield_width + 20
        next_preview_y = playfield_y + 20
        
        # 次のぷよペアの表示エリアの背景と枠線
        preview_width = 60
        preview_height = 60
        pyxel.rect(next_preview_x - 5, next_preview_y - 20, preview_width, preview_height, 1)  # 暗い青色の背景
        pyxel.rectb(next_preview_x - 5, next_preview_y - 20, preview_width, preview_height, 7)  # 白色の枠線
        
        # "NEXT" ラベルの表示
        pyxel.text(next_preview_x + 10, next_preview_y - 15, "NEXT", 7)
        
        # 次のペアのプレビューを描画
        self.puyo_manager.draw_next_pair_preview(next_preview_x, next_preview_y)
        
        # 操作説明パネルの表示
        # Requirements: 4.1 - 基本UI要素の実装
        controls_x = 10
        controls_y = 380
        controls_width = 300
        controls_height = 90
        
        # 操作説明パネルの背景と枠線
        pyxel.rect(controls_x, controls_y, controls_width, controls_height, 1)  # 暗い青色の背景
        pyxel.rectb(controls_x, controls_y, controls_width, controls_height, 7)  # 白色の枠線
        
        # 操作説明のタイトル
        pyxel.text(controls_x + 10, controls_y + 5, "CONTROLS:", 10)  # 緑色のタイトル
        
        # 操作説明の表示（2列レイアウト）
        col1_x = controls_x + 10
        col2_x = controls_x + 160
        
        # 左列
        pyxel.text(col1_x, controls_y + 20, "Arrow Keys: Move/Drop", 7)
        pyxel.text(col1_x, controls_y + 30, "X/UP: Rotate CW", 7)
        pyxel.text(col1_x, controls_y + 40, "Z: Rotate CCW", 7)
        pyxel.text(col1_x, controls_y + 50, "R: Restart Game", 7)
        pyxel.text(col1_x, controls_y + 60, "Q/ESC: Quit Game", 7)
        
        # 右列（デバッグ用）
        pyxel.text(col2_x, controls_y + 20, "G: Test Gravity", 6)
        pyxel.text(col2_x, controls_y + 30, "C: Test Connection", 6)
        pyxel.text(col2_x, controls_y + 40, "E: Test Elimination", 6)
        pyxel.text(col2_x, controls_y + 50, "A: Test Chain", 6)
        
        # ゲーム情報パネルの表示
        info_x = 10
        info_y = 10
        info_width = 70
        info_height = 60
        
        # ゲーム情報パネルの背景と枠線
        pyxel.rect(info_x, info_y, info_width, info_height, 1)  # 暗い青色の背景
        pyxel.rectb(info_x, info_y, info_width, info_height, 7)  # 白色の枠線
        
        # デバッグ情報の表示
        pyxel.text(info_x + 5, info_y + 5, f"Frame: {self.frame_count}", 7)
        
        # 重力処理状態の表示
        if self.gravity_active:
            pyxel.text(info_x + 5, info_y + 20, "GRAVITY ACTIVE", 8)  # 赤色で表示
        else:
            pyxel.text(info_x + 5, info_y + 20, "Gravity: Idle", 7)   # 白色で表示
        
        # 消去処理状態の表示
        if self.elimination_active:
            pyxel.text(info_x + 5, info_y + 30, "ELIMINATION ACTIVE", 9)  # オレンジ色で表示
        else:
            pyxel.text(info_x + 5, info_y + 30, "Elimination: Idle", 7)   # 白色で表示
        
        # 現在のぷよペア状態の表示
        if self.current_falling_pair is not None:
            pair_pos = self.current_falling_pair.get_position()
            pyxel.text(info_x + 5, info_y + 40, f"Pair: ({pair_pos[0]}, {pair_pos[1]})", 7)
        else:
            pyxel.text(info_x + 5, info_y + 40, "Pair: None", 7)
        
        # 連鎖状態の表示
        if self.chain_active:
            pyxel.text(info_x + 5, info_y + 50, f"CHAIN: {self.chain_level}", 11)  # 緑色で表示
        else:
            pyxel.text(info_x + 5, info_y + 50, "Chain: None", 7)   # 白色で表示
        
        # スコア表示エリア
        # Requirements: 4.1 - スコア表示エリアのレイアウト
        score_area_x = next_preview_x - 5
        score_area_y = next_preview_y + preview_height + 10
        score_area_width = preview_width
        score_area_height = 60
        
        # スコア表示エリアの背景と枠線
        pyxel.rect(score_area_x, score_area_y, score_area_width, score_area_height, 5)  # 紫色の背景
        pyxel.rectb(score_area_x, score_area_y, score_area_width, score_area_height, 7)  # 白色の枠線
        
        # 強化されたスコア表示
        # Requirements: 4.1, 4.4 - 現在スコアの画面表示とアニメーション
        self.draw_enhanced_score_display(score_area_x + 5, score_area_y + 5)
        
        # 連鎖アニメーション表示
        # Requirements: 5.3 - 連鎖数の視覚的表示
        if self.show_chain_text and self.chain_level > 0:
            # アニメーション効果（サイン波による拡大縮小）
            import math
            scale_factor = 1.0 + 0.3 * math.sin(self.chain_animation_phase)
            
            # 連鎖テキストの表示位置（画面中央）
            chain_text = f"{self.chain_level} CHAIN!"
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
            color_index = min(self.chain_level - 1, len(chain_colors) - 1)
            chain_color = chain_colors[color_index]
            
            # 連鎖テキストの描画
            pyxel.text(text_x, text_y, chain_text, chain_color)
        
        # 最終スコア表示
        # Requirements: 4.4 - 最終スコアの表示
        self.draw_final_score_display()
    
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
                print_playfield_state(self.playfield, self.current_falling_pair)
                return True, f"プレイフィールド上端到達 (列 {x})"
        
        # 新しいぷよペアが配置できない場合の判定
        if self.current_falling_pair is not None:
            # 現在のぷよペアの位置を取得
            main_pos, sub_pos = self.current_falling_pair.get_puyo_positions()
            
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
                    print_playfield_state(self.playfield, self.current_falling_pair)
                    return True, "新しいぷよペアが配置不可能"
        
        # 危険レベルの判定（上から3行以内にぷよがある場合）
        danger_level = self.get_danger_level()
        if danger_level >= 3:
            # 危険レベルが高い場合の警告（ゲームオーバーではないが警告）
            return False, f"危険レベル: {danger_level}"
        
        return False, "正常"
    
    def get_danger_level(self):
        """
        危険レベルを取得する（上部にどれだけぷよが積まれているか）
        
        Returns:
            int: 危険レベル（0-12、高いほど危険）
        """
        danger_count = 0
        # 上から3行をチェック
        for y in range(3):
            for x in range(6):
                if not self.playfield.is_empty(x, y):
                    danger_count += 1
        return danger_count
    
    def handle_game_over(self, reason="ゲームオーバー"):
        """
        ゲームオーバー処理
        Requirements: 4.3, 4.4 - ゲームオーバー状態への遷移と最終スコア表示
        
        Args:
            reason (str): ゲームオーバーの理由
        """
        # ゲームオーバーの理由を保存
        self.game_over_reason = reason
        
        # ゲームオーバー音を再生
        # Requirements: 12.2 - ゲームオーバー時の効果音
        self.audio_manager.play_sound(SoundType.GAME_OVER)
        
        # BGMをゲームオーバー用に切り替え
        # Requirements: 12.3 - ゲームオーバー時の音楽
        self.audio_manager.play_bgm(BGMType.GAME_OVER)
        
        # 最終スコア画面を表示
        self.show_final_score_screen()
        
        # 現在のぷよペアを削除
        self.current_falling_pair = None
        
        print(f"=== GAME OVER ===")
        print(f"Reason: {reason}")
        print(f"Final Score: {self.score_manager.format_score()}")
        print("Press R to restart")
    
    def update_score_display_system(self):
        """
        スコア表示システムの更新処理
        Requirements: 4.1, 4.4 - スコア表示とアニメーション
        """
        current_score = self.score_manager.get_score()
        
        # スコアが変更された場合、アニメーションを開始
        if current_score != self.last_displayed_score:
            self.score_increment_amount = current_score - self.last_displayed_score
            self.score_animation_active = True
            self.score_animation_timer = 0
            self.score_animation_phase = 0.0
            self.last_displayed_score = current_score
        
        # スコアアニメーションの更新
        if self.score_animation_active:
            self.score_animation_timer += 1
            self.score_animation_phase = (self.score_animation_phase + 0.3) % (2 * 3.14159)
            
            # アニメーション終了判定（60フレーム = 1秒）
            if self.score_animation_timer >= 60:
                self.score_animation_active = False
                self.score_animation_timer = 0
    
    def draw_enhanced_score_display(self, x, y):
        """
        強化されたスコア表示の描画
        Requirements: 4.1, 4.4 - 現在スコアの画面表示とアニメーション
        
        Args:
            x (int): 表示X座標
            y (int): 表示Y座標
        """
        current_score = self.score_manager.get_score()
        
        # スコアラベルの表示
        pyxel.text(x, y, "SCORE", 7)
        
        # スコア値の表示
        score_text = self.score_manager.format_score(current_score)
        score_y = y + 10
        
        # アニメーション効果
        if self.score_animation_active:
            import math
            
            # 点滅効果
            blink_intensity = abs(math.sin(self.score_animation_phase * 2))
            if blink_intensity > 0.5:
                score_color = 10  # 明るい緑色
            else:
                score_color = 11  # 通常の緑色
            
            # 拡大効果
            scale_factor = 1.0 + 0.2 * math.sin(self.score_animation_phase)
            
            # スコア増加量の表示
            if self.score_increment_amount > 0:
                increment_text = f"+{self.score_manager.format_score(self.score_increment_amount)}"
                increment_y = score_y - 10 - int(5 * math.sin(self.score_animation_phase))
                pyxel.text(x + 50, increment_y, increment_text, 8)  # 赤色で増加量表示
        else:
            score_color = 7  # 通常の白色
        
        # スコア値の描画
        pyxel.text(x, score_y, score_text, score_color)
        
        # スコアの背景枠（見やすさ向上）
        text_width = len(score_text) * 4
        pyxel.rectb(x - 2, y - 2, max(text_width + 4, 50), 22, 7)
    
    def draw_final_score_display(self):
        """
        最終スコア表示の描画
        Requirements: 4.4 - 最終スコアの表示
        """
        if not self.show_final_score:
            return
        
        # 画面中央に最終スコアを表示
        final_score = self.score_manager.get_score()
        
        # 背景の描画（より大きなサイズ）
        bg_width = 240
        bg_height = 140  # 高さを増やして理由表示のスペースを確保
        bg_x = (320 - bg_width) // 2
        bg_y = (480 - bg_height) // 2
        
        pyxel.rect(bg_x, bg_y, bg_width, bg_height, 0)  # 黒い背景
        pyxel.rectb(bg_x, bg_y, bg_width, bg_height, 7)  # 白い枠
        
        # "GAME OVER" ラベル
        game_over_text = "GAME OVER"
        game_over_x = bg_x + (bg_width - len(game_over_text) * 4) // 2
        game_over_y = bg_y + 10
        pyxel.text(game_over_x, game_over_y, game_over_text, 8)  # 赤色
        
        # ゲームオーバーの理由を表示
        if hasattr(self, 'game_over_reason'):
            reason_text = f"Reason: {self.game_over_reason}"
            # 長すぎる場合は省略
            if len(reason_text) > 30:
                reason_text = reason_text[:27] + "..."
            reason_x = bg_x + (bg_width - len(reason_text) * 4) // 2
            reason_y = bg_y + 25
            pyxel.text(reason_x, reason_y, reason_text, 9)  # オレンジ色
        
        # "FINAL SCORE" ラベル
        label_text = "FINAL SCORE"
        label_x = bg_x + (bg_width - len(label_text) * 4) // 2
        label_y = bg_y + 30
        pyxel.text(label_x, label_y, label_text, 7)
        
        # 最終スコア値
        score_text = self.score_manager.format_score(final_score)
        score_x = bg_x + (bg_width - len(score_text) * 4) // 2
        score_y = bg_y + 50
        pyxel.text(score_x, score_y, score_text, 10)  # 明るい緑色
        
        # 危険レベル表示（デバッグ情報）
        danger_level = self.get_danger_level()
        if danger_level > 0:
            danger_text = f"Danger Level: {danger_level}"
            danger_x = bg_x + (bg_width - len(danger_text) * 4) // 2
            danger_y = bg_y + 70
            pyxel.text(danger_x, danger_y, danger_text, 9)  # オレンジ色
        
        # 操作説明
        instruction_text = "Press R to Restart"
        instruction_x = bg_x + (bg_width - len(instruction_text) * 4) // 2
        instruction_y = bg_y + 90
        pyxel.text(instruction_x, instruction_y, instruction_text, 7)
        
        # 追加の操作説明
        menu_text = "Press Q to Quit"
        menu_x = bg_x + (bg_width - len(menu_text) * 4) // 2
        menu_y = bg_y + 105
        pyxel.text(menu_x, menu_y, menu_text, 7)
    
    def show_final_score_screen(self):
        """
        最終スコア画面を表示する
        Requirements: 4.4 - 最終スコアの表示
        """
        self.show_final_score = True
    
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
        Requirements: 4.3 - メニュー画面での処理
        """
        # メニュー画面のBGMを再生（現在のBGMがメニューBGMでない場合）
        # Requirements: 12.3 - メニュー画面のBGM
        if self.audio_manager.current_bgm != BGMType.MENU:
            self.audio_manager.play_bgm(BGMType.MENU)
        
        # メニュー状態では自動的にプレイ状態に移行（簡易実装）
        # 将来的にはメニュー選択機能を追加
        if self.game_state_manager.get_time_in_current_state() > 60:  # 1秒後に自動開始
            # 選択音を再生
            # Requirements: 12.2 - メニュー選択時の効果音
            self.audio_manager.play_sound(SoundType.ROTATE)
            self.game_state_manager.start_game()
    
    def update_playing_logic(self):
        """
        プレイ中状態での処理
        Requirements: 4.3 - ゲームプレイ中の処理
        """
        # 高度なゲームオーバー判定
        is_game_over, reason = self.check_game_over_advanced()
        
        # ゲームオーバー判定
        if is_game_over:
            print(f"ゲームオーバー検出: {reason}")
            self.handle_game_over(reason)  # 理由を渡す
            self.game_state_manager.end_game()
            return  # ゲームオーバー後は処理を終了
        elif "危険レベル" in reason:
            # 危険レベルが高い場合は警告表示
            if self.frame_count % 60 == 0:  # 1秒ごとに警告表示
                print(f"警告: {reason}")
                
        # 新しいぷよペアが生成されたときのゲームオーバー判定は
        # check_game_over_advancedメソッドで既に行われているため、
        # ここでは追加のチェックは不要
    
    def update_game_over_logic(self):
        """
        ゲームオーバー状態での処理
        Requirements: 4.4 - ゲームオーバー画面での処理
        """
        # リスタート入力の処理
        if self.input_handler.should_restart_game():
            # リスタート効果音
            # Requirements: 12.2 - リスタート時の効果音
            self.audio_manager.play_sound(SoundType.ROTATE)
            self.restart_game()
            self.game_state_manager.restart_game()
        
        # メニューに戻る処理
        if self.input_handler.should_quit_game():
            # メニューに戻る効果音
            # Requirements: 12.2 - メニューに戻る時の効果音
            self.audio_manager.play_sound(SoundType.CLEAR)
            self.game_state_manager.return_to_menu()
    
    def restart_game(self):
        """
        ゲームを再開始する
        Requirements: 4.4 - ゲーム再開始処理
        """
        # ゲーム状態をリセット
        self.score_manager.reset()
        self.playfield.clear()
        self.current_falling_pair = self.puyo_manager.get_current_pair()
        self.show_final_score = False
        
        # 各システムの状態をリセット
        self.gravity_active = False
        self.elimination_active = False
        self.chain_active = False
        self.chain_level = 0
        self.show_chain_text = False
        
        # ゲームオーバー関連の状態をリセット
        self.game_over_reason = ""
        
        # ゲームプレイ用BGMを再生
        # Requirements: 12.3 - ゲームプレイ中のBGMループ再生
        self.audio_manager.play_bgm(BGMType.GAME)
        
        print("Game restarted!")