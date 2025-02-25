# import os
# os.environ["TOKENIZERS_PARALLELISM"] = "false"

import jax
import jax.numpy as jnp
from einops import rearrange
from transformers import AutoProcessor, FlaxCLIPModel

class CLIP():
    def __init__(self, clip_model="clip-vit-base-patch32"):
        self.processor = AutoProcessor.from_pretrained(f"openai/{clip_model}")
        self.clip_model = FlaxCLIPModel.from_pretrained(f"openai/{clip_model}")

        self.img_mean = jnp.array(self.processor.image_processor.image_mean)
        self.img_std = jnp.array(self.processor.image_processor.image_std)

    def embed_img(self, img):
        """
        img shape (H W C) and values in [0, 1].
        returns shape (D)
        """
        H, W, C = img.shape
        if H!=224 or W!=224:
            img = jax.image.resize(img, (224, 224, C), method='bilinear')
        img = rearrange((img-self.img_mean)/self.img_std, "H W C -> 1 C H W")
        z_img = self.clip_model.get_image_features(img)[0]
        return z_img / jnp.linalg.norm(z_img, axis=-1, keepdims=True)

    def embed_txt(self, prompts):
        """
        prompts is list of strings
        returns shape (B D)
        """
        inputs = self.processor(text=prompts, return_tensors="jax", padding=True)
        z_text = self.clip_model.get_text_features(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'])
        return z_text / jnp.linalg.norm(z_text, axis=-1, keepdims=True)