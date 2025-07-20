#!/usr/bin/env python3
"""
Kiro Kiro Puzzle Game パッケージ化スクリプト
オリジナルのソースファイルを完全にコピーしてからPyxelアプリケーションパッケージを作成
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def clean_directory(directory):
    """ディレクトリを削除して再作成"""
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


def copy_source_files(src_dir, dest_dir):
    """ソースファイルを完全にコピー"""
    print(f"Copying source files from {src_dir} to {dest_dir}")
    
    # srcディレクトリ全体をコピー
    if os.path.exists(src_dir):
        shutil.copytree(src_dir, os.path.join(dest_dir, "src"))
        print(f"✓ Copied {src_dir} directory")
    else:
        print(f"✗ Source directory {src_dir} not found")
        return False
    
    return True


def create_package_main():
    """パッケージ用のmain.pyを作成"""
    main_content = '''"""
Kiro Kiro Puzzle Game - Pyxel Application Package Entry Point
"""

from src.game import KiroKiroGame


def main():
    """
    ゲームのエントリーポイント
    """
    KiroKiroGame()


if __name__ == "__main__":
    main()
'''
    return main_content


def create_package_readme():
    """パッケージ用のREADME.mdを作成"""
    readme_content = '''# Kiro Kiro Puzzle Game

Pyxelで作成されたPuyo Puyoスタイルのパズルゲームです。

## 実行方法

### パッケージ化されたアプリケーションの実行
```bash
python -m pyxel play kirokiro.pyxapp
```

### 開発環境での実行
```bash
python main.py
```

## 操作方法

- **左右矢印キー**: ぷよペアの左右移動
- **上矢印キー / Xキー**: 時計回り回転
- **Zキー**: 反時計回り回転
- **下矢印キー**: 高速落下
- **Rキー**: ゲーム再開始

## ゲームルール

1. 上から落ちてくる2つのぷよを操作して配置します
2. 同じ色のぷよが4つ以上つながると消去されます
3. ぷよが消去されると連鎖が発生し、高得点を狙えます
4. プレイフィールドの上部までぷよが積み上がるとゲームオーバーです

## 必要な環境

- Python 3.7以上
- Pyxel 1.4.0以上

## インストール

```bash
pip install pyxel
```

## パッケージ情報

このファイルはPyxelアプリケーションパッケージ（.pyxapp）として配布されています。
'''
    return readme_content


def run_pyxel_package(package_dir):
    """Pyxelパッケージ化コマンドを実行"""
    print(f"Running pyxel package command in {package_dir}")
    
    try:
        # パッケージディレクトリに移動してpyxel packageを実行
        result = subprocess.run(
            [sys.executable, "-m", "pyxel", "package", ".", "main.py"],
            cwd=package_dir,
            capture_output=True,
            text=True,
            check=True
        )
        
        print("✓ Pyxel package command completed successfully")
        print("Output:", result.stdout)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Pyxel package command failed: {e}")
        print("Error output:", e.stderr)
        return False
    except FileNotFoundError:
        print("✗ Python or pyxel not found. Make sure pyxel is installed.")
        return False


def rename_package_file(package_dir, old_name="package_build.pyxapp", new_name="kirokiro.pyxapp"):
    """パッケージファイルの名前を変更"""
    old_path = os.path.join(package_dir, old_name)
    new_path = os.path.join(package_dir, new_name)
    
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"✓ Renamed {old_name} to {new_name}")
        return True
    else:
        print(f"✗ Package file {old_name} not found")
        return False


def verify_package(package_dir, package_name="kirokiro.pyxapp"):
    """パッケージファイルの存在を確認"""
    package_path = os.path.join(package_dir, package_name)
    
    if os.path.exists(package_path):
        file_size = os.path.getsize(package_path)
        print(f"✓ Package file created: {package_name} ({file_size} bytes)")
        return True
    else:
        print(f"✗ Package file {package_name} not found")
        return False


def main():
    """メイン処理"""
    print("=" * 60)
    print("Kiro Kiro Puzzle Game パッケージ化スクリプト")
    print("=" * 60)
    
    # 現在のディレクトリを取得
    current_dir = os.getcwd()
    src_dir = os.path.join(current_dir, "src")
    package_build_dir = os.path.join(current_dir, "package_build")
    
    print(f"Current directory: {current_dir}")
    print(f"Source directory: {src_dir}")
    print(f"Package build directory: {package_build_dir}")
    
    # Step 1: パッケージビルドディレクトリをクリーン
    print("\n[Step 1] Cleaning package build directory...")
    clean_directory(package_build_dir)
    
    # Step 2: ソースファイルをコピー
    print("\n[Step 2] Copying source files...")
    if not copy_source_files(src_dir, package_build_dir):
        print("✗ Failed to copy source files")
        return False
    
    # Step 3: パッケージ用のmain.pyを作成
    print("\n[Step 3] Creating package main.py...")
    main_py_path = os.path.join(package_build_dir, "main.py")
    with open(main_py_path, "w", encoding="utf-8") as f:
        f.write(create_package_main())
    print("✓ Created main.py")
    
    # Step 4: パッケージ用のREADME.mdを作成
    print("\n[Step 4] Creating package README.md...")
    readme_path = os.path.join(package_build_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(create_package_readme())
    print("✓ Created README.md")
    
    # Step 5: Pyxelパッケージ化を実行
    print("\n[Step 5] Running pyxel package command...")
    if not run_pyxel_package(package_build_dir):
        print("✗ Failed to create pyxel package")
        return False
    
    # Step 6: パッケージファイルの名前を変更
    print("\n[Step 6] Renaming package file...")
    if not rename_package_file(package_build_dir):
        print("✗ Failed to rename package file")
        return False
    
    # Step 7: パッケージファイルの確認
    print("\n[Step 7] Verifying package file...")
    if not verify_package(package_build_dir):
        print("✗ Package verification failed")
        return False
    
    # 完了メッセージ
    print("\n" + "=" * 60)
    print("✓ パッケージ化が完了しました！")
    print("=" * 60)
    print(f"パッケージファイル: {os.path.join(package_build_dir, 'kirokiro.pyxapp')}")
    print("\n実行方法:")
    print(f"  cd {package_build_dir}")
    print("  python -m pyxel play kirokiro.pyxapp")
    print("\nまたは:")
    print("  python -m pyxel play package_build/kirokiro.pyxapp")
    
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        print("\n✗ パッケージ化に失敗しました")
        sys.exit(1)
    else:
        print("\n✓ パッケージ化に成功しました")
        sys.exit(0)