import os
from PIL import Image

print("Current dir:", os.getcwd())

# Config: Adjust based on your sprites
animations = {
    'Attack 1': {'file': '0 Forest Ranger Shooting 000.png', 'frame_count': 4, 'frame_width': 128, 'frame_height': 96},
    'Attack 2': {'file': '1 Forest Ranger Shooting 001.png', 'frame_count': 4, 'frame_width': 128, 'frame_height': 96},  # Assuming pattern; fix as needed
    'Dead': {'file': 'Dead.png', 'frame_count': 5, 'frame_width': 128, 'frame_height': 96},
    'Hurt': {'file': 'Hurt.png', 'frame_count': 2, 'frame_width': 128, 'frame_height': 96},
    'Idle': {'file': 'Idle.png', 'frame_count': 4, 'frame_width': 128, 'frame_height': 96},
    'Jump': {'file': 'Jump.png', 'frame_count': 4, 'frame_width': 128, 'frame_height': 96},
    'Run': {'file': 'Run.png', 'frame_count': 6, 'frame_width': 128, 'frame_height': 96},
    'RunAttack': {'file': 'RunAttack.png', 'frame_count': 6, 'frame_width': 128, 'frame_height': 96},
    'Walk': {'file': 'Walk.png', 'frame_count': 6, 'frame_width': 128, 'frame_height': 96},
    'Throwing': {'file': 'Throwing.png', 'frame_count': 12, 'frame_width': 128, 'frame_height': 96},  # Added
    # Add more as needed
}

base_path = '/var/mnt/vms/cryptwalk_project/assets/ForestRanger/Forest Ranger 1/PNG/PNG Sequences/'

for anim, info in animations.items():
    anim_path = os.path.join(base_path, anim)
    os.makedirs(anim_path, exist_ok=True)  # Create subfolder if needed
    
    full_path = os.path.join(anim_path, info['file'])  # Assumes sheet is in the subfolder
    print("Trying to open:", full_path)
    
    if not os.path.exists(full_path):
        print("File missing! Check path/case.")
        continue  # Skip if missing
    
    sheet = Image.open(full_path)
    
    for i in range(info['frame_count']):
        frame = sheet.crop((i * info['frame_width'], 0, (i + 1) * info['frame_width'], info['frame_height']))
        frame.save(os.path.join(anim_path, f'0_Forest_Ranger_{anim}_{i:03d}.png'))  # Matches your directory naming

print("Splitting complete!")