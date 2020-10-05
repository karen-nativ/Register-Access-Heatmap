# Register Access Heatmap
This tool displays a heatmap of accesses to registers in e code.

----------------------
Prerequisites
----------------------
This tool requires the following libraries/modules be installed within the Python
environment you are running this script in:
* `mpl_toolkits.axes_grid1.inset_locator.InsetPosition`
* `matplotlib.pyplot` (Matplotlib Version >= 3.1)
* `matplotlib.widgets`
   * `Slider`
   * `RadioButtons`
* `collections.namedtuple`
* `math`


This tool requires Specman to run in the environment, and the following environment variables to be configured:
* `PYTHONPATH` - the path to the python file
* `SPECMAN_PYTHON_INCLUDE_DIR`
* `SPECMAN_PYTHON_LIB_DIR`
* `SPECMAN_PATH`
(See Specman reference for details regarding these variables)
    
This tool requires the use of the vr_ad utility.
The vr_ad root folder must be included in the `SPECMAN_PATH` environment variable.


----------------------
Initialization
----------------------
In order to run the tool, the user must first run the following command:

`specman -64 -p 'load map_report.e'`

   
If the map_report.e file is not in the current directory, load it from a relative/absolute path.

Afterward, the user must load the file that accesses registers to Specman.

Example: `load my_reg_accesses.e`


----------------------
Usage
----------------------
To run the tool, start the test by running the following command:
	`test`


----------------------
Examples
----------------------
These uses run on examples from the vr_ad utility:

`specman -64 -c 'load vr_ad/examples/vr_ad_reg_cover.e map_report; test'`

`specman -64 -c 'load vr_ad/examples/vr_ad_rw_from_any_tcm.e map_report; test'`

---------------------
Output
----------------------
The tool creates an interactive heatmap of the registers and the amount they have been accessed.

The terminal running the figure will wait for the figure to be closed before running additional commands.
