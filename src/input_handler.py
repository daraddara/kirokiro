import pyxel


class InputHandler:
    """
    入力処理クラス - キーボード入力の検出と処理
    Requirements: 1.3, 2.1, 2.2, 2.3, 2.4 - 入力処理システム
    """
    
    def __init__(self):
        """
        InputHandlerの初期化
        """
        # キーリピート用のタイマー
        self.left_repeat_timer = 0
        self.right_repeat_timer = 0
        self.down_repeat_timer = 0
        
        # キーリピートの設定（操作感改善）
        # Requirements: 14.2 - 操作感の調整
        self.repeat_delay = 10  # 初回リピートまでのフレーム数（15→10に短縮）
        self.repeat_interval = 2  # リピート間隔のフレーム数（3→2に短縮）
        
        # 高速落下の設定
        self.fast_drop_interval = 1  # 高速落下時のフレーム間隔（2→1に短縮）
    
    def update(self):
        """
        入力状態の更新（毎フレーム呼び出し）
        """
        # 左右移動のリピートタイマー更新
        if pyxel.btn(pyxel.KEY_LEFT):
            self.left_repeat_timer += 1
        else:
            self.left_repeat_timer = 0
            
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.right_repeat_timer += 1
        else:
            self.right_repeat_timer = 0
            
        # 下キー（高速落下）のリピートタイマー更新
        if pyxel.btn(pyxel.KEY_DOWN):
            self.down_repeat_timer += 1
        else:
            self.down_repeat_timer = 0
    
    def should_move_left(self):
        """
        左移動を実行すべきかチェック
        
        Returns:
            bool: 左移動を実行する場合True
        """
        if pyxel.btnp(pyxel.KEY_LEFT):
            return True
        
        # キーリピート処理
        if self.left_repeat_timer > self.repeat_delay:
            if (self.left_repeat_timer - self.repeat_delay) % self.repeat_interval == 0:
                return True
        
        return False
    
    def should_move_right(self):
        """
        右移動を実行すべきかチェック
        
        Returns:
            bool: 右移動を実行する場合True
        """
        if pyxel.btnp(pyxel.KEY_RIGHT):
            return True
        
        # キーリピート処理
        if self.right_repeat_timer > self.repeat_delay:
            if (self.right_repeat_timer - self.repeat_delay) % self.repeat_interval == 0:
                return True
        
        return False
    
    def should_rotate_clockwise(self):
        """
        時計回り回転を実行すべきかチェック
        
        Returns:
            bool: 時計回り回転を実行する場合True
        """
        return pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.KEY_UP)
    
    def should_rotate_counterclockwise(self):
        """
        反時計回り回転を実行すべきかチェック
        
        Returns:
            bool: 反時計回り回転を実行する場合True
        """
        return pyxel.btnp(pyxel.KEY_Z)
    
    def should_fast_drop(self):
        """
        高速落下を実行すべきかチェック
        
        Returns:
            bool: 高速落下を実行する場合True
        """
        if pyxel.btnp(pyxel.KEY_DOWN):
            return True
        
        # 高速落下のリピート処理
        if self.down_repeat_timer > self.repeat_delay:
            if (self.down_repeat_timer - self.repeat_delay) % self.fast_drop_interval == 0:
                return True
        
        return False
    
    def should_quit_game(self):
        """
        ゲーム終了を実行すべきかチェック
        
        Returns:
            bool: ゲーム終了する場合True
        """
        return pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.KEY_ESCAPE)
    
    def should_test_gravity(self):
        """
        重力テストを実行すべきかチェック（デバッグ用）
        
        Returns:
            bool: 重力テストを実行する場合True
        """
        return pyxel.btnp(pyxel.KEY_G)
    
    def should_test_connection(self):
        """
        連結判定テストを実行すべきかチェック（デバッグ用）
        
        Returns:
            bool: 連結判定テストを実行する場合True
        """
        return pyxel.btnp(pyxel.KEY_C)
    
    def should_test_elimination(self):
        """
        消去処理テストを実行すべきかチェック（デバッグ用）
        
        Returns:
            bool: 消去処理テストを実行する場合True
        """
        return pyxel.btnp(pyxel.KEY_E)
    
    def should_test_chain_animation(self):
        """
        連鎖アニメーションテストを実行すべきかチェック（デバッグ用）
        
        Returns:
            bool: 連鎖アニメーションテストを実行する場合True
        """
        return pyxel.btnp(pyxel.KEY_A)
    
    def should_restart_game(self):
        """
        ゲーム再開始を実行すべきかチェック
        
        Returns:
            bool: ゲーム再開始する場合True
        
        Requirements: 4.4 - ゲーム再開始処理
        """
        return pyxel.btnp(pyxel.KEY_R)