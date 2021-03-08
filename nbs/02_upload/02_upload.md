```python
# default_exp upload
```

# Uploader

> We wrap all the functionality of the tools built in the `API` and the `converter` modules to upload the rendered markdown document to Medium


```python
#hide
from nbdev.showdoc import *
```


```python
#export
import os
from nb2medium.mediumapi import post_article
from nb2medium.convert import (
    HidePreprocessor,
    GisterPreprocessor, 
    ImagePreprocessor,
    WriteMarkdown,
    init_logger
)
from nbconvert.exporters import MarkdownExporter
from nbconvert.preprocessors import TagRemovePreprocessor
import logging
from fastcore.script import *

@call_parse
def nb2medium(
    title:Param("The title of your article"), 
    notebook:Param("Path to your notebook"),
    log_level:Param("The minimum reported logging level (debug, info, warning, error or critical)") = 'info',
    #log_to_stdout:Param("Whether logging should be redirected to stdout (internal use)", store_true) = False
):
    
    if isinstance(log_level, str): log_level = log_level.upper()
    
    # convert logger
    init_logger('converter', log_level, log_to_stdout = log_to_stdout)
    init_logger('uploader', log_level, log_to_stdout = log_to_stdout)
    upload_logger = logging.getLogger('uploader')
    if not os.getenv('MEDIUM_TOKEN'): 
        upload_logger.critical('MEDIUM_TOKEN not found, please make sure MEDIUM_TOKEN is defined')
    else:
        upload_logger.debug('Detected MEDIUM_TOKEN')
    
    # declare exporter
    m = MarkdownExporter()
    # Hide Preprocessors
    m.register_preprocessor(HidePreprocessor(mode = 'source'), enabled = True)
    m.register_preprocessor(HidePreprocessor(mode = 'output'), enabled = True)
    m.register_preprocessor(HidePreprocessor(mode = 'cell'), enabled = True)
    m.register_preprocessor(
        TagRemovePreprocessor(
            remove_input_tags = ('hide-source',),
            remove_all_outputs_tags = ('hide-output',),
            remove_cell_tags = ('hide-cell',),
            enabled = True)
    )
    # Gister Preprocessors
    m.register_preprocessor(GisterPreprocessor(), enabled = True)
    #Image Preprocessors
    m.register_preprocessor(ImagePreprocessor(), enabled = True)
    
    # process notebook
    b,r = m.from_filename(notebook)
    
    # write notebook to Markdown
    path, name = os.path.split(notebook)
    basename, ext = os.path.splitext(name)
    WriteMarkdown(b,r, filename = basename)
    md_home = os.path.join(path, basename, f"{basename}.md")
    
    # upload markdown document as medium post
    post_request = post_article(
        title = title, 
        content = open(md_home).read()
    )

    upload_logger.info(f"Draft of '{title}' from {os.path.basename(notebook)} notebook uploaded to Medium: {post_request.json()['data']['url']}")
    
```


```python
first_article = nb2medium(title = 'First test',
                          notebook = '../samples/test-notebook.ipynb')
```

    converter:INFO - Found a hide-source tag in cell #35.
    converter:INFO - Found a hide-output tag in cell #36.
    converter:INFO - Found a hide-cell tag in cell #37.
    converter:INFO - Gist notebooktest.py from cell 26 succesfully uploaded!
    converter:INFO - Gist print.py from cell 27 succesfully uploaded!
    converter:INFO - Gist pandas.py from cell 30 succesfully uploaded!
    converter:INFO - Gist pandas.py.csv from cell 30 succesfully uploaded!
    converter:INFO - Gist pandas-doubleupload.py from cell 33 succesfully uploaded!
    converter:INFO - Gist pandas-doubleupload.py.csv from cell 33 succesfully uploaded!
    converter:INFO - Detected 4 plots and 2 local images in notebook.
    converter:INFO - Markdown document written to ../samples/test-notebook/test-notebook.md
    uploader:INFO - Draft of 'First test' from test-notebook.ipynb notebook uploaded to Medium: https://medium.com/@lucha6/5b2bc2673bd8



```python
#hide
from nbdev.export import *
notebook2script()
```

    Converted 00_mediumapi.ipynb.
    Converted 01_convert.ipynb.
    Converted 02_upload.ipynb.
    Converted index.ipynb.

