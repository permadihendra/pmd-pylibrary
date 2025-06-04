import os


def check_file_in_directory(directory_path: str):
    """
    List and print all file names in the specified directory, excluding subdirectories.

    Args:
        directory_path (str): The absolute or relative path to the directory.

    Process:
        1. Lists all entries in the directory.
        2. Filters out any subdirectories, keeping only regular files.
        3. Prints each file name with an index number.

    Example:
        >>> check_file_in_directory("./data")
        0 report1.csv
        1 summary.txt
        2 results.json
    """
    # List all files and folders in the directory
    file_list = os.listdir(directory_path)

    # Filter out directories (keep only files)
    file_list = [
        f for f in file_list if os.path.isfile(os.path.join(directory_path, f))
    ]

    # Print the filenames with index
    i = 0
    for filename in file_list:
        print(i, filename)
        i = i + 1
