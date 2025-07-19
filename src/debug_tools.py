"""
Debug Tools - デバッグとテスト機能
Requirements: 3.1, 5.2, 5.3 - デバッグ機能とテスト用操作
"""

from src.puyo import Puyo


class DebugTools:
    """
    デバッグツール - テスト機能とデバッグ出力を管理
    """
    
    def __init__(self, playfield, game_systems):
        """
        DebugToolsの初期化
        
        Args:
            playfield: プレイフィールド
            game_systems: ゲームシステム管理
        """
        self.playfield = playfield
        self.game_systems = game_systems
        self.debug_mode = False
    
    def debug_print(self, message):
        """
        デバッグモードでのみメッセージを出力する
        
        Args:
            message (str): 出力するメッセージ
        """
        if self.debug_mode:
            print(message)
    
    def test_connection_detection(self):
        """
        連結判定のテスト機能
        Requirements: 3.1 - 連結グループの検出とdebug_print出力
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
        Requirements: 3.1, 5.2 - 消去処理のテストとdebug_print出力
        """
        # テスト用の消去可能なぷよを配置
        # 4つの赤いぷよを2x2で配置
        test_positions = [(0, 8), (0, 9), (1, 8), (1, 9)]
        for x, y in test_positions:
            if self.playfield.is_empty(x, y):
                self.playfield.place_puyo(x, y, Puyo(1))  # 赤いぷよ
        
        # 消去処理を開始
        self.game_systems.start_elimination_process()
        
        print("=== 消去処理テスト実行 ===")
        print("4つの赤いぷよを左上に配置して消去処理を開始しました")
    
    def test_chain_animation(self):
        """
        連鎖アニメーションのテスト機能
        Requirements: 5.3 - 連鎖数の視覚的表示のテスト
        """
        # 連鎖レベルを循環させる（1-5連鎖）
        if not self.game_systems.show_chain_text:
            # アニメーションが表示されていない場合、1連鎖から開始
            self.game_systems.chain_level = 1
        else:
            # 既に表示中の場合、次のレベルに進む
            self.game_systems.chain_level += 1
            if self.game_systems.chain_level > 5:
                self.game_systems.chain_level = 1
        
        # 連鎖アニメーションを開始
        self.game_systems.show_chain_text = True
        self.game_systems.chain_display_timer = 0
        self.game_systems.chain_animation_phase = 0
        
        print(f"=== 連鎖アニメーションテスト実行 ===")
        print(f"{self.game_systems.chain_level}連鎖のアニメーションを表示します")
    
    def test_gravity(self):
        """
        重力処理のテスト機能
        """
        self.game_systems.apply_gravity_after_fixation()
        print("=== 重力処理テスト実行 ===")
        print("重力処理を手動で開始しました")