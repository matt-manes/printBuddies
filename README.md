A few utilities to do terminal printing tricks. <br>
Contains one class and three functions: ProgBar, printInPlace, ticker, and clear.<br>
<br>
ProgBar is a self-incrementing, dynamically sized progress bar.<br>
The progress counter and completion values can be manually overriden if desired.<br>
The width of the progress bar is set according to a ratio of the terminal width
so it will be resized automatically if the terminal width is changed.<br>
The display function has a 'returnObject' parameter, allowing ProgBar to be used in comprehensions.<br>
Basic usage:<br>
<pre>
total = 100
progBar = ProgBar(total=100-1)
for _ in range(total):
    progBar.display()
progBar.reset()
myList = [progBar.display(returnObject=i) for i in range(total)]
</pre>
<br>