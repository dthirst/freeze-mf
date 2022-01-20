# freeze-mf - a simple tool for making montages of cryoEM screening images
written 2022 by demian keihsler at the institute of molecular pathology, vienna
********
usage:<br/>
* save the files you want to be in the montage in the following pattern in **one folder**:<br/>
  * `<name>_map.<ext>`,<br/>
  * `<name>_square.<ext>`,<br/>
  * `<name>_hole.<ext>`,<br/>
  * `<name>_i1.<ext>`,<br/>
  * `<name>_i2.<ext>`<br/>
* you can have as many different groups of files as you want, as long as files that belong together always start with the same name and have the same extension. the script will iterate through the folder and make a montage for each group that has at least a file whose name ends with `_map`.
* start the script by writing `python3 <path-to-script>/freeze.mf -p <path-of-files>`<br/>
* the montages will be save in the same folder with the naming pattern `<name>_montage.png`<br/>
* please mind the following **expected** behaviour:
	* if you have a map file but no square and smaller, **the montage will contain only the map**. same for square but no hole, hole but no i1/i2.<br/>
  * if you have a square and/or any other file but **no map, there will be no montage**.<br/>
* thank your local technician 🍻
********
