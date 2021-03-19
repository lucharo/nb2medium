# nb2medium
> Python package and Jupyter extension that enables submitting Medium drafts elegantly from a Jupyter Notebook


[![Testing](https://github.com/lucharo/nb2medium/actions/workflows/main.yml/badge.svg)](https://github.com/lucharo/nb2medium/actions/workflows/main.yml)
[![PyPI version](https://badge.fury.io/py/nb2medium.svg)](https://badge.fury.io/py/nb2medium)
[![Downloads](https://static.pepy.tech/personalized-badge/nb2medium?period=total&units=international_system&left_color=black&right_color=yellowgreen&left_text=Downloads)](https://pepy.tech/project/nb2medium)

**nb2medium main assets are:** 

> * Written using `nbdev` and therefore easy to maintain 
> * Simple pythonic implementation of Medium API
> * Makes use of `nbconvert` and custom preprocessors to turn notebooks to Markdown documents
> * Supports uploading blocks as GitHub gists with simple in-cell tags
> * Supports hiding of cells sources, cells outputs or cells
> * Comes with Jupyter extension and CLI for ease-of-use

nb2medium represents a simple yet sufficient framework to upload Jupyter notebook to Medium. Its main strenghts are that it makes use of great existing tools such as `nbconvert` or the `requests` package for its main functionality. Moreover the package is developed using `nbdev` from Jeremy Howard and the fastai team, which is claimed to accelerate development an debugging time.

![dialog](https://user-images.githubusercontent.com/47890755/110972057-7b5abb00-8353-11eb-8ddb-21e09dd78ccf.png)

## Install

`pip install nb2medium`

Then enable the notebook extension by running:
```bash
jupyter notebook install nb2medium --py
jupyter notebook enable nb2medium --py
```
Add `--user` to these commands if you want to activate the extension only for the current user.\
Add `--sys-prefix` to these commands if you want to activate the extension only in current virtual environment.

## Setup

You will need a Medium Integration token to be able to upload your articles to Medium. If you wish to upload some code blocks as gists, you will need a GitHub token too.
Both token should be available as environment variables, hence we recommend you add these 2 lines to your shell configuration file (`~/.bashrc` or `~/.zshrc` are the most common ones):
```bash
export MEDIUM_TOKEN=<your-medium-token>
export GITHUB_TOKEN=<your-github-token>
```

**Obtain an Medium Integration Token from [your Medium settings page](https://medium.com/me/settings)\
Obtain a GitHub token by following [GitHub's docs](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)**

## How to use

You may choose to use nb2medium as a command line tool, directly from python or using the Jupyter notebook extension button or menu. _Note:_ nb2medium uploads Jupyter notebooks as they are, the notebooks do not get executed before being rendered.

### From the Jupyter notebook

You may choose to use the `nb2medium` under file or the button on the top toolbar

![menu_and_button](https://user-images.githubusercontent.com/47890755/110972060-7c8be800-8353-11eb-92cd-51d1fb746faf.png)

### From the CLI

From the shell (bash, zsh, sh):
```bash
nb2medium "My article" path/to/notebook.ipynb
```
Use `nb2medium --help` to see all the different options

### From python

```
from nb2medium.upload import nb2medium

nb2medium(title = 'My First Article', notebook = '../samples/test-notebook.ipynb');
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
    uploader:INFO - Draft of 'My First Article' from test-notebook.ipynb notebook uploaded to Medium: https://medium.com/@lucha6/946f9176365b


### Images, code cells and tables

#### Images

Images usually come from a local file, online site or are the result of a plot. `nb2medium` can handle these 3 situations. If an image correspond to a local file in markdown cell (e.g. `![](path/to/image.png)`)

The image is uploaded to the Medium end point and the path to the image is swapped for the newly generated image URL.
If the image is the result of a plot, such as:
```python
import numpy as np
import matplotlib.pyplot as plt
x = np.arange(0, 10, 0.1)
y = np.sin(x)
plt.plot(x,y)
```
The result of the image is uploaded to the Medium endpoint (without being written to memory) and the corresponding plot is replaced by the plot's URL.

If the image is already online, nothing changes to it, as Medium can access it directly from the internet when loading the article

#### Code cells as GitHub gists

By default a code cell is rendered without syntax highlighting or anything fancy like:
```
import pandas as pd
pd.DataFrame({'a': [1,2,3], 'b': [2,4,6]})
```
Though if a GitHub token is available and the user includes the following header in a cell:
```python
# %gist gistname: pandas.py
import pandas as pd
pd.DataFrame({'a': [1,2,3], 'b': [2,4,6]})
```
The code block will be uploaded to the user's GitHub as a private gist (by default - can be changed to be made public) and the respective code cell will be replaced by the gist URL. The user can also use the `description:` and the `public:` flags in the `#gist` header.

The `#%gist` takes the following arguments:

* gistname: name of script with file extension (critical for correct syntax highlighting, e.g script.py)
* description: [optional] string (no quotes are necessary) describing the gist
* public: [optional - default False] whether gist should be public or not
* output: [optional - default source] whether cell's source, output or both should be uploaded as gists (e.g. `upload: both`, `upload: source`)

#### Hiding cells

It is often convenient to hide either a cell's source (i.e. the code), a cell's output (the result of evaluating the code) or the whole cell altogether. To achieve this the user can place the following header at the start of the relevant cells.
* To hide a cell's source:
```python
# %hide-source
print("This code won't be shown, but it's output will")
```
* To hide a cell's output:
```python
# %hide-output
print("This code will be shown, but it's output won't")
```
* To hide a cell completely (source and output):
```python
# %hide-cell
print("This cell won't make it to the final document")
```

_Note:_ all tags (`%hide-*` and `%gist`) were not designed with the idea to be combined so such usage has not been tested. In general there should be no need for such behaviour.

#### Tables

Medium does not have good support for HTML nor Markdown tables. My preferred existing option for tables is `gist`. If a cell outputs a pandas dataframe and you choose the `#%gist` option with the value of the `upload:` flag set to `both` or `output`, `nd2medium` will detect your table and upload it as a CSV to your GitHub gist repo.
```python
#% gist gistname: pandas.py upload: both
import pandas as pd
pd.DataFrame({'a': [1,2,3], 'b': [0,0,0], 'c': ['One', 'Two', 'Three']})
```

## Documentation

The docs are available at [https://lucharo.github.io/nb2medium](https://lucharo.github.io/nb2medium) and are rendered automatically from the `nbdev` notebooks so they are always up to date with the package source code

## Contributing

If you find a bug or think of an enhancement feel free to raise issues or submit pull requests. If you want to contribute to open source projects such as this one have a look at the issues with the label/tag `help needed` in particular.
