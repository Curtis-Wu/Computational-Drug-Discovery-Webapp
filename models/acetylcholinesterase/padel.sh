input_file=$1
output_file=${input_file%.*}_descriptors_output.csv

java -Xms1G -Xmx1G -Djava.awt.headless=true -jar ./models/PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./models/PaDEL-Descriptor/PubchemFingerprinter.xml -dir ./ -file $output_file -threads 0 -maxruntime 0 $input_file