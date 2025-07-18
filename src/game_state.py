"""
GameStateクラス - ゲーム状態管理システム
Requirements: 4.3, 4.4 - ゲーム状態の管理と遷移制御
"""

from enum import Enum


class GameState(Enum):
    """
    ゲーム状態の列挙型
    Requirements: 4.3, 4.4 - ゲーム状態の定義
    """
    MENU = "menu"           # メニュー画面
    PLAYING = "playing"     # ゲームプレイ中
    GAME_OVER = "game_over" # ゲームオーバー画面


class GameStateManager:
    """
    ゲーム状態管理クラス - 状態遷移と処理分岐を管理
    Requirements: 4.3, 4.4 - ゲーム状態管理と遷移制御
    """
    
    def __init__(self):
        """
        GameStateManagerの初期化
        """
        self.current_state = GameState.MENU  # 初期状態はメニュー
        self.previous_state = None  # 前の状態を記録
        self.state_change_timer = 0  # 状態変更からの経過時間
        self.transition_active = False  # 状態遷移中フラグ
        
        # 状態別の設定
        self.menu_selection = 0  # メニューでの選択項目
        self.game_over_timer = 0  # ゲームオーバー画面の表示時間
        
        print(f"GameStateManager initialized - Current state: {self.current_state.value}")
    
    def get_current_state(self):
        """
        現在のゲーム状態を取得する
        
        Returns:
            GameState: 現在のゲーム状態
        """
        return self.current_state
    
    def is_state(self, state):
        """
        指定された状態かどうかを確認する
        
        Args:
            state (GameState): 確認したい状態
        
        Returns:
            bool: 指定された状態の場合True
        """
        return self.current_state == state
    
    def change_state(self, new_state):
        """
        ゲーム状態を変更する
        
        Args:
            new_state (GameState): 新しいゲーム状態
        
        Requirements: 4.3, 4.4 - 状態遷移の制御
        """
        if new_state != self.current_state:
            self.previous_state = self.current_state
            self.current_state = new_state
            self.state_change_timer = 0
            self.transition_active = True
            
            print(f"State changed: {self.previous_state.value} -> {self.current_state.value}")
            
            # 状態変更時の初期化処理
            self._on_state_enter(new_state)
    
    def _on_state_enter(self, state):
        """
        状態に入った時の初期化処理
        
        Args:
            state (GameState): 入った状態
        
        Requirements: 4.3, 4.4 - 各状態での初期化処理
        """
        if state == GameState.MENU:
            self.menu_selection = 0
            print("Entered MENU state")
        
        elif state == GameState.PLAYING:
            print("Entered PLAYING state")
        
        elif state == GameState.GAME_OVER:
            self.game_over_timer = 0
            print("Entered GAME_OVER state")
    
    def update(self):
        """
        ゲーム状態管理の更新処理
        
        Requirements: 4.3, 4.4 - 状態別の処理分岐
        """
        # 状態変更タイマーの更新
        self.state_change_timer += 1
        
        # 遷移完了判定（数フレーム後に遷移完了とする）
        if self.transition_active and self.state_change_timer >= 5:
            self.transition_active = False
        
        # 状態別の更新処理
        if self.current_state == GameState.MENU:
            self._update_menu_state()
        elif self.current_state == GameState.PLAYING:
            self._update_playing_state()
        elif self.current_state == GameState.GAME_OVER:
            self._update_game_over_state()
    
    def _update_menu_state(self):
        """
        メニュー状態の更新処理
        
        Requirements: 4.3 - メニュー画面での処理
        """
        # メニュー状態での処理（将来的に実装）
        pass
    
    def _update_playing_state(self):
        """
        プレイ中状態の更新処理
        
        Requirements: 4.3 - ゲームプレイ中の処理
        """
        # プレイ中状態での処理（将来的に実装）
        pass
    
    def _update_game_over_state(self):
        """
        ゲームオーバー状態の更新処理
        
        Requirements: 4.4 - ゲームオーバー画面での処理
        """
        self.game_over_timer += 1
    
    def can_transition_to(self, target_state):
        """
        指定された状態に遷移可能かどうかを確認する
        
        Args:
            target_state (GameState): 遷移先の状態
        
        Returns:
            bool: 遷移可能な場合True
        
        Requirements: 4.3, 4.4 - 状態遷移の制御
        """
        # 現在遷移中の場合は新しい遷移を許可しない
        if self.transition_active:
            return False
        
        # 同じ状態への遷移は不要
        if target_state == self.current_state:
            return False
        
        # 状態遷移のルールを定義
        valid_transitions = {
            GameState.MENU: [GameState.PLAYING],  # メニューからプレイへ
            GameState.PLAYING: [GameState.GAME_OVER, GameState.MENU],  # プレイからゲームオーバーまたはメニューへ
            GameState.GAME_OVER: [GameState.MENU, GameState.PLAYING]  # ゲームオーバーからメニューまたはプレイへ
        }
        
        return target_state in valid_transitions.get(self.current_state, [])
    
    def start_game(self):
        """
        ゲームを開始する（メニューからプレイ状態へ）
        
        Requirements: 4.3 - ゲーム開始処理
        """
        if self.can_transition_to(GameState.PLAYING):
            self.change_state(GameState.PLAYING)
            return True
        return False
    
    def end_game(self):
        """
        ゲームを終了する（プレイ状態からゲームオーバーへ）
        
        Requirements: 4.4 - ゲーム終了処理
        """
        if self.can_transition_to(GameState.GAME_OVER):
            self.change_state(GameState.GAME_OVER)
            return True
        return False
    
    def return_to_menu(self):
        """
        メニューに戻る
        
        Requirements: 4.3, 4.4 - メニューへの遷移
        """
        if self.can_transition_to(GameState.MENU):
            self.change_state(GameState.MENU)
            return True
        return False
    
    def restart_game(self):
        """
        ゲームを再開始する（ゲームオーバーからプレイ状態へ）
        
        Requirements: 4.4 - ゲーム再開始処理
        """
        if self.can_transition_to(GameState.PLAYING):
            self.change_state(GameState.PLAYING)
            return True
        return False
    
    def get_state_info(self):
        """
        現在の状態情報を取得する（デバッグ用）
        
        Returns:
            dict: 状態情報
        """
        return {
            'current_state': self.current_state.value,
            'previous_state': self.previous_state.value if self.previous_state else None,
            'state_change_timer': self.state_change_timer,
            'transition_active': self.transition_active,
            'menu_selection': self.menu_selection,
            'game_over_timer': self.game_over_timer
        }
    
    def is_in_transition(self):
        """
        状態遷移中かどうかを確認する
        
        Returns:
            bool: 遷移中の場合True
        """
        return self.transition_active
    
    def get_time_in_current_state(self):
        """
        現在の状態にいる時間を取得する
        
        Returns:
            int: 現在の状態にいるフレーム数
        """
        return self.state_change_timer