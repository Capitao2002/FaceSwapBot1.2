import imageio
import os
import torch
import yaml
import numpy as np
from skimage.transform import resize
from demo import load_checkpoints, make_animation
import logging

logger = logging.getLogger(__name__)

def process_deepfake(source_image_path, driving_video_path, output_path):
    logger.info("🔧 Carregando modelo FOMM")
    config_path = 'first-order-motion-model/config/vox-256.yaml'
    checkpoint_path = 'first-order-motion-model/checkpoints/vox-cpk.pth.tar'

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    generator, kp_detector = load_checkpoints(config_path, checkpoint_path, device=device)

    source_image = imageio.imread(source_image_path)
    reader = imageio.get_reader(driving_video_path)
    fps = reader.get_meta_data()['fps']
    driving_video = [resize(frame, (256, 256))[..., :3] for frame in reader]
    reader.close()

    source_image = resize(source_image, (256, 256))[..., :3]
    predictions = make_animation(source_image, driving_video, generator, kp_detector, device=device)
    imageio.mimsave(output_path, [np.uint8(frame * 255) for frame in predictions], fps=fps)
    logger.info(f"🎬 Deepfake salvo em {output_path}")