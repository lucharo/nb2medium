__version__ = "0.0.1"


# Jupyter Extension points
def _jupyter_nbextension_paths():
    """
    (From jupytext)
    Allows commands like
    jupyter nbextension install --py nb2medium
    jupyter nbextension enable --py nb2medium"""
    return [
        dict(
            section="notebook",
            # the path is relative to the `nb2medium` directory
            src="nbextension",
            # directory in the `nbextension/` namespace
            dest="nb2medium",
            # _also_ in the `nbextension/` namespace
            require="nb2medium/nb2medium",
        )
    ]
