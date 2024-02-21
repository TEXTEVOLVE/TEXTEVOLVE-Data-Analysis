# import python modules needed to execute task
from pathlib import Path

# Variables you might want to modify - you can turn these into command-line arguments later
data_directory = Path("Manuscripts")  # Current working directory is assumed
output_file_suffix = "_whole.txt"  # this will append the text in quotes to the name of the file created by this code.
excluded_filenames = [".DS_Store", "Other_Thing"]  # we don't want the code to pay attention to these files
verses_sort_key = ('Ex14.30', 'Ex14.31', 'Ex15.1', 'Ex15.2', 'Ex15.4', 'Ex15.5', 'Ex15.6',
                   'Ex15.7', 'Ex15.8', 'Ex15.9', 'Ex15.10', 'Ex15.11', 'Ex15.12', 'Ex15.13', 'Ex15.14', 'Ex15.15',
                   'Ex15.16', 'Ex15.17')


# Get list of file Paths from specified directory Path - so computer can identify them
def get_file_list(dir_path):
    return [filepath for filepath in dir_path.iterdir() if
            filepath.is_file() and filepath.name not in excluded_filenames]


# Sort file Paths by sort key - because python has its own ordering system which does not fit human readability.
def sort_file_list(filepath_list, sort_key):
    def sort_by_key(file_name, key):
        return key.index(file_name)

    return sorted(filepath_list,
                  key=lambda filepath: sort_by_key(filepath.name.split('.txt')[0].split('_')[1], sort_key))


# Append file Paths in list to a single output file
def append_files(filepath_list, output_suffix):
    # Output files are named according to the parent directory and saved in the same directory as the data_directory
    output_file = Path(f"{filepath_list[0].parent}{output_suffix}")

    with output_file.open('w', encoding="utf8") as out:
        for filepath in filepath_list:
            with filepath.open('r', encoding="utf8") as f:
                out.write(f.read())


# Get list of directory Paths from specified directory
def get_dir_paths(data_dir):
    return [dir_path for dir_path in data_dir.iterdir() if dir_path.is_dir()]


# Merge files in a single directory
def merge_files_in_directory(dir_path):
    # Get file list from specified directory path
    files = get_file_list(dir_path)

    # Sort the file list
    sorted_files = sort_file_list(files, verses_sort_key)

    # Append the files to output text file
    append_files(sorted_files, output_file_suffix)


# Run the script steps
def run():
    # Get all directory paths in a given data directory
    for d in get_dir_paths(data_directory):
        # For each directory, merge files
        merge_files_in_directory(d)

# this statement tells the python interpreter to run the code.
if __name__ == '__main__':
    run()
