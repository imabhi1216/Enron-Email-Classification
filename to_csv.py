import os
import csv
# Define the output file name
output_file = 'out_new.csv'

# Create an empty list to store the text data
text_data = []
for i in [1,2,3,4,5,6]:
    # Define the root directory to search for files


# Define the root directory to search for files
    root_directory = f'C:\\Users\\Abhishek\\Desktop\\Vlabs_assessment\\processed\\{i}'

    

    # Walk through the root directory and read the text from each file
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.endswith('.txt'):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r') as infile:
                    text = ''.join(infile.readlines()) # read all the text in the file and join it together
                    folder_name = os.path.basename(dirpath)
                    text_data.append((filename, text, folder_name))
    # Write the text data to a CSV file
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['File Name', 'Text', 'Folder Name'])
        writer.writerows(text_data)


