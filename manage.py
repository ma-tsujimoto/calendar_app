#!/usr/bin/env python
"""Djangoの管理コマンドを実行するためのエントリーポイントファイル。"""

import os
import sys

def main():
    """メイン関数：Django設定を読み込み、コマンドを実行する。"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calendar_app.settings')  # 設定ファイルの場所を指定
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Djangoがインストールされていないか、環境設定が正しくありません。"
        ) from exc
    execute_from_command_line(sys.argv)  # コマンドライン引数に応じて処理を実行

if __name__ == '__main__':
    main()
