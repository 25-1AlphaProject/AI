# app/core/inference.py
import torch
import sys
from pathlib import Path

_MODEL = None

def load_model():
    # inference.py → app/core → app → AI
    base_dir = Path(__file__).resolve().parents[2]      # AI 폴더
    repo_dir = base_dir / "yolov5"                      # AI/yolov5
    weights  = base_dir / "weights" / "best.pt"         # AI/weights/best.pt

    sys.path.insert(0, str(repo_dir))

    global _MODEL
    _MODEL = torch.hub.load(
        str(repo_dir),   # 로컬 yolov5 디렉터리
        'custom',
        path=str(weights),
        source='local'
    )
    _MODEL.conf = 0.25

def predict(image_bytes: bytes):
    import io
    from PIL import Image

    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    results = _MODEL(img)
    # 클래스 인덱스 → 이름
    return [_MODEL.names[int(c)] for c in results.xyxyn[0][:, -1]]
