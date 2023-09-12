# ProbeLabeler
 ProbeLabeler (created by C. Devitre - https://github.com/cljdevitre/ProbeLabeler) is designed to label images taken on electron microprobes, based on the coordinates of the image and the coordinates of datapoints. It has only been tested for use with JEOL probes and with excel data as exported by Probe for EPMA software (https://www.probesoftware.com/). If you need other applications, contact me, I can implement more options. Please mention my Github when using ProbeLabeler!

 There are two possibilities with ProbeLabeler:
 1) You can use a Jupyter Notebook (see docs/JupyterNotebook_example) to run it. You can either pip install ProbeLabeler locally, or you can copy the jeol_labeler.py file from src folder to the folder where you will run your Jupyter Notebook from (to bypass the pip install - see notebook for details)
 2) You can use ProbeLabeler from a python command line. Example scripts and instructions are provided in docs/Python_script_example
