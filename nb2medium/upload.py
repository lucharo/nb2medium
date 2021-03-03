# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/02_upload.ipynb (unless otherwise specified).

__all__ = ['nb2medium']

# Cell
import os
from .mediumapi import post_article
from .convert import (
    HidePreprocessor,
    GisterPreprocessor,
    ImagePreprocessor,
    WriteMarkdown,
    init_logger
)
from nbconvert.exporters import MarkdownExporter
from nbconvert.preprocessors import TagRemovePreprocessor
import logging

def nb2medium(
    title,
    notebook,
    log_level = 'info',
    log_to_stdout = False
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
