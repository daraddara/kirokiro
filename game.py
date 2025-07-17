import pyxel
from puyo import Puyo
from puyo_pair import PuyoPair
from playfield import PlayField
from input_handler import InputHandler
from puyo_manager import PuyoManager


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
        self.fall_timer = 0  # 自動落下タイマー
        self.fall_interval = 60  # 通常の落下間隔（60フレーム = 1秒）
        self.fast_fall_interval = 3  # 高速落下間隔（3フレーム）
        
        # 現在操作中のぷよペア
        self.current_falling_pair = None
        
        # テスト用のぷよを作成（Puyoクラスの動作確認用）
        self.test_puyos = [
            Puyo(1, 0, 0),  # 赤いぷよ
            Puyo(2, 1, 0),  # オレンジのぷよ
            Puyo(3, 2, 0),  # 緑のぷよ
            Puyo(4, 3, 0),  # 青いぷよ
        ]
        
        # テスト用のプレイフィールドを作成（PlayFieldクラスの動作確認用）
        self.playfield = PlayField()
        
        # プレイフィールドにテスト用ぷよを配置
        self.playfield.place_puyo(1, 10, Puyo(2))  # オレンジのぷよを下部に配置
        self.playfield.place_puyo(2, 11, Puyo(4))  # 青いぷよを最下段に配置
        self.playfield.place_puyo(3, 10, Puyo(1))  # 赤いぷよを下部に配置
        self.playfield.place_puyo(4, 11, Puyo(3))  # 緑のぷよを最下段に配置
        
        # 入力処理システムを作成（InputHandlerクラスの動作確認用）
        self.input_handler = InputHandler()
        
        # ぷよ管理システムを作成（PuyoManagerクラスの動作確認用）
        self.puyo_manager = PuyoManager()
        
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
            # 消去処理を開始
            self.elimination_active = True
            self.elimination_timer = 0
            self.elimination_groups = erasable_groups
            
            # デバッグ情報
            print(f"消去処理開始: {len(erasable_groups)}グループ、{sum(len(group) for group in erasable_groups)}個のぷよ")
        else:
            # 消去するものがない場合は重力処理に移行
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
        Requirements: 3.4 - 連鎖判定（将来の実装のための準備）
        """
        # 重力処理後に新たな消去可能グループがあるかチェック
        erasable_groups = self.playfield.find_erasable_groups()
        
        if erasable_groups:
            # 連鎖発生！再度消去処理を開始
            print(f"連鎖発生！{len(erasable_groups)}グループが新たに消去可能")
            self.start_elimination_process()
        else:
            # 連鎖終了、通常のゲーム状態に戻る
            print("消去・重力処理完了")
    
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
        
        if self.input_handler.should_move_right():
            if self.playfield.can_move_puyo_pair(self.current_falling_pair, 1, 0):
                self.current_falling_pair.move(1, 0)
        
        # 回転の処理（キックシステム付き）
        if self.input_handler.should_rotate_clockwise():
            self.playfield.rotate_puyo_pair_with_kick(self.current_falling_pair, True)
        
        if self.input_handler.should_rotate_counterclockwise():
            self.playfield.rotate_puyo_pair_with_kick(self.current_falling_pair, False)
        
        # 高速落下の処理（個別の下移動）
        if self.input_handler.should_fast_drop():
            if self.playfield.can_move_puyo_pair(self.current_falling_pair, 0, 1):
                self.current_falling_pair.move(0, 1)
                self.fall_timer = 0  # タイマーリセット
    
    def update(self):
        """
        ゲーム状態の更新処理（毎フレーム呼び出される）
        Requirements: 1.1 - システムは対応するゲーム操作を実行する
        """
        # フレームカウンターの更新
        self.frame_count += 1
        
        # 入力処理の更新
        self.input_handler.update()
        
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
        
        # 消去システムの更新
        # Requirements: 3.1, 5.2 - 消去処理とアニメーション
        self.update_elimination_system()
        
        # 重力システムの更新
        # Requirements: 3.3 - 浮いているぷよの落下処理、重力処理のアニメーション
        self.update_gravity_system()
        
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
    
    def draw(self):
        """
        画面描画処理（毎フレーム呼び出される）
        Requirements: 1.1 - システムはゲーム画面を表示する
        Requirements: 1.2 - システムはプレイフィールドとぷよを表示する
        """
        # 画面をクリア（黒色 - デザイン文書の色定義に基づく）
        pyxel.cls(0)
        
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
        
        # プレイフィールドの描画（PlayFieldクラスの動作確認）
        self.playfield.draw(playfield_x, playfield_y)
        
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
        
        # テスト用ぷよの描画（Puyoクラスの動作確認）
        for i, puyo in enumerate(self.test_puyos):
            # プレイフィールド内の位置に描画
            screen_x = playfield_x + (i * 24)  # 24ピクセル間隔で配置
            screen_y = playfield_y + 24  # プレイフィールドの上から2行目
            puyo.draw(screen_x, screen_y)
        
        # 現在落下中のぷよペアの描画
        if self.current_falling_pair is not None:
            self.current_falling_pair.draw(playfield_x, playfield_y)
        
        # 次のぷよペアのプレビュー表示（PuyoManagerクラスの動作確認）
        next_preview_x = playfield_x + playfield_width + 20
        next_preview_y = playfield_y + 20
        
        # "NEXT" ラベルの表示
        pyxel.text(next_preview_x, next_preview_y - 15, "NEXT:", 7)
        
        # 次のペアのプレビューを描画
        self.puyo_manager.draw_next_pair_preview(next_preview_x, next_preview_y)
        
        # 操作説明の表示
        pyxel.text(50, 400, "Controls:", 7)
        pyxel.text(50, 410, "Arrow Keys: Move/Drop", 7)
        pyxel.text(50, 420, "X/UP: Rotate CW, Z: Rotate CCW", 7)
        pyxel.text(50, 430, "Q/ESC: Quit Game", 7)
        pyxel.text(50, 440, "G: Test Gravity", 7)
        pyxel.text(50, 450, "C: Test Connection", 7)
        pyxel.text(50, 460, "Test Pair: Red+Green (controllable)", 7)
        
        # デバッグ情報の表示
        pyxel.text(10, 10, f"Frame: {self.frame_count}", 7)
        
        # 重力処理状態の表示
        if self.gravity_active:
            pyxel.text(10, 20, "GRAVITY ACTIVE", 8)  # 赤色で表示
        else:
            pyxel.text(10, 20, "Gravity: Idle", 7)   # 白色で表示
        
        # 消去処理状態の表示
        if self.elimination_active:
            pyxel.text(10, 30, "ELIMINATION ACTIVE", 9)  # オレンジ色で表示
        else:
            pyxel.text(10, 30, "Elimination: Idle", 7)   # 白色で表示
        
        # 現在のぷよペア状態の表示
        if self.current_falling_pair is not None:
            pair_pos = self.current_falling_pair.get_position()
            pyxel.text(10, 40, f"Pair: ({pair_pos[0]}, {pair_pos[1]})", 7)
        else:
            pyxel.text(10, 40, "Pair: None", 7)