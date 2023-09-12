import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from tqdm.autonotebook import tqdm

plt.rcParams["pdf.fonttype"]=42

class ImageAnnotatorConfig:
    """Configuration class for image annotation."""

    def __init__(self, point_color='royalblue', text_color='royalblue', scalebar_color='k',
                 scalebar_text_color='k', point_size=5, text_offset_x=0, text_offset_y=-30,
                 font_size=7, font_thickness=2, scalebar_xy=(100, 900), scalebar_thickness=2, suffix="[-_.]",meta_extension=".txt",Sample_ID='SAMPLE',xposition='X_POS', yposition='Y_POS'):
        """
        Parameters:
            point_color (str or tuple): The color of annotation points (default: 'royalblue').
            text_color (str or tuple): The color of text annotations (default: 'royalblue').
            scalebar_color (str or tuple): The color of the scale bar (default: 'k' - black).
            scalebar_text_color (str or tuple): The color of the scale bar text (default: 'k' - black).
            point_size (int): The size of annotation points (default: 5).
            text_offset_x (int): The horizontal offset of text annotations (default: 0).
            text_offset_y (int): The vertical offset of text annotations (default: -30).
            font_size (int): The font size of text annotations (default: 7).
            font_thickness (int): The thickness of the font (default: 2).
            scalebar_xy (tuple): The coordinates (x, y) for the scale bar (default: (100, 900)).
            scalebar_thickness (int): The thickness of the scale bar (default: 2).
            suffix (str): The suffix used for matching sample IDs in data (default: "[-_.]").
            meta_extension (str): The file extension for image metadata files (default: ".txt").
            Sample_ID (str): The name of the column containing sample IDs (default: 'SAMPLE').
            xposition (str): The name of the column containing X positions (default: 'X_POS').
            yposition (str): The name of the column containing Y positions (default: 'Y_POS').
        """
        self.point_color = point_color
        self.text_color = text_color
        self.scalebar_color = scalebar_color
        self.scalebar_text_color = scalebar_text_color
        self.point_size = point_size
        self.text_offset_x = text_offset_x
        self.text_offset_y = text_offset_y
        self.font_size = font_size
        self.font_thickness = font_thickness
        self.scalebar_xy = scalebar_xy
        self.scalebar_thickness = scalebar_thickness
        self.suffix = suffix
        self.meta_extension=meta_extension
        self.Sample_ID=Sample_ID
        self.xposition=xposition
        self.yposition=yposition

def named_color_to_rgb(name):
    """
    Convert a named color to its RGB representation.

    Parameters:
        name (str): The name of the color to be converted.

    Returns:
        tuple: A tuple representing the RGB values of the color.
    """
    return mcolors.to_rgba(name)[:3]

def annotate_image(image_path, data_path, data_table_name, sheet_name, image_file_name, config=ImageAnnotatorConfig(), plot_result=True,save_fig='pdf',show_bbox=True):
    """
    Annotate an image from JEOL microprobe with data points and text annotations. The data should have a Sample column, X and Y positions.

    Parameters:
        image_path (str): The path to the folder containing the image.
        data_path (str): The path to the folder containing the data table.
        data_table_name (str): The name of the data table file.
        sheet_name (str): The name of the sheet in the data table.
        image_file_name (str): The name of the image file to annotate.
        config (ImageAnnotatorConfig): An instance of the ImageAnnotatorConfig class for configuring annotation parameters (default: ImageAnnotatorConfig()).
        plot_result (bool): Whether to display the annotated image (default: True).
        save_fig (str): The format in which to save the annotated image ('png', 'tif', 'pdf', or 'pdf&tif') (default: 'png').
        show_bbox (bool): Whether to display a bounding box around text annotations (default: True).
    """
    image = plt.imread(os.path.join(image_path, image_file_name))
    df = pd.read_excel(os.path.join(data_path, data_table_name), sheet_name=sheet_name)

    imagefilename = image_file_name
    try:
        with open(os.path.join(image_path, imagefilename.split('.')[0] + config.meta_extension)) as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("$CM_FULL_SIZE"):
                    parts = line.split()
                    new_width = int(parts[1])
                    new_height = int(parts[2])
                if line.startswith("$CM_STAGE_POS"):
                    parts = line.split()
                    stage_x = float(parts[1])
                    stage_y = float(parts[2])
                if line.startswith("$$SM_MICRON_BAR"):
                    parts = line.split()
                    pixels = float(parts[1])
                if line.startswith("$$SM_MICRON_MARKER"):
                    parts = line.split()
                    microns4pixels = float(parts[1].split("u")[0])

        scale_px_per_micron = pixels / microns4pixels
        Sample_ID=config.Sample_ID
        xpos=config.xposition
        ypos=config.yposition
        subset_df = df[[Sample_ID, xpos, ypos]].copy()
        subset_df['stage_x'] = stage_x
        subset_df['stage_y'] = stage_y
        subset_df['dx (\u03BCm)'] = 1000 * (stage_x - subset_df[xpos])
        subset_df['dy (\u03BCm)'] = 1000 * (stage_y - subset_df[ypos])
        suffix = config.suffix
        data2plot = subset_df[subset_df[Sample_ID].str.contains(imagefilename.split('.')[0] + suffix)].reset_index()

        height, width, _ = image.shape

        if height != new_height:
            left = 0
            top = 0
            right = new_width
            bottom = new_height
            cropped_image = image[top:bottom, left:right]
        else:
            cropped_image = image.copy()

        height, width, _ = cropped_image.shape

        center_x = width // 2
        center_y = height // 2

        dx = data2plot['dx (\u03BCm)'] * scale_px_per_micron
        dy = data2plot['dy (\u03BCm)'] * scale_px_per_micron

        x = center_x + dx
        y = center_y - dy

        text_col = data2plot[Sample_ID]

        point_color = config.point_color
        text_color = config.text_color
        scalebar_color = config.scalebar_color
        scalebar_text_color = config.scalebar_text_color
        point_size = config.point_size
        text_offset_x = config.text_offset_x
        text_offset_y = config.text_offset_y
        font_size = config.font_size
        font_thickness = config.font_thickness
        scalebar_xy = config.scalebar_xy
        scalebar_thickness = config.scalebar_thickness

        if isinstance(point_color, str):
            point_color = named_color_to_rgb(point_color)
        if isinstance(text_color, str):
            text_color = named_color_to_rgb(text_color)
        if isinstance(scalebar_color, str):
            scalebar_color = named_color_to_rgb(scalebar_color)
        if isinstance(scalebar_text_color, str):
            scalebar_text_color = named_color_to_rgb(scalebar_text_color)

        fig, ax = plt.subplots()
        ax.imshow(cropped_image)

        for i in range(len(x)):
            ax.scatter(x[i], y[i], s=point_size, color=point_color)

            text = ax.text(
                x[i] + text_offset_x,
                y[i] + text_offset_y,
                text_col[i],
                fontsize=font_size,
                color=text_color,
                fontweight='bold',
                horizontalalignment='center'
            )
            if show_bbox==True:
                text.set_bbox(dict(facecolor='white', alpha=0.7, edgecolor='none'))

        ax.plot(
            [scalebar_xy[0], scalebar_xy[0] + int(pixels * scale_px_per_micron)],
            [scalebar_xy[1], scalebar_xy[1]],
            color=scalebar_color,
            linewidth=scalebar_thickness
        )

        scalebar_text = str(int(microns4pixels)) + " \u00B5m"
        sctext=ax.text(
            scalebar_xy[0] + (int(pixels * scale_px_per_micron) / 2),
            scalebar_xy[1] - 20,
            scalebar_text,
            fontsize=font_size,
            color=scalebar_text_color,
            fontweight='bold',
            horizontalalignment='center'
        )
        if show_bbox==True:
            sctext.set_bbox(dict(facecolor='white', alpha=0.7, edgecolor='none'))


        labeled_image_folder = os.path.join(image_path, 'labeled_images')

        if not os.path.exists(labeled_image_folder):
            os.mkdir(labeled_image_folder)

        plt.axis('off')

        if save_fig=='pdf&tif':
            plt.savefig(os.path.join(labeled_image_folder, image_file_name.split('.')[0] + "_labeled.tif"), dpi=300,bbox_inches='tight', pad_inches=0)       
            plt.savefig(os.path.join(labeled_image_folder, image_file_name.split('.')[0] + "_labeled.pdf"), dpi=300,bbox_inches='tight', pad_inches=0)
            
        elif save_fig=='png':
            plt.savefig(os.path.join(labeled_image_folder, image_file_name.split('.')[0] + "_labeled.png"), dpi=300,bbox_inches='tight', pad_inches=0)       
            
        elif save_fig=='tif':
            plt.savefig(os.path.join(labeled_image_folder, image_file_name.split('.')[0] + "_labeled.tif"), dpi=300,bbox_inches='tight', pad_inches=0)       
            
        if save_fig=='pdf':   
            plt.savefig(os.path.join(labeled_image_folder, image_file_name.split('.')[0] + "_labeled.pdf"), dpi=300,bbox_inches='tight', pad_inches=0)
            
        if plot_result!=False:
            plt.show()
        plt.close()
    except FileNotFoundError as e:
        print(e)

def process_images(image_path, data_path, data_table, sheet_name, config=ImageAnnotatorConfig(), image_extension='.tif',plot_result=False, save_fig='pdf', show_bbox=True):
    """
    Process a batch of images with the same configuration.

    Parameters:
        image_path (str): The path to the folder containing the images.
        data_path (str): The path to the folder containing the data table.
        data_table (str): The name of the data table file.
        sheet_name (str): The name of the sheet in the data table.
        image_extension (str): The file extension of the images to process (default: '.tif').
        plot_result (bool): Whether to display annotated images (default: False).
        save_fig (str): The format in which to save the annotated images ('png', 'tif', 'pdf', or 'pdf&tif') (default: 'pdf').
        show_bbox (bool): Whether to display bounding boxes around text annotations (default: False).
    """
    image_list = [file for file in os.listdir(image_path) if file.endswith(image_extension)]
    print(image_list)

    for file in tqdm(image_list, desc="Processing"):
        annotated_image = annotate_image(image_path, data_path, data_table, sheet_name, file, config, plot_result, save_fig, show_bbox)
