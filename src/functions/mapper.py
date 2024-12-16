import os
import json

def find_files_recursively(directory, extensions):
    """
    Recursively find all files in the directory with specific extensions.

    Args:
        directory (str): The root directory to search.
        extensions (tuple): File extensions to look for.

    Returns:
        list: List of found file paths.
    """
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith(extensions):
                files.append(os.path.join(root, filename))
    return files

def generate_mapper_from_dataset_recursive(image_dir, audio_dir, output_file):
    # Find all images and audios recursively
    images = sorted(find_files_recursively(image_dir, ('.png', '.jpg', '.jpeg')))
    audios = sorted(find_files_recursively(audio_dir, ('.mid',)))

    # Normalize file paths to file names for mapper
    mapper = []
    for idx, audio_file in enumerate(audios):
        image_file = images[idx % len(images)]  # Repeat images if fewer than audios
        mapper.append({
            "image": os.path.relpath(image_file, start=image_dir),
            "audioSrc": os.path.relpath(audio_file, start=image_dir)
        })

    # Write the mapper to a JSON file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(mapper, f, indent=4)

    return mapper

# Example usage
# image_directory = './test/images'
# audio_directory = './test/audios'
# output_mapper_file = './test/mapper.json'

# mapper = generate_mapper_from_dataset_recursive(image_directory, audio_directory, output_mapper_file)
# print("Mapper generated:", mapper)
