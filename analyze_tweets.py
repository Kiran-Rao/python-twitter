"""
Analyze tweets module
Uses MatPlotLib to plot the number of times a keyword/hashtag appears
as a function of time
"""
import datetime
import matplotlib
import matplotlib.pyplot as plt
from twitter import Twitter

if __name__ == "__main__":
    # HANDLES = raw_input("Please enter a list of twitter handles separated by spaces:").split()
    # KEYWORD = raw_input("Please enter keyword or hashtag: ")
    # COUNT = raw_input("Please enter the number of tweets to search for: ")
    HANDLES = ["realDonaldTrump"]
    KEYWORD = "wall"
    COUNT = 200

    TIME_COUNTED_PAIRS = Twitter.request(HANDLES, KEYWORD, COUNT)

    print TIME_COUNTED_PAIRS

    COUNT = [pair[1] for pair in TIME_COUNTED_PAIRS]
    TIMES = [datetime.datetime.strptime(pair[0], "%a %b %d %H:%M:%S +0000 %Y") for pair in TIME_COUNTED_PAIRS]
    MPL_TIME = matplotlib.dates.date2num(TIMES)

    plt.plot_date(MPL_TIME, COUNT)
    plt.show()
