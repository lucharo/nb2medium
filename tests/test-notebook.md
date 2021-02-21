
# My Really Cool Article

## Content

We will use this notebook to test the parsing of notebooks to md of `jupyter nbconvert`. We will see how external images (both online and offline) work as well as images from plots. We will also see how code blocks get rendered and test our parsing options to enable gists to be created automatically when a certain flag is present

### Plot


```python
import matplotlib.pyplot as plt
import numpy as np
```

![](https://cdn-images-1.medium.com/proxy/1*ZnEIxs8iH8hajqTySqeARA.png)


Notice that a a list containing a `matplotlib.lines.Line2D` gets returned, we can cancel that output being returned by adding a semicolon

![](https://cdn-images-1.medium.com/proxy/1*ZnEIxs8iH8hajqTySqeARA.png)


## Several images in a single cell's output

![](https://cdn-images-1.medium.com/proxy/1*ZnEIxs8iH8hajqTySqeARA.png)

![](https://cdn-images-1.medium.com/proxy/1*fIAcA3AMNFGfxs42T2INsA.png)


### Online image

![](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.93Rd3hWSSUDZVPozrX4UcAHaLH%26pid%3DApi&f=1)

I like keeping some code cells as code cells and I like uploading others as gists

[https://gist.github.com/c665d01a9079b73b3c67292591f242d7](https://gist.github.com/c665d01a9079b73b3c67292591f242d7)

## Images from local paths

![](https://cdn-images-1.medium.com/proxy/1*xYdnXpwz3wapR0XTS4aP6Q.png)

## Online and offline images together

![](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%3Fid%3DOIP.TYe3gPutefAvqQe69fSXYAAAAA%26pid%3DApi&f=1)
![](https://cdn-images-1.medium.com/proxy/1*xYdnXpwz3wapR0XTS4aP6Q.png)


```python

```
