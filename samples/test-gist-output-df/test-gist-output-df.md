[https://gist.github.com/95156fe07a1114249737b324c16909aa](https://gist.github.com/95156fe07a1114249737b324c16909aa)

[https://gist.github.com/aeeab4ed96c4507de4ec2317bd8159b0](https://gist.github.com/aeeab4ed96c4507de4ec2317bd8159b0)



```python
%%js 
const pythonPromise = function(python) {
        return new Promise((resolve, reject) => {
            var callbacks = {
                iopub: {
                    output: (data) => {resolve(data.content.text)}
                    }
                };
            Jupyter.notebook.kernel.execute(python, callbacks);  
       });
    }

let a = pythonPromise(`
from nb2medium.upload import nb2medium
nb2medium(title = 'hi',
          notebook = './test-gist-output-df.ipynb')`)
console.log(a)
```


    <IPython.core.display.Javascript object>



```python
from nb2medium.upload import nb2medium
from io import StringIO
from contextlib import redirect_stdout
f = StringIO()
with redirect_stdout(f):
    n2medium_request = nb2medium(
        title = 'hi',
        notebook = './test-gist-output-df.ipynb',
        log_level = 'debug',
        log_to_stdout = True)
print(f.getvalue())
```

    uploader:DEBUG - Detected MEDIUM_TOKEN
    converter:DEBUG - Detected gist tag in cell 0  with arguments: description, gistname, upload; uploading...
    converter:INFO - Gist pandas.py from cell 0 succesfully uploaded!
    converter:DEBUG - Found table in cell 0, uploading...
    converter:INFO - Gist pandas.py.csv from cell 0 succesfully uploaded!
    converter:INFO - Detected 0 plots and 0 local images in notebook.
    converter:INFO - Markdown document written to ./test-gist-output-df/test-gist-output-df.md
    uploader:INFO - Draft of 'hi' from test-gist-output-df.ipynb notebook uploaded to Medium: https://medium.com/@lucha6/fd90a302ae0a
    



```python

```
