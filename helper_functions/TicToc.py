import time

def TicTocGenerator():
    """Generator that returns time differences
    Returns
    -------
    time_difference : float
        the time difference
    """
    initial_time = 0
    final_time = time.time()
    while True:
        initial_time = final_time
        final_time = time.time()
        time_difference = final_time-initial_time
        yield time_difference

# Create an instance of the TicTocGen generator
TicToc = TicTocGenerator()

# This will be the main function through which we define both tic() and toc()
def toc(tempBool=True):
    """returns elapsed time as a string"""
    tempTimeInterval = next(TicToc)
    if tempBool:
        t = "{:f}".format(tempTimeInterval)
        return t

def tic():
    """Records a time in TicToc, marks the beginning of a time interval"""
    toc(False)