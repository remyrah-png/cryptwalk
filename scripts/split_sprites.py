from PIL import Image
import os
print("Current dir:", os.getcwd())

# Config: Adjust based on your sprites (from Walk.png: 6 frames, ~128x96 each? Measure one frame width/height)
animations = {
    'Attack_1': {'file': '0_Forest_Ranger_Shooting_000.png', 'frame_count': 4, 'frame_width': 128, 'frame_height': 96},
    'Attack_2': {'file': '1_Forest_Ranger_Shooting_001.png', 'frame_count': 4, 'frame_width': 128, 'frame_height': 96},
    'Dead': {'file': 'Dead.png', 'frame_count': 5, 'frame_width': 128, 'frame_height': 96},
    'Hurt': {'file': 'Hurt.png', 'frame_count': 2, 'frame_width': 128, 'frame_height': 96},
    'Idle': {'file': 'Idle.png', 'frame_count': 4, 'frame_width': 128, 'frame_height': 96},
    'Jump': {'file': 'Jump.png', 'frame_count': 4, 'frame_width': 128, 'frame_height': 96},
    'Run': {'file': 'Run.png', 'frame_count': 6, 'frame_width': 128, 'frame_height': 96},
    'RunAttack': {'file': 'RunAttack.png', 'frame_count': 6, 'frame_width': 128, 'frame_height': 96},
    'Walk': {'file': 'Walk.png', 'frame_count': 6, 'frame_width': 128, 'frame_height': 96}
}

base_path = '/var/mnt/vms/cryptwalk_project/assets/ForestRanger/Forest_Ranger_1/PNG/PNG Sequences'

for anim, info in animations.items():
    anim_path = os.path.join(base_path, anim)
    os.makedirs(anim_path, exist_ok=True)  # Create subfolder if needed
    full_path = os.path.join(base_path, info['file'])
    print("Trying to open:", full_path)
    if not os.path.exists(full_path):
        print("File missing! Check path/case.")
    sheet = Image.open(os.path.join(base_path, info['file']))
    
    for i in range(info['frame_count']):
        frame = sheet.crop((i * info['frame_width'], 0, (i + 1) * info['frame_width'], info['frame_height']))
        frame.save(os.path.join(anim_path, f'{anim}_{i+1:03d}.png'))  # e.g., Walk_001.png

        

print("Splitting done!")