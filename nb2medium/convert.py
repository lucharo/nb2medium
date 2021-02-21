# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_convert.ipynb (unless otherwise specified).

__all__ = ['WriteMarkdown', 'HidePreprocessor', 'check_gh_auth', 'upload_gist', 'GisterPreprocessor',
           'ImagePreprocessor']

# Cell
from nbconvert import MarkdownExporter, FilenameExtension
from nbconvert.writers import FilesWriter

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
    return FilesWriter(build_directory = '' if dir_path is None else dir_path) \
    .write(
        output = body,
        resources = resources,
        notebook_name = filename
    )

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

    mode = Unicode().tag(config = True) # , 'output', 'all'
    patterns = List(Unicode(), default_value=[]).tag(config=True)
    remove_metadata_fields = Set(
        {'collapsed', 'scrolled'}
    ).tag(config=True)

    def check_conditions(self, cell):
        """
        Checks that a cell matches the pattern.
        Returns: Boolean.
        True means cell should *not* be removed.
        """

        # Compile all the patterns into one: each pattern is first wrapped
        # by a non-capturing group to ensure the correct order of precedence
        # and the patterns are joined with a logical or
        pattern = re.compile('|'.join('(?:%s)' % pattern
                             for pattern in self.patterns))

        # Filter out cells that meet the pattern and have no outputs
        return pattern.match(cell.source)

    def preprocess_cell(self, cell, resources, cell_index):
        """
        Preprocessing to apply to each cell.
        """
        # Skip preprocessing if the list of patterns is empty
        if not self.patterns:
            return cell, resources

        if self.mode == 'source':
            cell, resources = self.hide_source(cell, resources)
        elif self.mode == 'output':
            cell, resources = self.hide_output(cell, resources)
        elif self.mode == 'cell' or self.mode == 'all':
            cell, resources = self.hide_cell(cell, resources)

        return cell, resources

    def hide_source(self, cell, resources):

        if self.check_conditions(cell):
            cell.metadata.tags = ['hide-source']

        return cell, resources

    def hide_output(self, cell, resources):

        if cell.cell_type == 'code' and self.check_conditions(cell):
            cell.metadata.tags = ['hide-output']

        return cell, resources

    def hide_cell(self, cell, resources):

        if self.check_conditions(cell):
            cell.metadata.tags = ['hide-cell']

        return cell, resources


# Cell
import os
def check_gh_auth():
    if not os.getenv('GITHUB_TOKEN'):
        raise Exception('Please declare your GITHUB_TOKEN as an environment variable, \
        read more here: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token')
    else:
        return True

# Cell
from requests import post
import json

def upload_gist(description, gistcontent, gistname = None, public = False):
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
                    'public': False
                }),
                headers = {
                    'Authorization': f"token {os.getenv('GITHUB_TOKEN')}",
                    "Accept": "application/vnd.github.v3+json"
                }
        ).json() # to return dict response
    return post_req['id'], post_req['html_url']

# Cell
class GisterPreprocessor(Preprocessor):
    """
    Preprocessor that detects the presence of the #gist tag in a Jupyter Notebook cell,
    uploads the code in that cell as a GitHub gist for the authenticated user and replaces the original cell
    for a link to the gist in the resulting markdown file
    """

    patterns = List(Unicode(), default_value=[]).tag(config=True)

    def check_conditions(self, cell):
        """
        Checks that a cell matches the pattern.
        Returns: Boolean.
        True means cell should *not* be removed.
        """

        # Compile all the patterns into one: each pattern is first wrapped
        # by a non-capturing group to ensure the correct order of precedence
        # and the patterns are joined with a logical or
        pattern = re.compile('|'.join('(?:%s)' % pattern
                             for pattern in self.patterns))

        # Filter out cells that meet the pattern and have no outputs
        return pattern.match(cell.source.split('\n')[0]) # only matches in first line of cell

    def get_params(self,cell, **kwargs):
        keywords = ['description', 'gistname', 'public']
        params_string = re.search(r"#\s*gist\s*(.*)", cell.source.split('\n')[0])
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
            params_dict[param[0]] = param[1].strip()

        return params_dict

    def preprocess_cell(self, cell, resources, cell_index):
        """
        Preprocessing to apply to each cell.
        """
        # Skip preprocessing if the list of patterns is empty
        if not self.patterns:
            return cell, resources

        # gist handling
        if self.check_conditions(cell):
            params = self.get_params(cell)
            gist_id, gist_url = upload_gist(gistcontent = '\n'.join(cell.source.split('\n')[1:]), **params)
            cell.source = f"[{gist_url}]({gist_url})"
            cell.cell_type = 'markdown'

        return cell, resources


# Cell
from .API import post_image
from binascii import a2b_base64

class ImagePreprocessor(Preprocessor):
    """
    Preprocessor that detects the presence of the image in a Jupyter Notebook cell's output,
    uploads the image to Medium
    """

    def preprocess_cell(self, cell, resources, cell_index):
        """
        Preprocessing to apply to each cell.
        Images can either be in a cell's output as a result of a plot being generated in the code (Scenario 1)
        Or they can be passed from a local file or the internet in a Markdown cell's source (Scenario 2)
        """
        cell, resources = self.upload_image_from_cell_output(cell, resources)
        cell, resources = self.upload_local_image_from_md(cell, resources)
        return cell, resources

    def upload_local_image_from_md(self, cell, resources):
        # Scenario 2
        # extract name and path of notebook being processed
        name = resources['metadata']['name']
        path = resources['metadata']['path']

        # regex matches the way of insert images in Markdown (e.g `![](somestring)`)
        if cell.cell_type == 'markdown' and re.match('!\[\]\(.*\)', cell.source):
            # figure out if path is local or online, if local upload
            # we use a capture group in the regex to directly extract the content
            # the image tag
            imgs = re.findall('!\[\]\((.*)\)', cell.source)
            for img in imgs:
                img_path = os.path.join(path, img)
                if os.path.isfile(img_path): # local file
                    upload = post_image(filename = img_path).json()
                    url = upload['data']['url']
                    cell.source = re.sub(pattern = img,
                                         repl = url,
                                         string = cell.source)
        return cell, resources

    def upload_image_from_cell_output(self, cell, resources):
        # Scenario 1
        if 'outputs' in cell.keys():
            # Iterate thorugh each output of the cell, if at least 1 image is found
            # clear all other content; for each img upload and replace with url
            # change cell to markdown (output removed in this operation)
            img_counter = 0
            for output in cell.outputs:
                # matplotlib images seem to be already in an ASCII PNG format
                # hence we are going with that
                if 'image/png' in output.data.keys():
                    img_counter += 1
                    img_bin = a2b_base64(output.data['image/png'])
                    img = post_image(img = img_bin).json()
                    url = img['data']['url']
                    cell.source = f"![]({url})\n" if img_counter == 1 else '\n'.join([cell.source, f"![]({url})\n"])

            if img_counter > 0: cell.cell_type = 'markdown'


        return cell, resources
