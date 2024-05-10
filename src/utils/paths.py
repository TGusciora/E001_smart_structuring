import os


def paths_dictionary():
    """
    Creating dictionary with paths in the parent/project directory.

    Crawls through folders except names starting with '.' and '_'.
    Returns a dictionary with folder paths separated with "_" as
    keys and their true paths as values.

    Notes
    -------------------
    Required libraries: \n
    * import os

    Returns
    --------
    data : dictionary
           Dictionary with paths.
    """
    parent_path = os.path.dirname(os.getcwd())
    paths_dict = {}
    for root, dirs, files in os.walk(parent_path):
        # Delete all folders starting with '.' and '_' and their subfolders
        dirs[:] = [
            d for d in dirs if not d.startswith(".") and not d.startswith("_")
        ]

        for dir in dirs:
            folder_path = os.path.join(root, dir) + "/"
            # Adding dictionary keys, replacing separators to "_" and deleting paths before parent
            dict_key = (
                folder_path.replace(parent_path, "")
                .strip(os.sep)
                .replace(os.sep, "_")
            )
            paths_dict[dict_key] = folder_path
        paths_dict[parent_path.replace(os.sep, "")] = parent_path + "/"
    return paths_dict
