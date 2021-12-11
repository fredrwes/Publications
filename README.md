# Publications

Welcome to my GitHub! Here you will find Python source code that was used to import, process and plot geochemical data for publications. This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.

## Wesenlund et al. (2021) - Marine and Petroleum Geology

Fredrik Wesenlund, Sten-Andreas Grundvåg, Victoria Sjøholt Engelschiøn, Olaf Thießen, and Jon Halvard Pedersen.
"Linking facies variations, organic carbon richness and bulk bitumen content – A case study of the organic-rich Middle Triassic shales from eastern Svalbard."
*Marine and Petroleum Geology* **132**.
DOI: https://doi.org/10.1016/j.marpetgeo.2021.105168


## Wesenlund et al. (in preparation) - The Depositional Record

Currently in preparation.

## GC-MS data batch processing

This folder includes raw GCMS data (.raw file extension) of the Norwegian Geochemical Standard North Sea Oil - 1 (NGS NSO-1) analyzed using a Thermo Scientific GCMS quadropole instrument. The .raw file is converted to a .txt file using Thermo Xcalibur Roadmap --> Tools --> File converter (v. 3.1.66.10). The resulting .txt file is then imported by the .py script, subsequently extracting the m/z ratios from the .txt file and exported these within a .xlsx file, where each column represent a m/z ratio (e.g., 191 [terpanes]). An extra column including the instrument run time (0 to 120 minutes) is added. The benefits of extracting the single ion monitoring (SIM) data from a .raw file to a .xlsx or a .csv spreadsheet file are many:

* The data is non-proprietary (if in .csv format) and can therefore be investigated by readers who do not own the described proprietary software solutions
* The data can easily be read by other (open-source) software solutions for further processing or plotting, e.g. using Python and associated libraries
* The data can be stored in a data repository using common conventions (i.e., as a .csv file rather than a proprietary binary file)
* if the metadata included in the .raw file is deemed unnecessary, the amount of data per sample can be reduced significantly using the Python script above

## GC-FID data batch processing

Currently in preparation.
