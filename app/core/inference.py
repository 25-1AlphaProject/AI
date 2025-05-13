from runpy import run_path
import torch
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

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
        source='local'
    )
    #print("모델 로드 완료, 클래스 목록:", _MODEL.names)   # ← 여기에 추가

    _MODEL.conf = 0.1

def predict(image_bytes: bytes) -> list[str]:
    import io
    from PIL import Image

    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    results = _MODEL(img, size=416)   # detect.py와 동일하게 416 해상도

    return [ _MODEL.names[int(c)] for c in results.xyxyn[0][:, -1] ]
