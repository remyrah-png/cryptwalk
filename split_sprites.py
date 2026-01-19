from PIL import Image
import os

# Config: Adjust based on your sprites (from Walk.png: 6 frames, ~128x96 each? Measure one frame width/height)
animations = {
    'Attack_1': {'file': 'Attack_1.png', 'frame_count': 4, 'frame_width': 96, 'frame_height': 96},  # Example; adjust counts/sizes
    'Attack_2': {'file': 'Attack_2.png', 'frame_count': 4, 'frame_width': 96, 'frame_height': 96},
    'Attack_3': {'file': 'Attack_3.png', 'frame_count': 4, 'frame_width': 96, 'frame_height': 96},
    'Dead': {'file': 'Dead.png', 'frame_count': 5, 'frame_width': 96, 'frame_height': 96},
    'Hurt': {'file': 'Hurt.png', 'frame_count': 2, 'frame_width': 96, 'frame_height': 96},
    'Idle': {'file': 'Idle.png', 'frame_count': 4, 'frame_width': 96, 'frame_height': 96},
    'Jump': {'file': 'Jump.png', 'frame_count': 4, 'frame_width': 96, 'frame_height': 96},
    'Run': {'file': 'Run.png', 'frame_count': 6, 'frame_width': 96, 'frame_height': 96},
    'Run+Attack': {'file': 'Run+Attack.png', 'frame_count': 6, 'frame_width': 96, 'frame_height': 96},
    'Walk': {'file': 'Walk.png', 'frame_count': 6, 'frame_width': 128, 'frame_height': 96}  # From your preview
}

base_path = 'assets/Hero/PNG/PNG Sequences/'

for anim, info in animations.items():
    anim_path = os.path.join(base_path, anim)
    os.makedirs(anim_path, exist_ok=True)  # Create subfolder if needed
    sheet = Image.open(os.path.join(base_path, info['file']))
    
    for i in range(info['frame_count']):
        frame = sheet.crop((i * info['frame_width'], 0, (i + 1) * info['frame_width'], info['frame_height']))
        frame.save(os.path.join(anim_path, f'{anim}_{i+1:03d}.png'))  # e.g., Walk_001.png

    # Optional: Delete original sheet after split
    # os.remove(os.path.join(base_path, info['file']))

print("Splitting done!")