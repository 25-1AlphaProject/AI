import io, sys
import numpy as np
import torch
from pathlib import Path
from PIL import Image

_MODEL = None

def load_model():
    base_dir = Path(__file__).resolve().parents[2]
    repo_dir = base_dir / "yolov5"
    weights  = base_dir / "weights" / "best.pt"

    sys.path.insert(0, str(repo_dir))
    global _MODEL
    _MODEL = torch.hub.load(
        str(repo_dir),
        'custom',
        path=str(weights),
        source='local',
        force_reload=True
    )
    _MODEL.conf = 0.25
    #print("모델 로드 완료, 클래스 목록:", _MODEL.names)

def predict(image_bytes: bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_arr = np.array(img)

    results = _MODEL(img_arr, size=416)

    classes = results.xyxyn[0][:, -1].cpu().numpy().astype(int)
    return [ _MODEL.names[c] for c in classes ]
