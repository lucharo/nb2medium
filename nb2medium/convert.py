# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_convert.ipynb (unless otherwise specified).

__all__ = ['init_convert_logger', 'WriteMarkdown', 'HidePreprocessor', 'check_gh_auth', 'upload_gist',
           'GisterPreprocessor', 'ImagePreprocessor']

# Cell
from nbconvert import MarkdownExporter, FilenameExtension
from nbconvert.writers import FilesWriter

# Cell
import logging

def init_convert_logger(level = logging.INFO):
    #delete loggger if it exists
    if len(logging.getLogger('converter').handlers) != 0:
        logging.getLogger('converter').\
        removeHandler(logging.getLogger('converter').handlers[0])

    # create logger
    logger = logging.getLogger('converter')
    logger.setLevel(level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # create formatter
    formatter = logging.Formatter('%(name)s:%(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

# Cell
init_convert_logger(logging.DEBUG)

# Cell
def WriteMarkdown(body, resources, dir_path = None, filename = None):
    """
    body & resources are the output of any Jupyter nbconvert `Exporter`.
    dir_path should be a relative path with respect to the current working directory.
    If dir_path is not passed, the output document and its auxiliary files will be written
    to the same location than the input jupyter notebook
    filename should be the output document's name

    This function returns the location of the newly written file
    """
    logger = logging.getLogger('converter')
    markdown_location = FilesWriter(build_directory = '' if dir_path is None else dir_path) \
    .write(
        output = body,
        resources = resources,
        notebook_name = filename
    )
    logger.info(f"Markdown document written to {markdown_location}")

# Cell
from nbconvert.preprocessors import RegexRemovePreprocessor

# Cell
from nbconvert.preprocessors import Preprocessor, TagRemovePreprocessor
from traitlets import List, Unicode, Set
import re

class HidePreprocessor(Preprocessor):
    """
    Preprocessor that hides cell's body and only keeps the output based on regex matching

    Regex matching is based on the [RegexRemovePreprocessor source]
    (https://github.com/jupyter/nbconvert/blob/master/nbconvert/preprocessors/regexremove.py)

    """

    def __init__(self, mode:str):
        self.mode = mode
        if mode not in ('source', 'output', 'cell'):
            raise Exception(f"Mode {mode} not supported")
        self.pattern = f'^#.*%\s*hide-{mode}'
        self.logger = logging.getLogger('converter')

    def preprocess_cell(self, cell, resources, cell_index):
        """
        Preprocessing to apply to each cell.
        """

        cell, resources = self.hide_(cell, resources, cell_index)

        return cell, resources

    def hide_(self, cell, resources, cell_index):

        mode = self.mode
        has_keyword = re.search(self.pattern, cell.source.split('\n')[0])
        # gist handling
        if has_keyword:
            self.logger.debug(f"Found a hide-{mode} tag in cell #{cell_index}.")
            cell.metadata.tags = [f'hide-{mode}']

        return cell, resources


# Cell
import os
def check_gh_auth():
    logger = logging.getLogger('converter')
    if not os.getenv('GITHUB_TOKEN'):
        logger.warning('Please declare your GITHUB_TOKEN as an environment variable, \
        read more here: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token')
        return False
    else:
        logger.debug('GITHUB_TOKEN environment variable found.')
        return True

# Cell
from requests import post
import json

def upload_gist(gistname , gistcontent, description = "", public = False):
    """
    description: Description of gist, i.e. some metatext explaining what the gist is about
    gistname: name displayed for the gist, this impacts how the file is rendered based
    on the extension (e.g. script.py, README.md, script.R, query.sql...)
    gistcontent: this maybe the name of a file or just a a string describing a program
    public: whether the gist should be public or private
    """
    if os.path.isfile(gistcontent):
        gistname = gistcontent if gistname is None else gistname
        gistcontent =  open(gistcontent, 'r').read()

    post_req = post("https://api.github.com/gists",
                data = json.dumps({
                    'description': description,
                    'files': {gistname: {'content': gistcontent}},
                    'public': public
                }),
                headers = {
                    'Authorization': f"token {os.getenv('GITHUB_TOKEN')}",
                    "Accept": "application/vnd.github.v3+json"
                }
        )
    if post_req.ok:
        return post_req.ok, post_req.json()['html_url']
    else:
        raise Exception(f"There was an error uploading the gist {gistname}")

# Cell
import bs4
import pandas as pd

class GisterPreprocessor(Preprocessor):
    """
    Preprocessor that detects the presence of the #gist tag in a Jupyter Notebook cell,
    uploads the code in that cell as a GitHub gist for the authenticated user and replaces the original cell
    for a link to the gist in the resulting markdown file
    """

    pattern = '^#.*%\s*gist'
    is_auth = check_gh_auth()
    logger = logging.getLogger('converter')

    def get_params(self,cell, **kwargs):
        keywords = ['description', 'gistname', 'public', 'upload']
        params_string = re.search(r"%\s*gist\s*(.*)", cell.source.split('\n')[0])
        if params_string is None:
            raise Exception('Cell was labelled with a #gist tag but no parameters were passed')
        else:
            params_string = params_string.group(1)

        for keyword in keywords:
            params_string = params_string.replace(keyword, f'\n{keyword}')

        params_string = params_string.split('\n')[1:]
        params_dict = {}
        for param in params_string:
            param = param.split(':')
            # TODO write exception for when param[1] is not passed
            params_dict[param[0]] = param[1].strip()

        return params_dict

    def upload_gist_from_cell(self, cell, cell_index, params, content, n_output = 0):
        """
        output_number is 0 by default (source) or positive otherwise, if positive
        it corresponds to the n_output-th cell's output element
        """
        ok, gist_url = upload_gist(gistcontent = content, **params)
        if ok:
            self.logger.info(f"Gist {params['gistname']} succesfully uploaded!")
            if n_output == 0: append = False
            elif self.upload == 'output' and n_output > 1: append = True
            elif self.upload == 'both': append = True
            if not append:
                cell.source = f"[{gist_url}]({gist_url})"
            else:
                cell.source += f"\n[{gist_url}]({gist_url})"
        else:
            self.logger.error(f"Couldn't upload gist {params['gistname']}")

        return cell

    def handle_output(self, cell, cell_index, params):
        """
        The output of a Jupyter cell is a whole mess
        """

        # gist output handling
        # For each output we'll check the format and upload a separate gist
        for n_output, output in enumerate(cell.outputs):

            tbl_counter = 0
            # pandas tables are rendered as html tables and
            # hence can be detected via the <table> tag
            # and also the term dataframe
            if 'data' in output.keys():
                if 'text/html' in output.data.keys():
                    html_src = ''.join(output.data['text/html'])
                    if re.search('<table.*', html_src) is not None:
                        tbl_counter += 1
                        self.logger.debug(f"Found table in cell {cell_index}, uploading...")
                        # (try) turn html table into dataframe
                        try:
                            soup = bs4.BeautifulSoup(html_src,'lxml')
                            table = soup.find_all('table')
                            payload = pd.read_html(str(table), index_col = 0)[0].to_csv(index = False)
                            params['gistname'] += ".csv"
                        except:
                            self.logger.warning('Could not turn table to dataframe, uploading as html file')
                            payload = html_src
                            params['gistname'] += ".html"

                elif 'text/plain' in output.data.keys():
                    self.logger.debug(f"Uploading output from cell {cell_index} as text file...")
                    # output.data['text/plain'] returns a list so we join in into a string
                    # on its way out
                    payload = ''.join(output.data['text/plain'])
                    params['gistname'] += ".txt"


            elif 'output_type' in output.keys() and output.output_type == 'stream':
                self.logger.debug(f"Detected printed output in cell {cell_index}, uploading...")
                payload = ''.join(output.text)
                params['gistname'] += ".txt"

            cell = self.upload_gist_from_cell(cell, cell_index, params, payload, n_output + 1)

        return cell, tbl_counter

    def preprocess_cell(self, cell, resources, cell_index):
        """
        Preprocessing to apply to each cell.
        """
        self.upload = 'source' # default

        has_keyword = re.search(self.pattern, cell.source.split('\n')[0])
        # gist handling
        if has_keyword:
            if self.is_auth:
                params = self.get_params(cell)
                self.logger.debug(f"Detected gist tag in cell {cell_index}  with arguments: {', '.join(params.keys())}; uploading...")

                if 'upload' in params.keys():
                    self.upload = params['upload']
                    del params['upload']

                # upload cell source
                payload = '\n'.join(cell.source.split('\n')[1:])
                cell = self.upload_gist_from_cell(cell, cell_index, params, content = payload)

                # upload output if user chose to
                if self.upload != 'source':
                    cell, tbl_counter = self.handle_output(cell, cell_index, params)

                # Finally change cell_type to markdown to get rid of outputs
                # and ensure good formatting of links
                cell.cell_type = 'markdown'

            else: self.logger.info("Gist not uploaded as GITHUB_TOKEN could not be found.")



        return cell, resources


# Cell
from .mediumapi import post_image
from binascii import a2b_base64
from random import randint #to generate new cell ids

class ImagePreprocessor(Preprocessor):
    """
    Preprocessor that detects the presence of the image in a Jupyter Notebook cell's output,
    uploads the image to Medium
    """

    logger = logging.getLogger('converter')

    def preprocess(self, nb, resources):
        """
        Preprocessing to apply to each cell.
        Images can either be in a cell's output as a result of a plot being generated in the code (Scenario 1)
        Or they can be passed from a local file or the internet in a Markdown cell's source (Scenario 2)
        """

        n_items = len(nb['cells'])
        n = 0
        n_plots = n_local_images = 0
        while n < n_items:
            cell = nb['cells'][n]
            cell, newcell, img_count1 = self.upload_image_from_cell_output(cell, n)
            cell, img_count2 = self.upload_local_image_from_md(cell, resources, n)
            n_plots += img_count1
            n_local_images += img_count2
            nb['cells'][n] = cell
            if newcell is not None:
                n_items+=1
                #write next cell
                nb['cells'].insert(n+1, newcell)
                n+=1 # skip cell we've just created
            n+=1

        self.logger.info(f"Detected {n_plots} plots and {n_local_images} local images in notebook.")

        return nb, resources


    def upload_local_image_from_md(self, cell, resources, cell_index):
        # Scenario 2
        # extract name and path of notebook being processed
        name = resources['metadata']['name']
        path = resources['metadata']['path']
        img_counter = 0

        # regex matches the way of insert images in Markdown (e.g `![](somestring)`)
        if cell.cell_type == 'markdown' and re.match('!\[\]\(.*\)', cell.source):
            # figure out if path is local or online, if local upload
            # we use a capture group in the regex to directly extract the content
            # the image tag
            imgs = re.findall('!\[\]\((.*)\)', cell.source)
            for img in imgs:
                img_path = os.path.join(path, img)
                if os.path.isfile(img_path): # local file
                    img_counter += 1
                    self.logger.debug(msg = f"Detected {img_counter} local image(s) in cell {cell_index}, uploading...")
                    upload = post_image(filename = img_path)
                    ok, upload = upload.ok, upload.json()

                    if ok:
                        url = upload['data']['url']
                        self.logger.debug(msg = f"Image succesfully uploaded to {url}")
                        cell.source = re.sub(pattern = img,
                                         repl = url,
                                         string = cell.source)
                    else:
                        self.logger.error(msg = "Could not upload image to Medium!")

        return cell, img_counter

    def upload_image_from_cell_output(self, cell, cell_index):
        # Scenario 1
        newcell = None
        img_counter = 0
        if 'outputs' in cell.keys():
            # Iterate thorugh each output of the cell, if at least 1 image is found
            # clear all other content; for each img upload and replace with url
            # change cell to markdown (output removed in this operation)
            newcell = {'cell_type': 'markdown', 'id': str(randint(1e4, 1e5)), 'metadata':{}}
            for output in cell.outputs:
                # matplotlib images seem to be already in an ASCII PNG format
                # hence we are going with that
                if 'image/png' in output.data.keys():
                    img_counter += 1

                    self.logger.debug(msg = f"Detected {img_counter} plot(s) in cell {cell_index}, uploading...")
                    img_bin = a2b_base64(output.data['image/png'])

                    img = post_image(img = img_bin)
                    ok, img = img.ok, img.json()
                    if ok:
                        url = img['data']['url']
                        self.logger.debug(msg = f"Image succesfully uploaded to {url}")
                        newcell['source'] = f"![]({url})\n" if img_counter == 1 \
                        else '\n'.join([newcell['source'], f"![]({url})\n"])
                    else:
                        self.logger.error(msg = "Could not upload image to Medium!")


            if img_counter > 0: cell.outputs = []
            elif img_counter == 0: newcell = None

        return cell, newcell, img_counter
