import ProbeLabeler as pl 
import os

# Set these to appropriate paths and names for your data
image_path =os.path.join(os.path.dirname(os.getcwd()),"Image_examples")#Replace this with the path to the folder where your images are stored, for example in Windows: r"C:\Users\Documents\ProbeLabeler\docs\Image_examples" 
data_path = os.path.join(os.path.dirname(os.getcwd()),"Data_Folder")#Replace this with the path to the folder where your data are stored, for example in Windows: r"C:\Users\Documents\ProbeLabeler\docs\Data_Folder"
data_table = 'Data_example.xlsx' # This is the name of your datatable (excel file)
sheet_name = 'Sheet1' # Sheet name where the data is

image_file = "MLA-MLP_NFI-1.tif" #Name of the image you want to process (Replace with your own)

# Next is the configuration setup, it controls dot size and color, text size, color and positioning, white box behind text or not, scale bar size and color, etc. 
# You can run it with the defaults, or you can change as you want. 
# suffix specifies what suffix is at the end of the name of the files,

# IMPORTANT_NOTE: I highly recommend adding a suffix to your "SAMPLE" column in the data excel file, here the default is -, _ or . 
# Just add _ , - or . at the end of all your sample names in excel

config=pl.ImageAnnotatorConfig() # This will use the default configuration
save_fig='pdf' # Format of output image, this is pdf editable. Options are png, tif, pdf
show_bbox=False # show white box or not behind text
plot_result=True # show the plot or not

# If you want to change anything (color, text size, etc), uncomment the following "config=..." and change it as desired 
# (i.e., point_color='k' will plot the point in black instead of royal blue):

# config = ImageAnnotatorConfig(
#     point_color='royalblue',
#     text_color='royalblue',
#     scalebar_color='k',
#     scalebar_text_color='k',
#     point_size=5,
#     text_offset_x=0,
#     text_offset_y=-30,
#     font_size=7,
#     font_thickness=2,
#     scalebar_xy=(100, 900),
#     scalebar_thickness=2,
#     suffix="[-_.]",
#     meta_extension=".txt",
#     Sample_ID='SAMPLE',
#     xposition='X_POS', 
#     yposition='Y_POS'
# )

annotated_image = pl.annotate_image(image_path, data_path, data_table, sheet_name, image_file, config,plot_result=plot_result,save_fig=save_fig,show_bbox=show_bbox)