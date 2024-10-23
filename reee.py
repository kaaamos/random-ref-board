import os
import random
import shutil

def copy_random_images(folder_paths, num_images):
    images = find_images(folder_paths)

    # Check if there are enough images
    if len(images) < num_images:
        print(f"Error: Not enough images found. Found {len(images)} images.")
        raise ValueError

    # Select random images
    selected_images = random.sample(images, num_images)
    
    # Create a ref folder if it doesn't exist
    ref_folder = os.path.join(os.getcwd(), "ref")
    os.makedirs(ref_folder, exist_ok=True)

    # Create a new folder to store copied images
    target_folder, folder_number = create_incremental_folder()

    # Create a logs folder if it doesn't exist
    logs_folder = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_folder, exist_ok=True)

    # Create a log file for this folder
    log_file_path = os.path.join(logs_folder, f"{folder_number:02d}.txt")
    with open(log_file_path, 'w') as log_file:
        # Copy selected images to the new folder and log the paths
        for image in selected_images:
            shutil.copy(image, target_folder)
            log_entry = f"Copied: {image} to {target_folder}\n"
            log_file.write(log_entry)

def find_images(folder_paths):
    image_extensions = ('.jpg', '.jpeg', '.png')
    image_files = []
    for folder_path in folder_paths:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(image_extensions):
                    image_files.append(os.path.join(root, file))
    return image_files

def create_incremental_folder():
    current_dir = os.path.join(os.getcwd(), "ref")
    folder_number = 0
    while True:
        new_folder = os.path.join(current_dir, f"{folder_number:02d}")  # Format as two digits
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)
            return new_folder, folder_number
        folder_number += 1