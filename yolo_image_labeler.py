import os
import configparser
import tkinter as tk
from PIL import Image, ImageTk
from dataclasses import dataclass, field

@dataclass
class _Configs:
    source_folder: str = ''
    destination_folder: str = '../annotated_images'
    base_name: str = 'item-'
    width: int = 512
    height: int = 512
    objects_rect_colors: list = field(default_factory=list)
    
@dataclass
class _CanvasRect:
    rect_id: int = None
    current_object_index: int = 0
    start_x: int = 0
    start_y: int = 0
    end_x: int = 0
    end_y: int = 0

# Global variable to prevent garbage collection of the image
tk_img = None

def _normalize_coordinate(coordinate, max_value):
    if coordinate < 0:
        return 0
    elif coordinate > max_value:
        return max_value
    return coordinate    

def _calculate_relative_properties(canvasRect, img_width, img_height):
    top_left = (_normalize_coordinate(canvasRect.start_x, img_height), _normalize_coordinate(canvasRect.start_y, img_width))
    bottom_right = (_normalize_coordinate(canvasRect.end_x, img_height), _normalize_coordinate(canvasRect.end_y, img_width))
    
    x_center_abs = (top_left[0] + bottom_right[0]) / 2
    y_center_abs = (top_left[1] + bottom_right[1]) / 2
    
    rect_width_abs = abs(bottom_right[0] - top_left[0])
    rect_height_abs = abs(bottom_right[1] - top_left[1])

    x_center_rel = x_center_abs / img_width
    y_center_rel = y_center_abs / img_height
    rect_width_rel = rect_width_abs / img_width
    rect_height_rel = rect_height_abs / img_height

    return f"{canvasRect.current_object_index} {x_center_rel} {y_center_rel} {rect_width_rel} {rect_height_rel}"
    
def _display_image_for_interavtion(img, colors):
    drawn_rectangles = []
    current_object_index = 0
            
    # Setup the Tkinter window and canvas
    root = tk.Tk()
    tk_img = ImageTk.PhotoImage(img)  # Create the PhotoImage object
    canvas = tk.Canvas(root, width=tk_img.width(), height=tk_img.height())
    canvas.create_image(0, 0, anchor="nw", image=tk_img)
    canvas.pack()
    
    # Variables to store the starting and ending points of the rectangle
    start_x, start_y, end_x, end_y, rect = None, None, None, None, None
    
    def on_click(event):
        nonlocal start_x, start_y, rect
        start_x, start_y = event.x, event.y
        if rect is not None:
            canvas.delete(rect)
        rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline=colors[current_object_index])

    def on_drag(event):
        nonlocal rect
        end_x, end_y = event.x, event.y
        canvas.coords(rect, start_x, start_y, end_x, end_y)

    def on_release(event):
        nonlocal end_x, end_y, drawn_rectangles
        end_x, end_y = event.x, event.y
        canvas_rect = draw_rectangle(canvas, img, start_x, start_y, end_x, end_y, colors[current_object_index])
        drawn_rectangles.append(canvas_rect)
        
    def draw_rectangle(canvas, img, start_x, start_y, end_x, end_y, color):
        # Ensure coordinates are integers and within image bounds
        start_x = max(0, int(start_x))
        start_y = max(0, int(start_y))
        end_x = min(img.width, int(end_x))
        end_y = min(img.height, int(end_y))
        rect_id = canvas.create_rectangle(start_x, start_y, end_x, end_y, outline=color)
        # Create a rectangle on the canvas and return its ID
        return _CanvasRect(rect_id, current_object_index, start_x, start_y, end_x, end_y)
        
    def on_window_close(_):
       root.destroy()
        
    def on_enter_pressed(_):
       root.destroy()
        
    def on_backspace_pressed(_):
        nonlocal canvas, drawn_rectangles, rect
        
        # Remove the last rectangle
        if rect is not None:
            canvas.delete(rect)
        
        if drawn_rectangles:
            canvasRect = drawn_rectangles.pop()
            canvas.delete(canvasRect.rect_id)
            canvas.update_idletasks()
      
    def on_space_pressed(_):
        nonlocal current_object_index 
        current_object_index += 1
        if current_object_index >= len(colors):
            current_object_index = 0

    # Bind mouse events to the canvas
    canvas.bind("<ButtonPress-1>", on_click)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)
    
    # Bind key events to the canvas
    canvas.bind("<Return>", on_enter_pressed)
    canvas.bind("<BackSpace>", on_backspace_pressed)
    canvas.bind("<space>", on_space_pressed)
    
    root.protocol("WM_DELETE_WINDOW", on_window_close)
    
    canvas.focus_set()
     
    # Display the image and wait
    root.mainloop() 
    
    return drawn_rectangles


def _resize_images(configs):
    
    source_folder = configs.source_folder
    destination_folder = configs.destination_folder
    img_width = configs.width
    img_height = configs.height
    files_base_name = configs.base_name
    object_colors = configs.objects_rect_colors

    print(f"Source Folder:        '{source_folder}'")
    print(f"Destination Folder:   '{destination_folder}'")
    print(f"Base Image Name:      '{files_base_name}'")
    print(f"Image size:           '{img_width}x{img_height}'")
    print(f"Objects rect colors:  '{object_colors}'")
    
    global tk_img  # Use the global variable

    file_num = 1 
    
    for file_name in os.listdir(source_folder):
        if file_name.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
            
            # Load the image and resize it
            img = Image.open(os.path.join(source_folder, file_name))
            img = img.resize((configs.width, configs.height), Image.Resampling.LANCZOS)
 
            rects = _display_image_for_interavtion(img, object_colors)

            # Save the resized image
            output_image_file_name = f"{configs.base_name}{file_num}.png"
            output_image_path = os.path.join(destination_folder, output_image_file_name)
            img.save(output_image_path)
            
            # Save the text file with rects data
            if rects is not None:
                output_text_file_name = f"{configs.base_name}{file_num}.txt"
                output_txt_path = os.path.join(destination_folder, output_text_file_name)
                with open(output_txt_path, 'w') as txt_file:
                    for rect in rects:
                        txt_file.write(f"{_calculate_relative_properties(rect, img_width, img_height)}\n")
               
                print(f"Saved resized image and text instructions for {file_name}: {output_image_file_name}, {output_text_file_name}")
            
            file_num += 1 

def _load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config['DEFAULT']

def _prompt_for_missing_config(config):
    configs = _Configs()

    configs.source_folder = config.get('source_folder') or input(f"Enter source folder path [{configs.source_folder}]: ") or configs.source_folder
    configs.destination_folder = config.get('destination_folder') or configs.destination_folder
    configs.base_name = config.get('base_name') or input(f"Enter base name for output files [{configs.base_name}]: ") or configs.base_name

    width = config.get('width')
    configs.width = int(width) if width and width.isdigit() else configs.width

    height = config.get('height')
    configs.height = int(height) if height and height.isdigit() else configs.height
    
    objects_rect_colors = config.get('objects_rect_colors')
    if objects_rect_colors:
        configs.objects_rect_colors = [color.strip() for color in objects_rect_colors.split(',')]
    else:
        configs.objects_rect_colors = configs.objects_rect_colors

    return configs
def main():
    config_path = 'config.ini'
    config = _load_config(config_path)
    config = _prompt_for_missing_config(config)

    _resize_images(config)

if __name__ == "__main__":
    main()


       