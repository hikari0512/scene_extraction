from flask import Flask, render_template, request
import os, cv2, torch
from PIL import Image
from werkzeug.utils import secure_filename
import open_clip
from moviepy.editor import VideoFileClip

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
OUTPUT_FOLDER = os.path.join(app.root_path, 'static', 'output')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

model, _, preprocess = open_clip.create_model_and_transforms('RN50', pretrained='openai')
tokenizer = open_clip.get_tokenizer('RN50')
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = model.to(device)
model.load_state_dict(torch.load(
    r"C:\Users\KIT_Rental\Desktop\kono\project_001\Train_CLIP\finetuned_openclip.pth"))
model.eval()

class_texts = [
    "holding weapon not shooting at enemy",
    "preparing during buy phase",
    "using skill not in combat",
    "killed by enemy",
    "shooting at enemy",
    "killed an enemy"
]
target_class = 5

@app.route('/')
def index():
    return render_template("index.html")

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
    image_input = preprocess(image).unsqueeze(0).to(device)
    text_inputs = tokenizer(class_texts).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image_input)
        text_features = model.encode_text(text_inputs)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        logits = 100.0 * image_features @ text_features.T
        probs = logits.softmax(dim=-1).cpu().numpy().flatten()
    return probs.argmax(), probs[target_class]

def extract_combat_scenes(input_path, output_path, threshold):
    cap = cv2.VideoCapture(input_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    temp_output = output_path.replace('.mp4', '_temp.mp4')
    writer = cv2.VideoWriter(temp_output, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for _ in range(total):
        ret, frame = cap.read()
        if not ret:
            break
        pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        pred, conf = classify_frame(pil)
        if pred == target_class and conf > threshold:
            writer.write(frame)

    cap.release()
    writer.release()

    # 再エンコードで互換性確保
    clip = VideoFileClip(temp_output)
    clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
    clip.close()
    os.remove(temp_output)

if __name__ == '__main__':
    app.run(debug=True)
