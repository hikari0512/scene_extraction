import torch
import open_clip
from PIL import Image
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from torchvision import transforms


# モデルとトークナイザ
model, _, preprocess = open_clip.create_model_and_transforms('RN50', pretrained='openai')
tokenizer = open_clip.get_tokenizer('RN50')
model = model.to('cuda')

# 自作Dataset
class ClipPairDataset(Dataset):
    def __init__(self, csv_path, transform):
        self.df = pd.read_csv(csv_path)
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        image = Image.open(self.df.iloc[idx]['image_path']).convert('RGB')
        text = self.df.iloc[idx]['text']
        return self.transform(image), tokenizer([text])[0]

# データセットとデータローダーの準備
dataset = ClipPairDataset(r"train_clip.csv", transform=preprocess)
loader = DataLoader(dataset, batch_size=5, shuffle=True)

# 学習ループ
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)

model.train()
best_acc = 0.0
best_model_path = r"train_openclip.pth"

for epoch in range(20):
    total_samples = 0
    correct_image = 0
    correct_text = 0

    for images, texts in loader:
        images = images.to('cuda')
        texts = texts.to('cuda')

        image_features = model.encode_image(images)
        text_features = model.encode_text(texts)

        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)

        logits_per_image = image_features @ text_features.T
        logits_per_text = text_features @ image_features.T

        labels = torch.arange(len(images)).to(images.device)
        loss = (torch.nn.functional.cross_entropy(logits_per_image, labels) +
                torch.nn.functional.cross_entropy(logits_per_text, labels)) / 2

        pred_image = logits_per_image.argmax(dim=1)
        pred_text = logits_per_text.argmax(dim=1)
        correct_image += (pred_image == labels).sum().item()
        correct_text += (pred_text == labels).sum().item()
        total_samples += len(images)

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

    acc_image = correct_image / total_samples
    acc_text = correct_text / total_samples
    avg_acc = (acc_image + acc_text) / 2  # 平均精度を基準とする

    print(f"Epoch {epoch}: Loss {loss.item():.4f}, Image Accuracy: {acc_image:.4f}, Text Accuracy: {acc_text:.4f}")
     
     # ★ 最大精度モデルの保存
    if avg_acc > best_acc:
        best_acc = avg_acc
        torch.save(model.state_dict(), best_model_path)
        print(f"✅ Best model saved at Epoch {epoch} with Avg Accuracy {best_acc:.4f}")
