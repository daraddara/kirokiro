# -*- coding: utf-8 -*-
"""
AudioManagerのテスト
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.audio_manager import AudioManager

def test_audio_manager_initialization():
    """AudioManagerの初期化テスト"""
    print("Running audio manager initialization test...")
    audio_manager = AudioManager()
    print("[OK] AudioManager initialization test passed")

def test_bgm_playback():
    """BGM再生テスト"""
    print("Running BGM playback test...")
    audio_manager = AudioManager()
    audio_manager.play_bgm("game")
    print("[OK] BGM playback test passed")

def test_sound_effect_playback():
    """効果音再生テスト"""
    print("Running sound effect playback test...")
    audio_manager = AudioManager()
    audio_manager.play_sound("move")
    print("[OK] Sound effect playback test passed")

if __name__ == "__main__":
    test_audio_manager_initialization()
    test_bgm_playback()
    test_sound_effect_playback()
    print("Audio manager test passed! [OK]")
