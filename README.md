# YOLO Image Labeler

## Description
YOLO Image Labeler is a Python-based tool designed for easy and efficient labeling of images for use in YOLO (You Only Look Once) machine learning models. This tool enables users to manually draw rectangles around objects in images and generates corresponding annotation files in YOLO format.

## Features
- Supports various image formats (PNG, JPG, JPEG, GIF, BMP, WEBP).
- Customizable image resizing.
- Adjustable rectangle colors for different object classes.
- Interactive and user-friendly GUI for image annotation.

## Installation
To set up YOLO Image Labeler, follow these steps:
## Installation

To set up YOLO Image Labeler, follow these steps:

1. **Download the Folder**: Clone or download the repository to your local machine.

2. **Give Executable Permission to `starter.sh`**:
   - **Mac**:
     ```bash
     chmod +x starter.sh
     ```
   - **Windows**: 
     Windows does not use `chmod`. Instead, ensure that the script has execute permissions through file properties or use a Bash emulation layer like Git Bash.
   - **Linux**:
     ```bash
     chmod +x starter.sh
     ```

3. **Start the Script in the Console**:
   - **Mac**:
     ```bash
     ./starter.sh
     ```
   - **Windows**:
     You can run the script using Git Bash, WSL, or a similar bash emulation tool:
     ```bash
     ./starter.sh
     ```
     If these tools are not available, you may need to convert the script to a batch file or use a different method to start the application.
   - **Linux**:
     ```bash
     ./starter.sh
     ```

Please ensure that you have the necessary dependencies installed on your system to run the script. If you encounter any issues during installation, refer to the 'Troubleshooting' section below or open an issue in the repository.


## Usage
Before running the script, ensure you have a configuration file (`config.ini`) set up with the following parameters:

- `source_folder`: Path to the source folder containing images.
- `destination_folder`: Path to the folder where resized images and annotations will be saved.
- `base_name`: Base name for output files.
- `width`: Width to resize images to.
- `height`: Height to resize images to.
- `objects_rect_colors`: This parameter specifies a list of colors to be used for the bounding rectangles of different objects. Each color in the list corresponds to a unique object type being labeled in the images. The number of colors provided should match or exceed the total number of distinct objects expected to be labeled. At least one color should be provided.

To start labeling, run the script:

## Controls
- **Left Mouse Click & Drag**: Draw a rectangle around an object.
- **Spacebar**: Change the current object class color.
- **Backspace**: Remove the last drawn rectangle.
- **Enter**: Save annotations and proceed to the next image.
- **Close Window**: Save annotations and proceed to the next image.

## Contributing
Contributions to YOLO Image Labeler are welcome.

### Terms of Use
- **Permission**: The code is provided for use as is, and can be modified, distributed, and used in personal and commercial projects.
- **No Warranty**: The code is provided "as is" without any warranties of any kind, express or implied. The author(s) are not responsible for any damage, data loss, or issues arising from the use of this code.
- **Contributions**: Any contributions made to this project will be subject to the same license terms.
- **Acknowledgement**: While not required, credit or acknowledgment is appreciated if the code is used in your projects.
