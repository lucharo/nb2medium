# nb2medium
> Python package and Jupyter extension that enables submitting Medium drafts elegantly from a Jupyter Notebook


nb2medium represents a simple yet sufficient framework to upload Jupyter notebook to Medium. Its main strenghts are that it makes use of great existing tools such as `nbconvert` or the `requests` package for its main functionality. Moreover the package is build using `nbdev` from Jeremy Howard and the fastai team, which is claimed to accelerate development time.

## Install

`pip install nb2medium`

## Setup

You will need a Medium Integration token to be able to upload your articles to Medium. If you wish to upload some code blocks as gists, you will need a GitHub token too.
Both token should be available as environment variables, hence we recommend you add these 2 lines to your shell configuration file (`~/.bashrc` or `~/.zshrc` are the most common ones):
```bash
export MEDIUM_TOKEN=<your-medium-token>
export GITHUB_TOKEN=<your-github-token>
```

## How to use

nb2medium uploads Jupyter notebooks as they are, the notebooks do not get executed before being rendered.

```
from nb2medium.upload import nb2medium

nb2medium(title = 'My First Article', notebook = '../samples/test-notebook.ipynb');
```

    converter:DEBUG - GITHUB_TOKEN environment variable found.
    converter:INFO - Detected 4 plots and 2 local images in notebook.
    converter:INFO - Detected 4 plots and 2 local images in notebook.
    converter:INFO - Markdown document written to ../samples/test-notebook.md
    converter:INFO - Markdown document written to ../samples/test-notebook.md


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

If the image is already online, nothing changes to it,

#### Code cells as GitHub gists

By default a code cell is rendered without syntax highlighting or anything fancy like:
```
import pandas as pd
pd.DataFrame({'a': [1,2,3], 'b': [2,4,6]})
```
Though if a GitHub token is available and the user includes the following header in a cell:
```python
# gist gistname: pandas.py
import pandas as pd
pd.DataFrame({'a': [1,2,3], 'b': [2,4,6]})
```
The code block will be uploaded to the user's GitHub as a private gist (by default - can be changed to be made public) and the respective code cell will be replaced by the gist URL. The user can also use the `description:` and the `public:` flags in the `#gist` header, where `public:` maybe either True or False and description can just be a string (no single or double quotes required - just avoid using the keywords *gistname, public or description*)

#### Hiding cells

It is often convenient to hide either a cell's source (i.e. the code), a cell's output (the result of evaluating the code) or the whole cell altogether. To achieve this the user can place the following header at the start of the relevant cells.
* To hide a cell's source:
```python
# hide-source
print("This code won't be shown, but it's output will")
```
* To hide a cell's output:
```python
# hide-output
print("This code will be shown, but it's output won't")
```
* To hide a cell completely (source and output):
```python
# hide-cell
print("This cell won't make it to the final document")
```

#### Tables

Not supported yet
