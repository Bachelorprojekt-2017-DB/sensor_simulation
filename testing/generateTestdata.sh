#!/bin/bash
#This bash script generates a new GTFS directory with specific routes from a larger one.

fixStopTimes()
{
	while IFS='' read -r line || [[ -n "$line" ]]; do
		line=$(expr "$line" : '\([^\,]*\,[^\,]*\,[^\,]*\,[^\,]*\,[^\,]*\)')
		i=$((${#line}-1))
		if [ "${line:$i:1}" == "," ] 
		then
	    		line+="0"
		fi
		echo "$line" >> "temp"
	done < "$@"
	mv "temp" "$@"
}

####### MAIN
temp="tempFolder"

python "deleteTripsAndRoutes.py" "$1" "$temp" "$3"
mkdir "$2"
mv "$temp" "$2""/""$temp"
cd "$2"
unzip "$temp"
rm "$temp"
fixStopTimes "stop_times.txt"
cd ..
python filter_unused_stops.py "$2" "$temp"
rm -r "$2"
mkdir "$2"
mv "$temp" "$2""/""$temp"
cd "$2"
unzip "$temp"
rm "$temp"
fixStopTimes "stop_times.txt"
cd ..
