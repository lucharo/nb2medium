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

[https://gist.github.com/2736f5f9894b6d1737f94b1c2d1d7442](https://gist.github.com/2736f5f9894b6d1737f94b1c2d1d7442)


[https://gist.github.com/3162bf6a4c73b4b3595b0dd1e3785028](https://gist.github.com/3162bf6a4c73b4b3595b0dd1e3785028)


### Pandas dataframes as CSV gists

When we specify the flag `upload: output`, `nb2medium` will upload the output of the cell in a suitable format

[https://gist.github.com/f9dec5a39070a40cd58a2e69b8eba29f](https://gist.github.com/f9dec5a39070a40cd58a2e69b8eba29f)


### Uploading both code and dataframe as gists

We can achieve this by specifying the flag `upload: both`

[https://gist.github.com/0e4898cb31f9775a26092aab8fcd5757](https://gist.github.com/0e4898cb31f9775a26092aab8fcd5757)

[https://gist.github.com/e9c87ac5460eb464ad9c28938f48a6a3](https://gist.github.com/e9c87ac5460eb464ad9c28938f48a6a3)


### Hiding cells

    This code won't be shown, but it's output will



```
print("This code will be shown, but it's output won't")
```
