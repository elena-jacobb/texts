
#######################################################################
# NLP data pre-processing I : converting .docx files into .txt files
#######################################################################

#-------------------------------------------------------
# 1. Rename Word documents to UUID names (anonymization)
#-------------------------------------------------------

# If needed, check installed Python versions (different conda environments have different versions of Python)
# and executable Python (where your system looks for pip-installed packages).
# import sys
# print(sys.path)
# print(sys.executable)

# Install docx2txt package where your executable Python is.
# Ex:
#!~/anaconda3/bin/python -m pip install docx2txt
# (try 'sudo pip install docx2txt' if any problems')

# To start, the parent directory has a single "source_files" directory with document folders containing Word files.
# NOTE: any zipped Word files should be unzipped in "source_files", before proceeding.

import os
import shutil
import uuid
import docx2txt

import re
import random


def create_directory_if_not_exists(targetDir):
    if not os.path.exists(targetDir):
        os.mkdir(targetDir)
        print("Directory '" + targetDir + "' created ")
    else:
        print("Directory '" + targetDir + "' already exists")
    return os.path.join(os.getcwd(), targetDir)


def copytree(src, dst, symlinks=False, ignore=None):

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def count_files(folder):
    count = 0
    for file in os.listdir(os.path.join(os.getcwd(), folder)):
        count += 1
    return count


def check_if_dir_exists(targetDir):
    if not os.path.exists(targetDir):
        print("Directory '" + targetDir + "' removed.")
    else:
        print("Directory '" + targetDir + "' exists.")


def remove_space(text):
    text = text.strip()
    text = text.split()
    return " ".join(text)


def show_random_text(sourceDir):
    rand_text = random.choice(os.listdir(sourceDir))
    
    while rand_text[0] == ".":
        rand_text = random.choice(os.listdir(sourceDir))

    with open(os.path.join(source_dir, rand_text), "r") as f:
            data = f.read()
    print(data)


# Duplicate all "source_files" directory

# current_dir = os.path.dirname(os.getcwd()) # this is a parent folder
current_dir = os.getcwd()

source_dir = os.path.join(current_dir, "source_files")
target_dir = create_directory_if_not_exists("temp1")


copytree(source_dir, target_dir)

# 2. Give docx files UUID names and place them in temp2 directory.

source_dir = os.path.join(os.getcwd(), "temp1")
target_dir = create_directory_if_not_exists("temp2")

for foldername in os.listdir(source_dir):

    # Skip hidden ".DS_Store" files in MacOS
    if foldername[0] != ".":
        subdirectory = os.path.join(os.getcwd(), "temp1", foldername)

        for filename in os.listdir(subdirectory):
            if filename[0] != ".":
                if filename.startswith("Contrat"):
                    file, extension = os.path.splitext(filename)
                    # replace file name with uuid-name
                    unique_filename = str(uuid.uuid4()) + extension
                    # rename original file with uuid-name and move into 'temp2' directory
                    os.rename(os.path.join(subdirectory, filename), os.path.join(target_dir, unique_filename))

num_original_documents = count_files(target_dir)

print("=" * 40)
print(f"Number of original Word files: {num_original_documents}")
print("=" * 40)





#-----------------------------------------
# 2. Convert Word files to .txt files
#-----------------------------------------

source_dir = os.path.join(os.getcwd(), "temp2")
target_dir = create_directory_if_not_exists("text_files")

for process_file in os.listdir(source_dir):

    if process_file[0] != ".":
        file, _ = os.path.splitext(process_file)

        # Create a new text file name by concatenating the .txt extension to file UUID
        dest_file = file + '.txt'
        print(dest_file)

        # extract text from the file
        content = docx2txt.process(os.path.join(source_dir, process_file))

        write_text_file = open(os.path.join(target_dir, dest_file), "w+")

        # write the content and close the newly created file
        write_text_file.write(content)
        write_text_file.close()

print("=" * 40)
print(f"Number of original Word files: {num_original_documents}")
print(f"Text files created: {count_files(target_dir)}")
print("=" * 40)


#-----------------------------------------
# 3. Delete temp1 and temp2 directories.
#-----------------------------------------

dir1 = os.path.join(os.getcwd(), "temp1")
dir2 = os.path.join(os.getcwd(), "temp2")
shutil.rmtree(dir1)
shutil.rmtree(dir2)

check_if_dir_exists("temp1")
check_if_dir_exists("temp2")


# remove internal spaces

source_dir = os.path.join(os.getcwd(), "text_files")

for filename in os.listdir(source_dir):
            
    # skip hidden files
    if filename[0] != ".":
        
        with open(os.path.join(source_dir, filename), "r") as f:
            data = f.read()
        
        data = remove_space(data)
        
        with open(os.path.join(source_dir, filename),'w') as f:
            f. write(data)

