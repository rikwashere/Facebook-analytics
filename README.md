# Facebook-analytics
Crawling facebook posts

For large news organization, posting articles on Facebook is delegated to individuals, for instances social media editors or website managers. But the writers of these articles, arguably have more feeling for their article and are more inclined/better equiped to write a stimulating Facebook post.

However: this does not happen and that makes perfect sense, for two reasons:

1.) Facebook's data is is hard to get to. The search function of their insight platform is rubbish. 
2.) Facebook's data is hard to interpret without context.

This script seeks to remediate these two issues:

The script crawls a supplied Facebook page (need page access token) untill the beginning of time. Storing on first pass key Facebook metrics to an SQL database. On the second pass these posts get hydrated: Facebook Post Insight API is called to reveal the amount of impressions, consumptions, click to the site and the amount of shares. 

In time, a web-interface will be developed (Flask, probably) that will let users input a link to their article and fetch the results. This will create more transparancy about the performance of Facebook posts. Finding the Facebook post written to promote your article - and providing feedback to its author - will be as easy as plugging the URL to your article into this web interface.

The database will also - when entirely populated - provide for some in-depth marco analysis about the best perfomance of Facebook-post. Including, but not limited to: best time to post, the best post authors and what kind of post perform the best. 
Other research questions include: does the penalty for posting the same link twice diminish and - by comparing with the time a post was created - say something about the effect of urgency on a Facebook post.
