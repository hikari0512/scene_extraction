# VALORANT シーン自動抽出アプリケーション

このアプリケーションは、VALORANTのプレイ動画から特定のシーンを自動抽出する機能を提供します。OpenCLIPモデルを活用し、さまざまなシーンへの柔軟な対応が可能です。

## 機能概要

### 主な機能
- 動画のアップロード
- シーンの自動抽出
- 抽出結果のプレビュー

### モデル学習に関する機能
- OpenCLIPモデルのファインチューニング
- カスタムデータセットを用いた学習プロセス
- 最適なモデルの保存と運用

## 使用技術

- **Python**: ロジック構築と機械学習モデルの操作
- **Flask**: Webフレームワーク
- **OpenCLIP**: CLIPモデルの利用と学習
- **Torch**: モデル学習と推論
- **MoviePy**: 動画編集ツール
- **Bootstrap**: フロントエンドデザインの構築

## セットアップ手順

### 必要な環境
- Python 3.8以上
- CUDA対応GPU（推奨）

### インストール方法
1. リポジトリをクローンします:
    ```
    git clone https://github.com/hikari0512/VALORANT_scene_extraction.git
    cd VALORANT_scene_extraction
    ```

2. 必要な依存関係をインストールします:
    ```
    pip install -r requirements.txt
    ```

3. モデルファイルを準備します:
    - `finetuned_openclip.pth`を`app.py`で指定されたパスに配置してください。

4. サーバーを起動します:
    ```
    python app.py
    ```

5. ブラウザで`http://127.0.0.1:5000/`にアクセスしてください。

### モデル学習を行う場合
1. トレーニング用のCSVファイルを準備します:
    - ファイルには画像パスとテキストラベルを含める必要があります。
    - 学習データの形式：
      ```
      image_path, text
      .data\0\train_000.png
      .data\0\train_001.png
      ```

2. 学習を開始します:
    ```
    python train_openCLIP.py
    ```

## システム画面

### 入力画面
[入力画面](images/start_screen.png)

### 抽出プロセス画面
[入力画面](images/extraction_screen.png)

### 抽出結果画面
[入力画面](images/result_screen.png)

## ファイル構成

```
│── images/           # システムの画面画像
    ├──
    ├── extraction_screen.png  # 抽出途中の画像
    ├── result_screen.png   # 抽出結果の画像
    ├── start_screen.png  # 入力画面の画像
├── templates/            # HTMLテンプレート
    ├── index.html        # 動画アップロード画面
    └── result.html       # 抽出結果画面
├── README.md             # プロジェクト概要
├── app.py                # 主なサーバースクリプト
├── requirements.txt      # 必要なPython依存関係
├── train_openCLIP.py     # モデル学習用スクリプト
```

### 今後の展望
1. ユーザがプロンプトを設定し、より多様なシーンに対応。
2. 学習データセットの拡充。
3. プロンプトの精度向上。
4. モデル選定の最適化。
