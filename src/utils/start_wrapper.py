def wrapper_notebook_settings():
    """
    Enabling autoreload and inline plotting in Jupyter notebooks.

    Autoreload causes modules to be reloaded each time before execution.
    This saves time on re-importing the package after each change.
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
    
