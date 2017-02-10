"""
Plotting module
Uses MatPlotLib to plot the number of times a keyword/hashtag appears
"""

import matplotlib.pyplot as plt
from twitter import Twitter

if __name__ == "__main__":
    HANDLES = raw_input("Please enter a list of twitter handles separated by spaces:").split()
    KEYWORD = raw_input("Please enter keyword or hashtag: ")
    COUNT = raw_input("Please enter the number of tweets to search for: ")

    TIME_COUNTED_PAIRS = Twitter.request(HANDLES, KEYWORD, COUNT)
    COUNT = [pair[1] for pair in TIME_COUNTED_PAIRS]

    plt.plot(COUNT)
    plt.show()
