from pathlib import Path
from PIL import Image

import torch
import open_clip

from .base import AIClassifier

PROMPT_TEMPLATES = [
    "a high quality wallpaper of {}",
    "a photo of {}",
    "an illustration of {}",
]

class ClipClassifier(AIClassifier):
    def __init__(self, categories: list[str]):
        if not categories:
            raise ValueError("ClipClassifier requer ao menos uma categoria")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32",
            pretrained="laion2b_s34b_b79k"
        )
        self.tokenizer = open_clip.get_tokenizer("ViT-B-32")

        self.model.to(self.device)
        self.model.eval()

        self.categories = categories
        self.prompt_to_category: list[str] = []
        prompts = []
        for c in categories:
            for tpl in PROMPT_TEMPLATES:
                prompts.append(tpl.format(c.lower()))
                self.prompt_to_category.append(c)

        self.text_tokens = self.tokenizer(prompts).to(self.device)

        with torch.no_grad():
            self.text_features = self.model.encode_text(self.text_tokens)
            self.text_features /= self.text_features.norm(dim=-1, keepdim=True)

    def classify(self, image_path: Path) -> tuple[str, float]:
        image = Image.open(image_path).convert("RGB")
        image_tensor = self.preprocess(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            image_features = self.model.encode_image(image_tensor)
            image_features /= image_features.norm(dim=-1, keepdim=True)

            similarity = (image_features @ self.text_features.T).softmax(dim=-1)

        confidence, idx = similarity[0].max(dim=0)
        idx = idx.item()

        return self.prompt_to_category[idx], float(confidence.item())
