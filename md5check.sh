#!/bin/bash
#Generate md5deep hash, exluding this script, the stored md5 sum, and all git$

cd "$(dirname "$0")"
#Depending of the type of os, either md5sum or md5 command is used. 
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    md5cmd="md5sum"
    endcmd="-exec sh -c \"md5sum {} | cut -c 1-32 \" \; | sort"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    md5cmd="md5 -q"
    endcmd="-exec md5 -q {} + | sort"
fi

#Construct a find command, ignoring all the .gitignore files. 
inputfile=".gitignore"
var='find . -type f ! -path "*.git*" ! -iname "md5*" '
while IFS= read -r line
do
if [[ $line == *"."* ]] && [[ $line != "#"* ]] && [ "$line" != "\n" ] && [ "$line" != "" ]; then
        var+="! -iname \"$line\" " 
    fi
done < "$inputfile"


#If the -g/--generate arguement is provided, it writes the calculated md5sum into a md5verify file
if [[ $1 == "-g" ]] || [[ $1 == "--generate" ]]; then
    var+="$endcmd | $md5cmd | awk '{ print \$1 }' > md5verify "
    eval $var
    echo Generated md5sum written into md5verify: $(cat md5verify) 
#If no arguements are provided, just print out the calculated checksum to stdout
else
    var+="$endcmd | $md5cmd | awk '{ print \$1 }' "
    eval $var
fi
