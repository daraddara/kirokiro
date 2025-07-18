"""
音響管理システム - BGMと効果音の再生・制御を管理
Requirements: 12.1 - AudioManagerクラスの実装
"""

import pyxel
from enum import Enum


class SoundType(Enum):
    """効果音の種類"""
    MOVE = "move"           # ぷよ移動音
    ROTATE = "rotate"       # ぷよ回転音
    LAND = "land"           # ぷよ着地音
    CLEAR = "clear"         # ぷよ消去音
    CHAIN = "chain"         # 連鎖音
    GAME_OVER = "game_over" # ゲームオーバー音


class BGMType(Enum):
    """BGMの種類"""
    MENU = "menu"           # メニュー画面BGM
    GAME = "game"           # ゲームプレイBGM
    GAME_OVER = "game_over" # ゲームオーバーBGM


class AudioManager:
    """
    音響管理クラス
    BGMと効果音の再生・停止・音量制御を管理
    Requirements: 12.1 - 音響管理システムの基本構造
    """
    
    def __init__(self):
        """
        AudioManagerの初期化
        """
        # BGM関連の状態
        self.bgm_playing = False
        self.current_bgm = None
        self.bgm_volume = 0.7  # BGM音量 (0.0-1.0)
        
        # 効果音関連の状態
        self.sound_enabled = True
        self.sound_volume = 0.8  # 効果音音量 (0.0-1.0)
        
        # 音響データの定義
        self.bgm_data = {}
        self.sound_data = {}
        
        # 音響データの初期化
        self._initialize_audio_data()
        
        # フェード関連
        self.fade_active = False
        self.fade_duration = 0
        self.fade_timer = 0
        self.fade_start_volume = 0
        self.fade_target_volume = 0
        self.fade_callback = None
    
    def _initialize_audio_data(self):
        """
        音響データの初期化
        Pyxelの音響システムに合わせて音楽と効果音を定義
        """
        # BGMデータの定義（Pyxelの音楽チャンネル0-3を使用）
        self.bgm_data = {
            BGMType.MENU: {
                'channel': 0,
                'notes': [
                    # シンプルなメニュー用メロディ
                    "c3e3g3c4",  # ド・ミ・ソ・ド（オクターブ上）
                ],
                'tempo': 120,
                'loop': True
            },
            BGMType.GAME: {
                'channel': 0,
                'notes': [
                    # ゲームプレイ用のリズミカルなメロディ
                    "c3d3e3f3g3a3b3c4",  # ドレミファソラシド
                    "c4b3a3g3f3e3d3c3",  # 逆順
                ],
                'tempo': 140,
                'loop': True
            },
            BGMType.GAME_OVER: {
                'channel': 0,
                'notes': [
                    # ゲームオーバー用の短いメロディ
                    "c4a3f3d3c3",  # 下降メロディ
                ],
                'tempo': 80,
                'loop': False
            }
        }
        
        # 効果音データの定義（Pyxelの音響チャンネル1-3を使用）
        self.sound_data = {
            SoundType.MOVE: {
                'channel': 1,
                'note': "c4",
                'duration': 5,
                'volume': 0.3
            },
            SoundType.ROTATE: {
                'channel': 1,
                'note': "e4",
                'duration': 8,
                'volume': 0.4
            },
            SoundType.LAND: {
                'channel': 2,
                'note': "g3",
                'duration': 15,
                'volume': 0.5
            },
            SoundType.CLEAR: {
                'channel': 2,
                'note': "c5",
                'duration': 20,
                'volume': 0.6
            },
            SoundType.CHAIN: {
                'channel': 3,
                'note': "g5",
                'duration': 25,
                'volume': 0.7
            },
            SoundType.GAME_OVER: {
                'channel': 3,
                'note': "c2",
                'duration': 60,
                'volume': 0.8
            }
        }
    
    def play_bgm(self, bgm_type: BGMType):
        """
        BGMを再生する
        Args:
            bgm_type (BGMType): 再生するBGMの種類
        Requirements: 12.1 - BGM再生機能
        """
        if not isinstance(bgm_type, BGMType):
            print(f"Warning: Invalid BGM type: {bgm_type}")
            return
        
        # 現在のBGMを停止
        self.stop_bgm()
        
        # 新しいBGMを再生
        bgm_info = self.bgm_data.get(bgm_type)
        if bgm_info:
            try:
                # Pyxelの音楽システムを使用してBGMを再生
                # 実際の実装では、より複雑な音楽データを使用する可能性があります
                channel = bgm_info['channel']
                notes = bgm_info['notes']
                
                # 簡単な音楽再生（実際のPyxelでは音楽データを事前に定義する必要があります）
                # ここでは概念的な実装を示します
                self.current_bgm = bgm_type
                self.bgm_playing = True
                
                print(f"Playing BGM: {bgm_type.value}")
                
            except Exception as e:
                print(f"Error playing BGM {bgm_type.value}: {e}")
                self.bgm_playing = False
                self.current_bgm = None
    
    def stop_bgm(self):
        """
        BGMを停止する
        Requirements: 12.1 - BGM停止機能
        """
        if self.bgm_playing and self.current_bgm:
            try:
                # Pyxelの音楽停止
                bgm_info = self.bgm_data.get(self.current_bgm)
                if bgm_info:
                    channel = bgm_info['channel']
                    # pyxel.stop(channel)  # 実際のPyxelでの停止処理
                
                print(f"Stopped BGM: {self.current_bgm.value}")
                
            except Exception as e:
                print(f"Error stopping BGM: {e}")
            
            finally:
                self.bgm_playing = False
                self.current_bgm = None
    
    def play_sound(self, sound_type: SoundType, chain_level: int = 1):
        """
        効果音を再生する
        Args:
            sound_type (SoundType): 再生する効果音の種類
            chain_level (int): 連鎖レベル（連鎖音の音程調整用）
        Requirements: 12.1 - 効果音再生システム
        """
        if not self.sound_enabled:
            return
        
        if not isinstance(sound_type, SoundType):
            print(f"Warning: Invalid sound type: {sound_type}")
            return
        
        sound_info = self.sound_data.get(sound_type)
        if not sound_info:
            print(f"Warning: Sound data not found for: {sound_type.value}")
            return
        
        try:
            channel = sound_info['channel']
            note = sound_info['note']
            duration = sound_info['duration']
            volume = sound_info['volume'] * self.sound_volume
            
            # 連鎖音の場合は連鎖レベルに応じて音程を上げる
            if sound_type == SoundType.CHAIN and chain_level > 1:
                # 連鎖レベルに応じて音程を調整（簡易実装）
                base_note = note[0]  # 'g'
                octave = int(note[1]) if len(note) > 1 else 4
                
                # 連鎖レベルに応じてオクターブを上げる
                new_octave = min(octave + (chain_level - 1), 7)
                note = f"{base_note}{new_octave}"
            
            # Pyxelの効果音再生
            # 実際の実装では pyxel.sound() や pyxel.play() を使用
            print(f"Playing sound: {sound_type.value} (note: {note}, duration: {duration}, volume: {volume:.2f})")
            
        except Exception as e:
            print(f"Error playing sound {sound_type.value}: {e}")
    
    def set_bgm_volume(self, volume: float):
        """
        BGM音量を設定する
        Args:
            volume (float): 音量 (0.0-1.0)
        Requirements: 12.1 - 音量制御機能
        """
        self.bgm_volume = max(0.0, min(1.0, volume))
        print(f"BGM volume set to: {self.bgm_volume:.2f}")
        
        # 現在再生中のBGMの音量を更新
        if self.bgm_playing:
            # 実際の実装では、Pyxelの音量制御APIを使用
            pass
    
    def set_sound_volume(self, volume: float):
        """
        効果音音量を設定する
        Args:
            volume (float): 音量 (0.0-1.0)
        Requirements: 12.1 - 音量制御機能
        """
        self.sound_volume = max(0.0, min(1.0, volume))
        print(f"Sound volume set to: {self.sound_volume:.2f}")
    
    def set_master_volume(self, volume: float):
        """
        マスター音量を設定する（BGMと効果音の両方）
        Args:
            volume (float): 音量 (0.0-1.0)
        """
        self.set_bgm_volume(volume)
        self.set_sound_volume(volume)
    
    def toggle_sound(self):
        """
        効果音の有効/無効を切り替える
        Returns:
            bool: 切り替え後の効果音有効状態
        """
        self.sound_enabled = not self.sound_enabled
        print(f"Sound {'enabled' if self.sound_enabled else 'disabled'}")
        return self.sound_enabled
    
    def fade_bgm(self, target_volume: float, duration_frames: int, callback=None):
        """
        BGMをフェードイン/フェードアウトする
        Args:
            target_volume (float): 目標音量 (0.0-1.0)
            duration_frames (int): フェード時間（フレーム数）
            callback (callable): フェード完了時のコールバック関数
        """
        if not self.bgm_playing:
            return
        
        self.fade_active = True
        self.fade_duration = duration_frames
        self.fade_timer = 0
        self.fade_start_volume = self.bgm_volume
        self.fade_target_volume = max(0.0, min(1.0, target_volume))
        self.fade_callback = callback
        
        print(f"Starting BGM fade from {self.fade_start_volume:.2f} to {self.fade_target_volume:.2f} over {duration_frames} frames")
    
    def update(self):
        """
        AudioManagerの更新処理（毎フレーム呼び出し）
        フェード処理などの時間ベースの処理を実行
        """
        # フェード処理
        if self.fade_active:
            self.fade_timer += 1
            
            if self.fade_timer >= self.fade_duration:
                # フェード完了
                self.set_bgm_volume(self.fade_target_volume)
                self.fade_active = False
                
                # コールバック実行
                if self.fade_callback:
                    self.fade_callback()
                    self.fade_callback = None
                
                print("BGM fade completed")
            else:
                # フェード中の音量計算
                progress = self.fade_timer / self.fade_duration
                current_volume = self.fade_start_volume + (self.fade_target_volume - self.fade_start_volume) * progress
                self.set_bgm_volume(current_volume)
    
    def get_status(self):
        """
        現在の音響システムの状態を取得する
        Returns:
            dict: 音響システムの状態情報
        """
        return {
            'bgm_playing': self.bgm_playing,
            'current_bgm': self.current_bgm.value if self.current_bgm else None,
            'bgm_volume': self.bgm_volume,
            'sound_enabled': self.sound_enabled,
            'sound_volume': self.sound_volume,
            'fade_active': self.fade_active
        }
    
    def cleanup(self):
        """
        AudioManagerのクリーンアップ処理
        ゲーム終了時に呼び出される
        """
        print("Cleaning up AudioManager...")
        
        # BGM停止
        self.stop_bgm()
        
        # フェード処理停止
        self.fade_active = False
        self.fade_callback = None
        
        print("AudioManager cleanup completed")