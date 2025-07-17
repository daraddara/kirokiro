"""
Test runner script - 全てのテストを実行する
Requirements: 全システムの動作確認とリグレッション防止
"""

import subprocess
import sys


def run_test_file(test_file):
    """テストファイルを実行し、結果を返す"""
    try:
        print(f"\n{'='*60}")
        print(f"Running {test_file}...")
        print('='*60)
        
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, timeout=30, 
                              encoding='utf-8', errors='replace')
        
        if result.returncode == 0:
            print(result.stdout)
            return True, None
        else:
            print(f"❌ {test_file} FAILED")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False, result.stderr
            
    except subprocess.TimeoutExpired:
        print(f"❌ {test_file} TIMED OUT")
        return False, "Test timed out"
    except Exception as e:
        print(f"❌ {test_file} ERROR: {e}")
        return False, str(e)


def main():
    """全てのテストを実行"""
    print("🚀 Running all Puyo Puyo game tests...")
    print(f"Python version: {sys.version}")
    
    # テストファイルのリスト（実行順序）
    test_files = [
        "test_puyo.py",                    # 基本クラスのテスト
        "test_fall_system.py",             # 落下システムのテスト
        "test_gravity_system.py",          # 重力システムのテスト
        "test_kick_system.py",             # キックシステムのテスト
        "test_connection_system.py",       # 連結判定システムのテスト
        "test_elimination_system.py",      # 消去システムのテスト
        "test_game_integration.py",        # 統合テスト
    ]
    
    results = []
    failed_tests = []
    
    # 各テストファイルを実行
    for test_file in test_files:
        success, error = run_test_file(test_file)
        results.append((test_file, success, error))
        
        if not success:
            failed_tests.append((test_file, error))
    
    # 結果のサマリーを表示
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    
    passed_count = sum(1 for _, success, _ in results if success)
    total_count = len(results)
    
    for test_file, success, error in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_file:<30} {status}")
    
    print(f"\nTotal: {total_count} tests")
    print(f"Passed: {passed_count}")
    print(f"Failed: {total_count - passed_count}")
    
    if failed_tests:
        print(f"\n{'='*60}")
        print("FAILED TESTS DETAILS")
        print('='*60)
        
        for test_file, error in failed_tests:
            print(f"\n❌ {test_file}:")
            print(f"   Error: {error}")
    
    # 全テスト成功の場合
    if passed_count == total_count:
        print(f"\n🎉 ALL TESTS PASSED! 🎉")
        print("The Puyo Puyo game is working correctly!")
        return 0
    else:
        print(f"\n💥 {total_count - passed_count} TEST(S) FAILED!")
        print("Please fix the failing tests before proceeding.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)