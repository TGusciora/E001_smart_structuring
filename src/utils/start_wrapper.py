def wrapper_notebook_settings():
    """
    Configures settings specific to IPython/Jupyter notebooks.

    This function checks if the code is running in an IPython/Jupyter notebooks session.
    If it is, it enables autoreloading of modules, sets matplotlib to inline mode.
    If it is not, it prints a message indicating that it is not in a notebooks session.
    
    Note:
        - This function requires the IPython, matplotlib, pandas module to be installed.

    Raises:
        None

    Returns:
        None
    """
    try:
        __IPYTHON__
        _in_ipython_session = True
    except NameError:
        _in_ipython_session = False
    if _in_ipython_session:
        from IPython import get_ipython
        get_ipython().run_line_magic("load_ext", "autoreload")
        get_ipython().run_line_magic("autoreload", "2")
        get_ipython().run_line_magic("matplotlib", "inline")
    else:
        print("Not in IPython/Jupyter notebooks session")
