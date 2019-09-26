#!/usr/bin/python3.7

import praw 
import time
import json
from itertools import combinations
class flaggedComment:
	#TODO   add in attribute for badwords found in the comment body
	def __init__(self,prawComment, sev, sub):
		self.prawComment = prawComment
		self.body = self.prawComment.body
		self.sub = sub
		self.sev = sev
		self.permalink = prawComment.permalink
		self.id = self.prawComment.id
	def getId(self):
		return self.prawComment.id
	

reddit =  praw.Reddit(client_id = '', 
		      client_secret = '',
		      user_agent = ':)')
# an algorithm for calculationg toxicity 
# TODO: improve algorithm
def GetSev(rawbadwords, body):
	slurs, swears, figures = rawbadwords['slurs'], rawbadwords['swears'], rawbadwords['political']
	total = 0
	multi = 1
	commentBody = body.split()
	for index, word in enumerate(commentBody):
		if word in swears and index > 0 and index < len(commentBody)-1:
			temp = swears[word]
			if commentBody[index - 1] in slurs and index > 0:
				total += temp * slurs[commentBody[index-1]]
				del commentBody[index:index-1]
			if commentBody[index + 1] in slurs:
				total += temp * slurs[commentBody[index+1]]
				del commentBody[index:index+1]
			elif commentBody[index + 1] in figures:
				multi += figures[word]
			elif commentBody[index - 1] in figures and index > 0:
				multi += figures[word]
			else:
				total += temp
		elif word in slurs and index > 0 and index < len(commentBody):
			temp = slurs[word]
			if commentBody[index - 1] in slurs and index > 0:
				total += temp ** slurs[commentBody[index-1]]
				del commentBody[index:index-1]
			if commentBody[index + 1] in slurs:
				total += temp ** slurs[commentBody[index+1]]
				del commentBody[index:index+1]
			elif commentBody[index + 1] in figures:
				multi += figures[word]
			elif commentBody[index - 1] in figures and index > 0:
				multi += figures[word]
			else:
				total += temp
		if len(commentBody) == 1:
			if word in swears:
				total += swears[word]*1.5
			elif word in slurs:
				total += slurs[word]*1.5
	if len(commentBody) >= 16:
		total = total/len(commentBody)

	return total * multi

# returns a dictionary of flagged comment objects that contain a sev > 1
# USE SPARINGLY as avg runtime is over 20 minutes for 1000 posts. 
def SampleSub(subName='gaming', sampleSize=100):
	if __name__ == '__main__':
		print ("running SearchSub")
	badwords = {}
	try:
		with open("badwords.json") as json_file:
			rawbadwords = json.load(json_file)
		for key, value in rawbadwords['swears'].items():
			badwords[key] = value
		for key, value in rawbadwords['slurs'].items():
			badwords[key] = value
	except:
		print("File read err - exiting")
		exit()
	sub = reddit.subreddit(subName)
	disc_comment = {}
	submissions = sub.hot(limit=sampleSize)
	i2 = 0
	for submission in submissions:
		i2 += 1
		submission.comments.replace_more(limit=None)
		for comment in submission.comments.list():
			disc_comment[comment.id] = comment
			i = len(disc_comment)
			if __name__ == '__main__':
				print(comment.id,i,"|",submission.id,i2,end='\r')
	foundComments = []
	for badword in badwords:
		for key in disc_comment.keys():
			commentBody = disc_comment[key].body.split()
			for commentWord in commentBody:
				if badword.capitalize() in commentWord.capitalize() and key not in foundComments:
					foundComments.append(key)
	flaggedComments = {}
	for commentid in foundComments:
		if commentid not in flaggedComments.keys():
			sev = GetSev(rawbadwords, disc_comment[commentid].body)
			flaggedComments[commentid] = flaggedComment(
													disc_comment[commentid],
													sev,
													subName)

	return flaggedComments
def TopTen(commentDict):
	
	topTen = [value for key, value in commentDict.items()]
	topTen.sort(key=lambda comment: comment.sev, reverse=True)
	out = []
	for index, item in enumerate(topTen):
		if index >= 9:
			break
		else:
			out.append(item)
	topTen.clear()
	return out
	
def ToDict(fcomment):
	#TODO: make this not lazy
	try:
		data = {
			'id': fcomment.id,
			'name': fcomment.prawComment.author.name,
			'sev': fcomment.sev,
			'sub': fcomment.sub,
			'perm': fcomment.prawComment.permalink
			}
	except:
		data = {
			'id': fcomment.id,
			'name': '[Deleted]',
			'sev': fcomment.sev,
			'sub': fcomment.sub,
			'perm': fcomment.prawComment.permalink
			}
	return data
def ToJson(fcommentlist):
	data = {}
	data['fcomments'] = []
	for fcomment in fcommentlist:
		data['fcomments'].append(fcomment)
	with open('fcomments-reddit.json','w') as outfile:
		json.dump(data, outfile, indent=4)

if __name__ == "__main__":	
	targetSub = input("Enter Subreddit Target (default=r/gaming):\nr/")
	targetSample = input("Enter Submission Sample Size (default=1000):\n~")
	if len(targetSample) < 1:
		targetSample = 10
	if len(targetSub) < 1:
		targetSub = 'gaming'

	starttime = time.time()
	flaggedComments = SampleSub(targetSub,int(targetSample))
	print('\ntook {0:.2f}s'.format((time.time()-starttime)/2))

	print('\nsearch complete')
	print('flaggedComments:',len(flaggedComments))
	fcommentlist = []
	for key, fcomment in flaggedComments.items():
		if fcomment.sev > 1:
			fcommentlist.append(ToDict(fcomment))
			print('appending:',key,end='\r')
	ToJson(fcommentlist)

	for index, item in enumerate(TopTen(flaggedComments)):
		print('#'+str(index+1),
		      item.getId(),
		      '| sev:',item.sev,
		      '\n   ⮡ link: https://reddit.com'+item.permalink,
		      end='\n\n')
