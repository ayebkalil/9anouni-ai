import os
import shutil
import glob
from collections import defaultdict

def cleanup_processed_dirs():
    processed_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed"))
    
    # Get all prod-run folders
    folders = glob.glob(os.path.join(processed_dir, "prod-run-*"))
    
    # Group folders by the base law name
    # Example folder name: prod-run-finance_law_2020-671c4ff2
    # Base name: finance_law_2020
    grouped_folders = defaultdict(list)
    
    for folder in folders:
        basename = os.path.basename(folder)
        # Split by '-' and reconstruct the base law name
        parts = basename.split('-')
        # parts looks like: ['prod', 'run', 'finance_law_2020', '671c4ff2']
        if len(parts) >= 4:
            base_law_name = "-".join(parts[2:-1])
            grouped_folders[base_law_name].append(folder)
            
    deleted_count = 0
    kept_count = 0
    
    # For each law, sort by creation time, keep the newest, delete the rest
    for law, paths in grouped_folders.items():
        # Sort by creation time (or modification time) descending
        paths.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        # Keep the newest one
        newest = paths[0]
        kept_count += 1
        print(f"Keeping newest for {law}: {os.path.basename(newest)}")
        
        # Delete the older ones
        for old_path in paths[1:]:
            print(f"  -> Deleting older duplicate: {os.path.basename(old_path)}")
            shutil.rmtree(old_path)
            deleted_count += 1

    print(f"\nCleanup complete! Kept {kept_count} latest folders, deleted {deleted_count} old duplicate folders.")

if __name__ == "__main__":
    cleanup_processed_dirs()
