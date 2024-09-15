import os
import shutil


def find_and_copy_images(log_file, source_directory, destination_directory):
    # Define paths for the image and materials directories
    image_directory = os.path.join(destination_directory, 'image')
    materials_directory = os.path.join(destination_directory, 'materials')

    # Create directories if they don't already exist
    create_directory(image_directory)  # Directory for images
    create_directory(materials_directory)  # Main directory for materials
    create_directory(os.path.join(materials_directory, 'm'))  # Subdirectory for "m" materials
    create_directory(os.path.join(materials_directory, 'mc'))  # Subdirectory for "mc" materials

    # Traverse through the source directory to look for files
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            file_path = os.path.join(root, file)

            # Open the file and read line by line
            with open(file_path, 'r') as file:
                lines = file.readlines()

                # Check each line for specific keywords ('Image', 'Missing material')
                for line in lines:
                    # If 'Image' is in the line, try to extract the image path and copy it
                    if 'Image' in line:
                        copy_image_from_line(line, source_directory, image_directory)

                    # If 'Missing material "$m' is found, copy the file to the 'm' materials folder
                    elif 'Missing material "$m' in line:
                        copy_to_materials(file_path, materials_directory, 'm')

                    # If 'Missing material "$mc' is found, copy the file to the 'mc' materials folder
                    elif 'Missing material "$mc' in line:
                        copy_to_materials(file_path, materials_directory, 'mc')


def create_directory(directory_path):
    """
    Creates a directory if it doesn't already exist.
    Args:
        directory_path (str): The path of the directory to be created.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)  # Creates the directory and any intermediate directories


def copy_image_from_line(line, source_directory, image_directory):
    """
    Extracts an image path from a line and copies the image to the target directory.
    Args:
        line (str): The line from which to extract the image path.
        source_directory (str): The directory where the source image is located.
        image_directory (str): The directory where the image should be copied.
    """
    split_line = line.split('"')  # Attempt to extract the image name by splitting the line
    if len(split_line) >= 2:
        image_name = split_line[1]
        image_path = os.path.join(source_directory, image_name)
        if os.path.exists(image_path):  # Only copy the image if it exists
            shutil.copy(image_path, image_directory)  # Copy the image to the target directory


def copy_to_materials(file_path, materials_directory, material_type):
    """
    Copies a file to the appropriate materials subdirectory ('m' or 'mc').
    Args:
        file_path (str): The path of the file to be copied.
        materials_directory (str): The root directory for materials.
        material_type (str): The subdirectory within 'materials' where the file should be copied ('m' or 'mc').
    """
    target_directory = os.path.join(materials_directory, material_type)
    shutil.copy(file_path, target_directory)  # Copy the file to the appropriate materials subdirectory


# Example usage
log_file = 'D:\\Projects\\Visual_Studio_code\\Python\\cod_CsvWriter\\Outcoming.txt'
source_directory = 'E:\\h1\\dump\\sp'
destination_directory = 'E:\\h1\\zonetool\\mwr_recon_force'

# Call the function to find and copy images/materials
find_and_copy_images(log_file, source_directory, destination_directory)