# Publications

Welcome! Here you will find Python source code that was used to import, process and plot geochemical data for scientific publications. This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.

## Wesenlund et al. (2021) - Marine and Petroleum Geology

Fredrik Wesenlund, Sten-Andreas Grundvåg, Victoria Sjøholt Engelschiøn, Olaf Thießen, and Jon Halvard Pedersen (2021).
"Linking facies variations, organic carbon richness and bulk bitumen content – A case study of the organic-rich Middle Triassic shales from eastern Svalbard."
*Marine and Petroleum Geology* **132**, 105168.
DOI: https://doi.org/10.1016/j.marpetgeo.2021.105168

## Wesenlund et al. (2022) - The Depositional Record

Fredrik Wesenlund, Sten-Andreas Grundvåg, Victoria Sjøholt Engelschiøn, Olaf Thießen, and Jon Halvard Pedersen (2022).
"Multi-elemental chemostratigraphy of Triassic mudstones in eastern Svalbard: implications for source rock formation in front of the World’s largest delta plain."
*The Depositional Record*.
DOI: https://doi.org/10.1002/dep2.182

## Wesenlund et al. (in prep.) - Paper III in PhD degree

Currently in preparation.

## GC-MS data extraction

This folder includes raw GC-MS data (.raw file extension) of the Norwegian Geochemical Standard North Sea Oil - 1 (NGS NSO-1) analyzed using a Thermo Scientific Trace 1310 gas chromatograph coupled to a Thermo Scientific TSQ 8000 Triple Quadrupole MS quadropole instrument. The .raw file is converted to a .txt file using Thermo Xcalibur Roadmap --> Tools --> File converter (v. 3.1.66.10). The resulting .txt file is then imported by the .py script, which subsequently extracts the m/z ratios from the .txt file and exports these as a .csv file. In the .csv file, each column represent a m/z ratio (e.g., 191 [terpanes]), and an extra column which shows the instrument run time (9 to 125 minutes) is added. Some benefits of extracting the single ion monitoring (SIM) data from a .raw file to a .csv spreadsheet file are provided below:

* The data is non-proprietary and can therefore be investigated by readers who do not own the described proprietary software solutions
* The data can easily be read by other (open-source) software solutions for further processing or plotting, e.g. using Python and associated libraries
* The data can be stored in a data repository using common conventions (i.e., as a .csv file rather than a proprietary binary file)
* If the metadata included in the .raw file is deemed unnecessary, the file size per sample can be reduced significantly using the Python script above

## GC-FID data extraction

This folder includes raw GC-FID data (.cdf file extension) of the Norwegian Geochemical Standard North Sea Oil - 1 (NGS NSO-1) analyzed using a Varian 3800 GC-FID instrument. The .cdf file is converted from a .run file using the Varian Star Chromatography Workstation Interactive Graphics software (v. 6.30). The resulting .cdf file is then imported by the .py script, which subsequently extracts the FID response (in volts [V]) from the .txt file and exports these data as a .csv file. An extra column including the instrument run time (0 to 90 minutes) is added in the .csv file.

Many of the benefits described in the previous section also applies to this approach.
