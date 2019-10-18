# reddit-toxicity-sampler
A simple integration of the praw reddit API wrapper that samples the hot posts of a sub and finds the worst comments.


# requirements:

1. An internet connection
2. Praw python library (pip install praw)
3. A twitter client id and client secret

### some notes
* Depending on the sub, it will take between 20mins to 2.5hrs for 1000 posts.
* Subs that i've tested that have extreme running times are:
...- r/news
...- r/gaming
...- r/4chan (Not particularly large but high toxicity)
