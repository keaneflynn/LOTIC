#!/bin/bash

if [ $# != 1 ]; then
	echo "Usage: ./compile_tflite.sh <input filename>"
	exit 1
fi

input_filename=$1
image_name=edgetpu_compiler

docker build -t ${image_name} .

docker run --rm -it -v $(pwd):/home/edgetpu ${image_name} /usr/bin/edgetpu_compiler ${input_filename}

echo "Wrote compiled edge tpu file"
