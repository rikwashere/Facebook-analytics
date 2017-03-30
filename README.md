# Facebook-analytics
Crawling facebook posts

This script seeks to answer a simple question for large organizations: how did my Facebook post do?

The current script crawls the supplied page (need page access token) untill the beginning of time. Storing key values, like impressions, consumptions, shares, the text of the post, the time and the link supplied. 

In time, this data will be stored in a SQL database (using SQLite3, probably) and the code will be modified so that the database will automatically update itself. With this updating database complete, a web-interface will be developed (Flask, probably) that will let users input a link to their article and fetch the results. This will create more transparancy about the performance of Facebook posts. 

The database will also - when entirely populated - provide for some in-depth analyses about the best perfomance of Facebook-post. Including, but not limited to: best time to post, the best post authors and what kind of post perform the best. Other research questions include: does the penalty for posting the same link twice diminish and - by comparing with the time a post was created - say something about the effect of urgency on a Facebook post.,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
