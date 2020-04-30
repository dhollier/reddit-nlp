import praw
import configparser
import pandas as pd
import pprint

#set options
pd.set_option('display.max_columns', None)

#read config
config = configparser.ConfigParser()
config.read('../config.ini')


reddit = praw.Reddit(client_id=config['default']['client_id'],
client_secret=config['default']['client_secret'],
password = config['default']['password'],
user_agent=config['default']['user_agent'],
username = config['default']['username'])

print(reddit.user.me())


#functions
def get_posts(subname,sort,limit_val=10, time_filter="all"):
    
    if sort == 'top':
        print(f'~Getting posts for {subname} sorted by {sort}, for {time_filter} with limit {limit_val}')
    else:
        print(f'~Getting posts for {subname} sorted by {sort} with limit {limit_val}')




    posts = []

    if sort == 'controversial':
        ml_subreddit = reddit.subreddit(subname).controversial(limit=limit_val)
    if sort == 'gilded':
        ml_subreddit = reddit.subreddit(subname).gilded(limit=limit_val)
    if sort == 'hot':
        ml_subreddit = reddit.subreddit(subname).hot(limit=limit_val)
    if sort == 'new':
        ml_subreddit = reddit.subreddit(subname).new(limit=limit_val)
    if sort == 'rising':
        ml_subreddit = reddit.subreddit(subname).rising(limit=limit_val)
    if sort == 'top':
        ml_subreddit = reddit.subreddit(subname).top(limit=limit_val, time_filter=time_filter)
    




    for post in ml_subreddit:
        posts.append([post.id, 
        post.title,
        post.created_utc,
        post.score, 
        post.subreddit, 
        post.url, 
        post.num_comments, 
        post.selftext,
        post.stickied,
        post.spoiler,
        post.subreddit_subscribers,
        post.subreddit_type,
        post.subreddit_id,
        post.subreddit,
        post.total_awards_received,
        post.ups,
        post.downs,
        post.upvote_ratio,
        post.view_count,
        post.quarantine,
        post.removal_reason,
        post.removed_by_category,
        post.report_reasons,
        post.pinned,
        post.permalink,
        post.over_18,
        post.num_reports,
        post.num_duplicates,
        post.num_crossposts,
        post.num_comments,
        post.no_follow,
        post.media,
        post.media_embed,
        post.media_only,
        post.is_video,
        post.is_original_content,
        post.gilded,
        post.edited,
        post.category,
        post.banned_at_utc,
        post.archived])

        postsDF = pd.DataFrame(posts,columns=['id', 
        'title',
        'created_utc',
        'score', 
        'subreddit', 
        'url', 
        'num_comments', 
        'selftext',
        'stickied',
        'spoiler',
        'subreddit_subscribers',
        'subreddit_type',
        'subreddit_id',
        'subreddit',
        'total_awards_received',
        'ups',
        'downs',
        'upvote_ratio',
        'view_count',
        'quarantine',
        'removal_reason',
        'removed_by_category',
        'report_reasons',
        'pinned',
        'permalink',
        'over_18',
        'num_reports',
        'num_duplicates',
        'num_crossposts',
        'num_comments',
        'no_follow',
        'media',
        'media_embed',
        'media_only',
        'is_video',
        'is_original_content',
        'gilded',
        'edited',
        'category',
        'banned_at_utc',
        'archived'])




    #convert dates to date time
    postsDF['created_utc'] = pd.to_datetime(postsDF['created_utc'] , format=None,unit='s',origin='unix')
    postsDF['banned_at_utc'] = pd.to_datetime(postsDF['banned_at_utc'] , format=None,unit='s',origin='unix')


    print(f'~Done!!! {postsDF.shape[0]} posts found in {subname}')

    return postsDF


def get_comments(permalink):
    url = 'https://www.reddit.com' + permalink

    print(f'~Getting comments for: {url}')
    c_list = []
    post = reddit.submission(url = url)
    post.comments.replace_more(limit=0)

    for comment in post.comments.list():
        this_list =  list([comment.author, 
        comment.body,
        comment.created_utc,
        comment.depth,
        comment.downs,
        comment.edited,
        comment.gilded,
        comment.is_submitter,
        comment.likes,
        comment.link_id,
        comment.parent_id,
        comment.id,
        comment.locked,
        comment.controversiality,
        comment.mod_note,
        comment.mod_reason_by,
        comment.mod_reason_title,
        comment.mod_reports,
        comment.no_follow,
        comment.permalink,
        comment.removal_reason,
        comment.report_reasons,
        comment.score,
        comment.stickied,
        comment.total_awards_received, 
        comment.ups,
        comment.subreddit,
        comment.subreddit_id,
        comment._submission])

        c_list.append(this_list)


    commentDF = pd.DataFrame(c_list,columns=['author', 
    'body', 
    'created_utc',
    'depth',
    'downs',
    'edited',
    'gilded',
    'is_submitter',
    'likes',
    'link_id',
    'parent_id',
    'id',
    'locked',
    'controversiality',
    'mod_note',
    'mod_reason_by',
    'mod_reason_title',
    'mod_reports',
    'no_follow',
    'permalink',
    'removal_reason',
    'report_reasoned',
    'score',
    'stickied',
    'total_awards_received',
    'ups',
    'subreddit',
    'subreddit_id',
    'submission_id'])
    #converts datetime

    commentDF['created_utc'] = pd.to_datetime(commentDF['created_utc'] , format=None,unit='s',origin='unix')
    
    print(f'~Done!!! {commentDF.shape[0]} comments found')
    
    return commentDF