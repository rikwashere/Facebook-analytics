# Facebook-analytics
Crawling facebook posts

For large media organization posting articles on Facebook is delegated to individuals, like social media editors or website managers. But I think that people who write the articles should write the Facebook posts: they are more invested in the article and have more knowledge about the article. This will lead to beter performing Facebook articles.

However: this does not happen - and that makes perfect sense - for two reasons:

1.) Facebook's data is is hard to get to. The search function of their insight platform is rubbish. 
2.) Facebook's data is hard to interpret without context.

A dedicated (social media) professional will therefore always outperform the writers of the articles. They have more knowledge about what works and what does not. For a non-professional this feedback loop is closed. 

This repository seeks to open this feedback loop. 

The script crawls a supplied Facebook page (need page access token) untill the beginning of time. Storing on first pass key Facebook metrics to an SQL database. On the second pass these posts get hydrated: Facebook Post Insight API is called to reveal the amount of impressions, consumptions, clicks to the site and the amount of shares. 

In time, a web-interface will be developed (Flask, probably) that will let users input a link to their article and fetch the results. This will create more transparancy about the performance of Facebook posts. Finding the Facebook post written to promote your article - and providing feedback to its author - will be as easy as plugging the URL to your article into this web interface. Contextual data will be provided as well: performance of posts in the same time slot will be supplied.

The database will also - when entirely populated - provide for some in-depth marco analysis about the best perfomance of Facebook-post. Including, but not limited to: best time to post, the best post authors and what kind of post perform the best. 
Other research questions include: does the penalty for posting the same link twice diminish and - by comparing with the time a post was created - say something about the effect of urgency on a Facebook post.
