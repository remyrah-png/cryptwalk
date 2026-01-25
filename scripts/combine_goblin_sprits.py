import os
from PIL import Image

base_path = '/var/mnt/vms/cryptwalk_project/assets/Goblin/PNG/PNG Sequences/'  # From ls

# List available folders
print("Available folders in PNG Sequences:", [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))])

# All available folders (with file_prefix based on ls naming)
animations = {
    'Dying': {'file_prefix': '0_Goblin_Dying_'},
    'Falling Down': {'file_prefix': '0_Goblin_Falling Down_'},
    'Hurt': {'file_prefix': '0_Goblin_Hurt_'},
    'Idle': {'file_prefix': 'Idle_'},  # Updated for Idle naming
    'Idle Blinking': {'file_prefix': '0_Goblin_Idle Blinking_'},
    'Jump Loop': {'file_prefix': '0_Goblin_Jump Loop_'},
    'Jump Start': {'file_prefix': '0_Goblin_Jump Start_'},
    'Kicking': {'file_prefix': '0_Goblin_Kicking_'},
    'Running': {'file_prefix': '0_Goblin_Running_'},
    'Run Slashing': {'file_prefix': '0_Goblin_Run Slashing_'},
    'Run Throwing': {'file_prefix': '0_Goblin_Run Throwing_'},
    'Slashing': {'file_prefix': '0_Goblin_Slashing_'},
    'Slashing in The Air': {'file_prefix': '0_Goblin_Slashing in The Air_'},
    'Sliding': {'file_prefix': '0_Goblin_Sliding_'},
    'Throwing': {'file_prefix': '0_Goblin_Throwing_'},
    'Throwing in The Air': {'file_prefix': '0_Goblin_Throwing in The Air_'},
    'Walking': {'file_prefix': '0_Goblin_Walking_'},
}

for anim, info in animations.items():
    anim_path = os.path.join(base_path, anim)
    if not os.path.exists(anim_path):
        print(f"Missing folder: {anim_path}")
        continue
    
    file_prefix = info.get('file_prefix', '0_Goblin_')  # Default if not set
    prefix = anim.replace(' ', '_')  # For output file name
    
    # Get sorted frame files (exclude any existing combined PNG)
    frame_files = sorted([f for f in os.listdir(anim_path) if f.endswith('.png') and f.startswith(file_prefix) and f != f'{prefix}.png'])
    if not frame_files:
        print(f"No frames found in: {anim_path}")
        continue
    
    # Check if combined already exists
    output_file = os.path.join(anim_path, f'{prefix}.png')
    if os.path.exists(output_file):
        print(f"Already combined: {output_file}")
        continue
    
    # Auto-detect dimensions from first frame
    first_frame_path = os.path.join(anim_path, frame_files[0])
    with Image.open(first_frame_path) as first_frame:
        frame_width, frame_height = first_frame.size
    
    # Create new blank sheet
    sheet_width = frame_width * len(frame_files)
    sheet = Image.new('RGBA', (sheet_width, frame_height))
    
    for i, frame_file in enumerate(frame_files):
        frame_path = os.path.join(anim_path, frame_file)
        with Image.open(frame_path) as frame:
            sheet.paste(frame, (i * frame_width, 0))
    
    sheet.save(output_file)
    print(f"Combined {anim} into {output_file}")

print("Combining complete!")
print(f"Unknown item type: {item.type}")