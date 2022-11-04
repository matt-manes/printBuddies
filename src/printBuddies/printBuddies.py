from sys import stdout
from os import get_terminal_size
from typing import Any
from time import sleep

def clear():
    """ Erase the current line from the terminal. """
    stdout.write(' '*(get_terminal_size().columns-1) + '\r')

def printInPlace(string:str, animate:bool=False,
                 animateRefresh:float=0.01):
    """ Calls to printInPlace will overwrite 
    the previous line of text in the terminal
    with the 'string' param.\n
    :param animate: Will cause the string
    to be printed to the terminal 
    one character at a time.\n
    :param animateRefresh: Number of seconds 
    between the addition of characters
    when 'animate' is True."""
    clear()
    if animate:
        for i in range(len(string)):
            width = get_terminal_size().columns
            string = string[:width-2]
            stdout.write(f'{string[:i+1]} \r')
            stdout.flush()
            sleep(animateRefresh)
    else:
        width = get_terminal_size().columns
        string = string[:width-2]
        stdout.write(f'{string} \r')
        stdout.flush()

def ticker(info:str|list):
    """ Prints info to terminal with
    top and bottom padding so that repeated 
    calls print info without showing previous
    outputs from ticker calls.\n
    Similar visually to printInPlace,
    but for multiple lines."""
    if type(info) != list:
        info = str(info).split('\n')
    height = get_terminal_size().lines-len(info)
    padLines = int((height - len(info))/2)
    print('\n'*padLines)
    for line in info:
        print(line)
    print('\n'*padLines)

class ProgBar:
    """ Self incrementing, dynamically sized progress bar.\n
    Call ProgBar.clear() or print() after the last call to 
    ProgBar.display(); otherwise, the next thing that
    tries to write to the terminal will print on the same
    line."""
    def __init__(self, total:float, fillCh:str='_', unfillCh:str='/',
                 widthRatio:float=0.75):
        """ :param total: The number of calls to reach 100% completion.\n
        :param fillCh: The character used to represent the completed part of the bar.\n
        :param unfillCh: The character used to represent the uncompleted part of the bar.\n
        :param widthRatio: The width of the progress bar relative to the width of the terminal window."""
        self.total = total
        self.fillCh = fillCh[0]
        self.unfillCh = unfillCh[0]
        self.widthRatio = widthRatio
        self.reset()
    
    def reset(self):
        self.counter = 0
        self.percent = ''
        self.prefix = ''
        self.suffix = ''
        self.filled = ''
        self.unfilled = ''
        self.bar = ''
    
    def getPercent(self)->str:
        """ Returns the percentage complete to two decimal places
        as a string without the %."""
        percent = str(round(100.0*self.counter/self.total, 2))
        if len(percent.split('.')[1]) == 1:
            percent = percent + '0'
        if len(percent.split('.')[0]) == 1:
            percent = '0' + percent
        return percent
    
    def _prepareBar(self):
        self.terminalWidth = get_terminal_size().columns - 1
        barLength = int(self.terminalWidth * self.widthRatio)
        progress = int(barLength*self.counter / self.total)
        self.filled = self.fillCh * progress
        self.unfilled = self.unfillCh * (barLength-progress)
        self.percent = self.getPercent()
        self.bar = self._getBar()
    
    def _trimBar(self):
        originalRatio = self.widthRatio
        while len(self.bar) > self.terminalWidth:
            self.widthRatio -= 0.01
            self._prepareBar()
        self.widthRatio = originalRatio
    
    def _getBar(self):
        return f'{self.prefix} [{self.filled}{self.unfilled}]-{self.percent}% {self.suffix} '
    
    def display(self, prefix:str='', suffix:str='',
                counterOverride:float=None, 
                totalOverride:float=None,
                returnObject:Any=None)->Any:
        """ Writes the progress bar to the terminal.\n
        :param prefix: String affixed to the front of the progress bar.\n
        :param suffix: String appended to the end of the progress bar.\n
        :param counterOverride: When an externally incremented completion counter is needed.\n
        :param totalOverride: When an externally controlled bar total is needed.\n
        :param returnObject: An object to be returned by display().\n
        Allows display() to be called within a comprehension:\n
        e.g.\n 
        progBar = ProgBar(9)\n
        myList = [progBar.display(returnObject=i) for i in range(10)]"""
        if counterOverride:
            self.counter = counterOverride
        if totalOverride:
            self.total = totalOverride
        #Don't wanna divide by 0 there, pal
        while self.total <= 0:
            self.total += 1
        self.prefix = prefix
        self.suffix = suffix
        self._prepareBar()
        self._trimBar()
        pad = ' ' * (self.terminalWidth-len(self.bar))
        stdout.write(f"{self.bar}{pad}\r")
        stdout.flush()
        self.counter += 1
        return returnObject
