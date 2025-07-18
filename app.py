from flask import Flask, render_template, request
import os, cv2, torch
from PIL import Image
from werkzeug.utils import secure_filename
import open_clip
from moviepy.editor import VideoFileClip

"""
Flaskアプリケーション：VALORANTのシーン自動検出・抽出
- 動画アップロードを受け取る
- ファインチューニングされたCLIPモデルでフレームごとに分類
- target_class（抽出対象のクラス）のみを抽出
- 抽出後の動画を出力・表示
"""

app = Flask(__name__)

# アップロードされた動画と抽出後の動画を保存するディレクトリの作成
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
OUTPUT_FOLDER = os.path.join(app.root_path, 'static', 'output')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# CLIPモデル（ResNet50）と前処理、トークナイザーの読み込み
model, _, preprocess = open_clip.create_model_and_transforms('RN50', pretrained='openai')
tokenizer = open_clip.get_tokenizer('RN50')
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = model.to(device)
model.load_state_dict(torch.load(r"finetuned_openclip.pth")) # ファインチューニングされたモデルを読み込み
model.eval()

# 使用するプロンプト
class_texts = [
    "holding weapon not shooting at enemy", # 武器を構えているが敵を撃っていない
    "preparing during buy phase", # ラウンド前の武器購入フェーズ中
    "using skill not in combat", # キャラクターのスキルを使用している
    "killed by enemy", # 敵に倒された
    "shooting at enemy", # 敵を撃っている
    "killed an enemy" # 敵を倒した
]

# 抽出対象のクラス
target_class = 5 # "killed an enemy"

# トップページ（動画アップロードフォーム）を表示
@app.route('/')
def index():
    return render_template("index.html")

# アップロードされた動画を保存し、シーン抽出処理後、結果ページを表示
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['video']
    threshold = float(request.form.get('threshold', 0.5))
    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    output_filename = "output_" + filename
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    extract_combat_scenes(input_path, output_path, threshold)

    return render_template(
        "result.html",
        input_video=f"uploads/{filename}",
        output_video=f"output/{output_filename}"
    )

def classify_frame(image):
    """
    1フレームの画像に対してCLIPモデルで分類
    クラス予測とクラスの信頼度を返す関数

    Args:
        image (PIL.Image): 分類対象の画像
        
    Returns:
        tuble:（予測クラスID, スコア）
    """
    image_input = preprocess(image).unsqueeze(0).to(device)
    text_inputs = tokenizer(class_texts).to(device)
    with torch.no_grad():
        # 画像とテキストをそれぞれエンコード
        image_features = model.encode_image(image_input)
        text_features = model.encode_text(text_inputs)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        logits = 100.0 * image_features @ text_features.T
        probs = logits.softmax(dim=-1).cpu().numpy().flatten()
    return probs.argmax(), probs[target_class]

def extract_combat_scenes(input_path, output_path, threshold):
    """
    入力動画から抽出対象のクラス（target_class）のフレーム画像を抽出し、新しい動画として保存する。

    Args: 
    input_path (str): 入力動画のパス
    output_path (str): 出力動画の保存先ファイルパス
    threshold (float): 信頼度の閾値（これを超えたシーンのみ抽出）
    """
    cap = cv2.VideoCapture(input_path) # 動画ファイルの読み込み
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    temp_output = output_path.replace('.mp4', '_temp.mp4')
    writer = cv2.VideoWriter(temp_output, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height)) # 一時ファイルの書き出し準備

    for _ in range(total):
        ret, frame = cap.read()
        if not ret:
            break
        pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        pred, conf = classify_frame(pil)

        # 画像を分類し、条件を満たすフレームのみ書き出す
        if pred == target_class and conf > threshold:
            writer.write(frame)

    cap.release()
    writer.release()

    # 再エンコードで互換性確保
    clip = VideoFileClip(temp_output)
    clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
    clip.close()
    os.remove(temp_output)

# Flaskアプリ起動
if __name__ == '__main__':
    app.run(debug=True)
