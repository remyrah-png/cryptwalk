import os
import pygame

ASSETS_BASE = '/var/mnt/vms/cryptwalk_project/assets/'

# Default dimensions per entity (from your ls/screenshots; add more as needed)
DEFAULT_DIMS = {
    'goblin': {'width': 96, 'height': 96},
    'forest_ranger': {'width': 128, 'height': 96},
    # Add 'orc': {'width': 128, 'height': 96}, etc.
}

def get_sprite_sheet(entity_type, animation='Idle', subfolder=''):
    """
    Load a sprite sheet for an entity and animation.
    - entity_type: 'goblin', 'forest_ranger', etc. (case-insensitive)
    - animation: 'Idle', 'Running', etc.
    - subfolder: For ForestRanger, use 'Forest_Ranger_1'; empty for Goblin
    """
    entity_type = entity_type.lower()
    if entity_type == 'forest_ranger':
        entity_folder = 'ForestRanger'
    else:
        entity_folder = entity_type.capitalize()  # e.g., 'Goblin'
    
    path = os.path.join(ASSETS_BASE, entity_folder, subfolder, 'PNG', 'PNG Sequences', animation, f"{animation.replace(' ', '_')}.png")
    if not os.path.exists(path):
        print(f"Sheet path missing: {path}")
        return None
    
    try:
        sheet = pygame.image.load(path)
        print(f"Loaded sheet for {entity_type}/{animation}: {sheet.get_size()}")
        return sheet
    except Exception as e:
        print(f"Load error for {entity_type}/{animation}: {e}")
        return None

def get_frames(sheet, entity_type, scale=(250, 250)):
    if not sheet:
        placeholder = pygame.Surface(scale).convert()
        placeholder.fill((0, 255, 0) if entity_type == 'goblin' else (0, 128, 255))
        return [placeholder] * 4
    
    dims = DEFAULT_DIMS.get(entity_type.lower(), {'width': 128, 'height': 96})
    frame_count = sheet.get_width() // dims['width']
    if frame_count == 0:
        print(f"No frames for {entity_type}")
        return [pygame.Surface(scale).convert()]
    
    frames = [sheet.subsurface((i * dims['width'], 0, dims['width'], dims['height'])) for i in range(frame_count)]
    frames = [pygame.transform.scale(frame, scale) for frame in frames]
    return frames