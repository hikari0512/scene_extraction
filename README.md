# VALORANT シーン自動抽出アプリケーション

このアプリケーションは、VALORANTのプレイ動画から特定のシーンを自動抽出するアプリケーションです。アプリケーションでは、OpenCLIPモデルを使用してシーンを分類し、特定のシーンを自動抽出します。

## 機能概要

### アプリケーション機能
- 動画アップロード機能
- シーン抽出機能
- 抽出結果のプレビュー機能

### モデル学習機能
- OpenCLIPモデルのファインチューニング
- カスタムデータセットを用いた学習
- 最適なモデルの保存

## 使用技術

- **Python**: アプリケーションロジックとモデル学習
- **Flask**: Webアプリケーションフレームワーク
- **OpenCLIP**: CLIPモデルの利用と学習
- **Torch**: モデル学習と推論
- **MoviePy**: 動画編集
- **Bootstrap**: フロントエンドデザイン

## セットアップ方法

### 必要な環境
- Python 3.8以上
- CUDA対応GPU（推奨）

### インストール手順
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

4. アプリケーションを起動します:
    ```
    python app.py
    ```

5. ブラウザで`http://127.0.0.1:5000/`にアクセスしてください。

### モデル学習を実行する場合
1. トレーニング用のCSVファイルを準備します:
    - ファイルには画像パスとテキストラベルを含める必要があります。
    - 学習データの形式：
   image_path, text
   .data\0\train_000.png
   .data\0\train_001.png

2. トレーニングを実行します:
    ```
    python train_openCLIP.py
    ```

## システム画面

### 抽出入力画面
start_screen.png

### 抽出画面
extraction_screen.png

### 抽出結果画面
result_screen.png

## ファイル構成

```
├── app.py                # Flaskアプリケーションのメインスクリプト
├── train_openCLIP.py     # OpenCLIPモデルのトレーニングスクリプト
├── requirements.txt      # 必要なPython依存関係
├── templates/            # HTMLテンプレート
│   ├── index.html        # 動画アップロード画面
│   └── result.html       # 抽出結果画面
├── static/               # 静的ファイル
│   ├── uploads/          # アップロードされた動画
│   ├── output/           # シーン抽出後の動画
│   ├── images/           # システムの画面画像
│   │   ├── extraction_result.png  # 抽出結果画面画像
│   │   ├── extraction_input.png   # 抽出入力画面画像
└── README.md             # プロジェクト概要
```

### 今後の展望
1. ユーザ側からプロンプトを設定し、多様なシーンに対応する。
2. 学習データの拡張。
3. プロンプトの改善。
4. モデルの選定。
