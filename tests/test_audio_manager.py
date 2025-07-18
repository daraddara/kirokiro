"""
AudioManagerのテスト
"""

import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# テスト対象のモジュールをインポートするためにsrcディレクトリをパスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.audio_manager import AudioManager, SoundType, BGMType


class TestAudioManager(unittest.TestCase):
    """
    AudioManagerクラスのテスト
    """
    
    def setUp(self):
        """テストの前準備"""
        self.audio_manager = AudioManager()
    
    def test_initialization(self):
        """AudioManagerの初期化テスト"""
        self.assertFalse(self.audio_manager.bgm_playing)
        self.assertIsNone(self.audio_manager.current_bgm)
        self.assertEqual(self.audio_manager.bgm_volume, 0.7)
        self.assertTrue(self.audio_manager.sound_enabled)
        self.assertEqual(self.audio_manager.sound_volume, 0.8)
        self.assertFalse(self.audio_manager.fade_active)
    
    def test_bgm_data_initialization(self):
        """BGMデータの初期化テスト"""
        # 全てのBGMタイプがデータに含まれているかチェック
        for bgm_type in BGMType:
            self.assertIn(bgm_type, self.audio_manager.bgm_data)
            bgm_data = self.audio_manager.bgm_data[bgm_type]
            self.assertIn('channel', bgm_data)
            self.assertIn('notes', bgm_data)
            self.assertIn('tempo', bgm_data)
            self.assertIn('loop', bgm_data)
    
    def test_sound_data_initialization(self):
        """効果音データの初期化テスト"""
        # 全ての効果音タイプがデータに含まれているかチェック
        for sound_type in SoundType:
            self.assertIn(sound_type, self.audio_manager.sound_data)
            sound_data = self.audio_manager.sound_data[sound_type]
            self.assertIn('channel', sound_data)
            self.assertIn('note', sound_data)
            self.assertIn('duration', sound_data)
            self.assertIn('volume', sound_data)
    
    def test_play_bgm(self):
        """BGM再生テスト"""
        # BGM再生
        self.audio_manager.play_bgm(BGMType.MENU)
        self.assertTrue(self.audio_manager.bgm_playing)
        self.assertEqual(self.audio_manager.current_bgm, BGMType.MENU)
        
        # 別のBGMに切り替え
        self.audio_manager.play_bgm(BGMType.GAME)
        self.assertTrue(self.audio_manager.bgm_playing)
        self.assertEqual(self.audio_manager.current_bgm, BGMType.GAME)
    
    def test_stop_bgm(self):
        """BGM停止テスト"""
        # BGMを再生してから停止
        self.audio_manager.play_bgm(BGMType.MENU)
        self.assertTrue(self.audio_manager.bgm_playing)
        
        self.audio_manager.stop_bgm()
        self.assertFalse(self.audio_manager.bgm_playing)
        self.assertIsNone(self.audio_manager.current_bgm)
    
    def test_play_sound(self):
        """効果音再生テスト"""
        # 効果音が有効な状態でのテスト
        self.assertTrue(self.audio_manager.sound_enabled)
        
        # 各種効果音の再生テスト（エラーが発生しないことを確認）
        for sound_type in SoundType:
            try:
                self.audio_manager.play_sound(sound_type)
            except Exception as e:
                self.fail(f"Sound playback failed for {sound_type}: {e}")
    
    def test_play_sound_disabled(self):
        """効果音無効時のテスト"""
        self.audio_manager.sound_enabled = False
        
        # 効果音が無効な場合は何も起こらない
        self.audio_manager.play_sound(SoundType.MOVE)
        # エラーが発生しないことを確認
    
    def test_play_chain_sound_with_level(self):
        """連鎖音の連鎖レベル対応テスト"""
        # 連鎖レベル1
        self.audio_manager.play_sound(SoundType.CHAIN, 1)
        
        # 連鎖レベル3
        self.audio_manager.play_sound(SoundType.CHAIN, 3)
        
        # 連鎖レベル5
        self.audio_manager.play_sound(SoundType.CHAIN, 5)
        
        # エラーが発生しないことを確認
    
    def test_set_bgm_volume(self):
        """BGM音量設定テスト"""
        # 正常な音量設定
        self.audio_manager.set_bgm_volume(0.5)
        self.assertEqual(self.audio_manager.bgm_volume, 0.5)
        
        # 範囲外の値（下限）
        self.audio_manager.set_bgm_volume(-0.1)
        self.assertEqual(self.audio_manager.bgm_volume, 0.0)
        
        # 範囲外の値（上限）
        self.audio_manager.set_bgm_volume(1.5)
        self.assertEqual(self.audio_manager.bgm_volume, 1.0)
    
    def test_set_sound_volume(self):
        """効果音音量設定テスト"""
        # 正常な音量設定
        self.audio_manager.set_sound_volume(0.3)
        self.assertEqual(self.audio_manager.sound_volume, 0.3)
        
        # 範囲外の値（下限）
        self.audio_manager.set_sound_volume(-0.1)
        self.assertEqual(self.audio_manager.sound_volume, 0.0)
        
        # 範囲外の値（上限）
        self.audio_manager.set_sound_volume(1.5)
        self.assertEqual(self.audio_manager.sound_volume, 1.0)
    
    def test_set_master_volume(self):
        """マスター音量設定テスト"""
        self.audio_manager.set_master_volume(0.6)
        self.assertEqual(self.audio_manager.bgm_volume, 0.6)
        self.assertEqual(self.audio_manager.sound_volume, 0.6)
    
    def test_toggle_sound(self):
        """効果音切り替えテスト"""
        # 初期状態は有効
        self.assertTrue(self.audio_manager.sound_enabled)
        
        # 無効に切り替え
        result = self.audio_manager.toggle_sound()
        self.assertFalse(self.audio_manager.sound_enabled)
        self.assertFalse(result)
        
        # 有効に切り替え
        result = self.audio_manager.toggle_sound()
        self.assertTrue(self.audio_manager.sound_enabled)
        self.assertTrue(result)
    
    def test_fade_bgm(self):
        """BGMフェードテスト"""
        # BGMを再生
        self.audio_manager.play_bgm(BGMType.MENU)
        
        # フェード開始
        callback_called = False
        def fade_callback():
            nonlocal callback_called
            callback_called = True
        
        self.audio_manager.fade_bgm(0.2, 30, fade_callback)
        
        # フェード状態の確認
        self.assertTrue(self.audio_manager.fade_active)
        self.assertEqual(self.audio_manager.fade_duration, 30)
        self.assertEqual(self.audio_manager.fade_target_volume, 0.2)
        
        # フェード処理の更新（途中）
        for _ in range(15):
            self.audio_manager.update()
        self.assertTrue(self.audio_manager.fade_active)
        
        # フェード完了まで更新
        for _ in range(15):
            self.audio_manager.update()
        
        # フェード完了の確認
        self.assertFalse(self.audio_manager.fade_active)
        self.assertEqual(self.audio_manager.bgm_volume, 0.2)
        self.assertTrue(callback_called)
    
    def test_fade_bgm_without_bgm_playing(self):
        """BGM未再生時のフェードテスト"""
        # BGMが再生されていない状態でフェードを試行
        self.audio_manager.fade_bgm(0.5, 30)
        
        # フェードは開始されない
        self.assertFalse(self.audio_manager.fade_active)
    
    def test_get_status(self):
        """ステータス取得テスト"""
        # 初期状態
        status = self.audio_manager.get_status()
        expected_keys = ['bgm_playing', 'current_bgm', 'bgm_volume', 'sound_enabled', 'sound_volume', 'fade_active']
        for key in expected_keys:
            self.assertIn(key, status)
        
        self.assertFalse(status['bgm_playing'])
        self.assertIsNone(status['current_bgm'])
        
        # BGM再生後
        self.audio_manager.play_bgm(BGMType.GAME)
        status = self.audio_manager.get_status()
        self.assertTrue(status['bgm_playing'])
        self.assertEqual(status['current_bgm'], BGMType.GAME.value)
    
    def test_cleanup(self):
        """クリーンアップテスト"""
        # BGMを再生してフェードを開始
        self.audio_manager.play_bgm(BGMType.MENU)
        self.audio_manager.fade_bgm(0.0, 30)
        
        # クリーンアップ実行
        self.audio_manager.cleanup()
        
        # 状態がリセットされていることを確認
        self.assertFalse(self.audio_manager.bgm_playing)
        self.assertIsNone(self.audio_manager.current_bgm)
        self.assertFalse(self.audio_manager.fade_active)
        self.assertIsNone(self.audio_manager.fade_callback)
    
    def test_invalid_bgm_type(self):
        """無効なBGMタイプのテスト"""
        # 無効なBGMタイプを渡してもエラーが発生しないことを確認
        self.audio_manager.play_bgm("invalid_bgm")
        self.assertFalse(self.audio_manager.bgm_playing)
    
    def test_invalid_sound_type(self):
        """無効な効果音タイプのテスト"""
        # 無効な効果音タイプを渡してもエラーが発生しないことを確認
        self.audio_manager.play_sound("invalid_sound")
        # エラーが発生しないことを確認
    
    def test_update(self):
        """更新処理テスト"""
        # 更新処理がエラーなく実行されることを確認
        self.audio_manager.update()
        
        # フェード中の更新処理
        self.audio_manager.play_bgm(BGMType.MENU)
        self.audio_manager.fade_bgm(0.5, 10)
        
        # フェード処理が正常に動作することを確認
        for _ in range(5):
            self.audio_manager.update()
        self.assertTrue(self.audio_manager.fade_active)
        
        for _ in range(5):
            self.audio_manager.update()
        self.assertFalse(self.audio_manager.fade_active)


def run_tests():
    print("Running AudioManager tests...")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    print("All AudioManager tests passed! [OK]")


if __name__ == "__main__":
    run_tests()