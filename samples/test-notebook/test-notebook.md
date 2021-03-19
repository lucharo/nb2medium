# Complete Test of `nb2medium`

## My empty and sad subtitle

We will use this notebook as a complete example of the `nb2medium` capabilities

### "Normal" cells

Assign a value


```
a = 1
```

Have a value returned (JNB's default), note that printed and returned values are different


```
a
```




    1



Printing a value


```
print(a)
```

    1


Multiple outputs


```
print(a)
a
```

    1





    1



### Plots & Images


```
import matplotlib.pyplot as plt
import numpy as np
```

#### One `matplotlib` plot


```
x = np.arange(0, 10, 0.1)
y = np.sin(x)
plt.plot(x,y)
plt.grid()
```

![](https://cdn-images-1.medium.com/proxy/1*60J3d7TXOUcpu2ND8sun0Q.png)


Notice that a a list containing a `matplotlib.lines.Line2D` gets returned from `plt.plot(x,y)`, we can cancel that output being returned by adding a semicolon `;`


```
x = np.arange(0, 10, 0.1)
y = np.sin(x)
plt.plot(np.exp(x),y, c = 'red');
```

![](https://cdn-images-1.medium.com/proxy/1*ky0JIY4Tf-2HfBXtNZhFog.png)


## Several images in a single cell's output


```
plt.plot(x,y, c = 'orange')
fig = plt.figure()
plt.plot(x**2,y)
plt.grid();
```

![](https://cdn-images-1.medium.com/proxy/1*XCrZjB5ZPHHlPuV1hmhTiA.png)

![](https://cdn-images-1.medium.com/proxy/1*k2qlCbK6GPq596AbnJ2xjw.png)


### Offline/local images

![](https://cdn-images-1.medium.com/proxy/1*xYdnXpwz3wapR0XTS4aP6Q.png)

### Online image

![](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%3Fid%3DOIP.TYe3gPutefAvqQe69fSXYAAAAA%26pid%3DApi&f=1)

### Online and offline image in same cell

![](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%3Fid%3DOIP.TYe3gPutefAvqQe69fSXYAAAAA%26pid%3DApi&f=1)
![](https://cdn-images-1.medium.com/proxy/1*xYdnXpwz3wapR0XTS4aP6Q.png)

### Gists code cells

Simple variable definition gist

[https://gist.github.com/99d61f4f0e05a263601e5fd02bf01b19](https://gist.github.com/99d61f4f0e05a263601e5fd02bf01b19)


[https://gist.github.com/6a084db8b65010785ce1a983098bb114](https://gist.github.com/6a084db8b65010785ce1a983098bb114)


### Pandas dataframes as CSV gists

When we specify the flag `upload: output`, `nb2medium` will upload the output of the cell in a suitable format

[https://gist.github.com/1c8bccde3942d375f94e3f7c8a3eee2d](https://gist.github.com/1c8bccde3942d375f94e3f7c8a3eee2d)


### Uploading both code and dataframe as gists

We can achieve this by specifying the flag `upload: both`

[https://gist.github.com/6d3b7a64daec9cfbea3c4e48eb5a9484](https://gist.github.com/6d3b7a64daec9cfbea3c4e48eb5a9484)

[https://gist.github.com/841e0bd3373b957ce27c69449991b4ab](https://gist.github.com/841e0bd3373b957ce27c69449991b4ab)


### Hiding cells

    This code won't be shown, but it's output will



```
print("This code will be shown, but it's output won't")
```
