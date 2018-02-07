#!/bin/bash
#This bash script fixes the "stop_times.txt" of the transitfeed module to our format.

while IFS='' read -r line || [[ -n "$line" ]]; do
  line=$(expr "$line" : '\([^\,]*\,[^\,]*\,[^\,]*\,[^\,]*\,[^\,]*\)')
  i=$((${#line}-1))
  if [ "${line:$i:1}" == "," ] 
  then
    line+="0"
  fi
  echo "$line" >> "temp"
done < $1
mv "temp" "$1"