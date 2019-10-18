# reddit-toxicity-sampler
A simple integration of the praw reddit API wrapper that samples the hot posts of a sub and finds the worst comments.


<h1>
requirements:
</h1>

1. An internet connection
2. Praw python library (pip install praw)
3. A twitter client id and client secret

<h2> some notes </h2>
*Depending on the sub, it will take between 20mins to 2.5hrs for 1000 posts.
  *Subs that i've tested that have extreme running times are:
    1.r/news
    2.r/gaming
    3.r/4chan (Not particularly large but high toxicity)
