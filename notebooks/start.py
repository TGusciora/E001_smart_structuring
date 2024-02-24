# Load packages wrapper
def start_wrapper():
    import src.utils.start_wrapper
    src.utils.start_wrapper.notebook_settings()

    # import packages
    # \src\utils\start_wrapper.py
    src.utils.start_wrapper.import_packages()

    # Load dictionary of project paths
    import src.utils.paths
    paths = src.utils.paths.paths_dictionary()
    print("Contents of paths dictionary:")
    for key in paths:
        print(key, ": ", paths[key])

    # Load environment variables
    from dotenv import load_dotenv
    print("Are variables loaded from .env?")
    load_dotenv()
    print(load_dotenv())  # take environment variables from .env.
