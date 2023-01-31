# Hydrotel-Telemac_results
Process and analyse results from Hydrotel and Telemac2D
___

Using Hydrotel results in the form of text files containing flow timeseries:

1. Read hydrotel results and generate a hydrograph of a particular event to be used in a Telemac Unsteady state simulation
2. Build and plot flow-duration curves and plot a subset of the flow timeseries (a hydrograph).
3. Use flow results with water stage measurmentes (made with level-loggers) to determine the most probable flows for multiple water elevations. This is used later to determine a rating curve at the outlet of the lakes.

Then, using Telemac2D results generated with BlueKenue:

1. Use water stage result timeseries to analyse maximum water elevations for multiple hydrographs. Plot result figures.
2. Use water depth mesh to extract and analyse maximum and minimum water extensions for multiple hydrographs. Create files with the grid coordinates and depth for each condition.
