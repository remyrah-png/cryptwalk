import os
from PIL import Image

print("Current dir:", os.getcwd())

base_path = '/var/mnt/vms/cryptwalk_project/assets/ForestRanger/Forest_Ranger_1/PNG/'

# List files in base_path to debug
print("Files in base_path:", os.listdir(base_path))
print("Files in PNG folder:", os.listdir(os.path.join(base_path)))

# Config: Update 'file' to your actual sprite sheet names (e.g., 'Shooting.png' if that's the file)
animations = {
    'Attack 1': {'file': 'Shooting.png', 'frame_count': 4, 'frame_width': 128, 'frame_height': 96},
    'Dead': {'file': 'Dead.png', 'frame_count': 5, 'frame_width': 128, 'frame_height': 96},
    'Hurt': {'file': 'Hurt.png', 'frame_count': 2, 'frame_width': 128, 'frame_height': 96},
    'Idle': {'file': 'Idle.png', 'frame_count': 4, 'frame_width': 128, 'frame_height': 96},
    'Jump': {'file': 'Jump.png', 'frame_count': 4, 'frame_width': 128, 'frame_height': 96},
    'Run': {'file': 'Run.png', 'frame_count': 6, 'frame_width': 128, 'frame_height': 96},
    'RunAttack': {'file': 'RunAttack.png', 'frame_count': 6, 'frame_width': 128, 'frame_height': 96},
    'Walk': {'file': 'Walk.png', 'frame_count': 6, 'frame_width': 128, 'frame_height': 96},
    'Throwing': {'file': 'Throwing.png', 'frame_count': 12, 'frame_width': 128, 'frame_height': 96},  # Based on your directory
}

for anim, info in animations.items():
    anim_path = os.path.join(base_path, 'PNG Sequence', anim)
    os.makedirs(anim_path, exist_ok=True)  # Create subfolder for output frames if needed
    
    full_path = os.path.join(base_path, info['file'])  # Load sheet from base_path (not anim_path)
    print("Trying to open:", full_path)
    
    if not os.path.exists(full_path):
        print("File missing! Check path/case or confirm sprite sheet exists.")
        continue
    
    sheet = Image.open(full_path)
    
    for i in range(info['frame_count']):
        frame = sheet.crop((i * info['frame_width'], 0, (i + 1) * info['frame_width'], info['frame_height']))
        frame.save(os.path.join(anim_path, f'0_Forest_Ranger_{anim}_{i:03d}.png'))  # Matches your naming convention

print("Splitting complete!")