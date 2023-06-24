import json
import uuid
import requests
from ast import literal_eval
from datetime import datetime, timedelta
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from webapp.models import HackerNewsPost

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

def make_request():
    print('initial request started', datetime.now())
    # Make the API call and store response
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    response = requests.get(url)

    # Process Information 
    submission_ids = response.json()
    commits = []
    for i in range(100):
        # make a separate api call for each submission
        url = f"https://hacker-news.firebaseio.com/v0/item/{submission_ids[i]}.json"
        response = requests.get(url)
        response_dict = json.loads(response.content)
        if not response_dict:
            continue
        data_to_save = {
            "post_id": response_dict.get('id'),
            "by": response_dict.get('by'),
            "kids": response_dict.get('kids'),
            "score": response_dict.get('score'),
            "descendants" : response_dict.get('descendants'),
            "time": response_dict.get('time'),
            "title": response_dict.get('title'),
            "text" : response_dict.get('text'),
            "type": response_dict.get('type'),
            "url": response_dict.get('url'),
            "source": 'Hacker API',
        }
        
        post_id = data_to_save.pop('post_id')
        post, created = HackerNewsPost.objects.get_or_create(post_id=post_id, defaults=data_to_save)
        
        # Check if the post was created or already exists in the database
        if not created:
            # If the post already exists, update its attributes with the values from data_to_save
            for key, value in data_to_save.items():
                setattr(post, key, value)
            # Add the modified post to the commits list for bulk update
            commits.append(post)

    # Update the modified fields of existing posts in bulk
    HackerNewsPost.objects.bulk_update(commits, ['by', 'kids', 'score', 'time', 'title', 'text', 'type', 'url', 'source'])
    print('initial request finished', datetime.now())


def get_children():
    print('get children started', datetime.now())

    # Retrieve all posts with Hacker API as their source
    posts = HackerNewsPost.objects.filter(source='Hacker API').all()
    posts = posts.exclude(parent__isnull=False)

    # Get a list of existing post IDs from the database
    existing_post_ids = list(HackerNewsPost.objects.values_list('post_id', flat=True))
    existing_post_ids = list(map(int, existing_post_ids))
    commits = []
    for post in posts:
        if post.kids:
            print(post.id)

            # Extract the kids list from the post and remove already existing post IDs
            kids_list = literal_eval(post.kids)
            final_list = list(set(kids_list) - set(existing_post_ids))
            for kid in final_list:
                print(f'getting comments of post_id {post.id}')

                # Retrieve the details of the kid from the Hacker API
                url = f"https://hacker-news.firebaseio.com/v0/item/{kid}.json"
                response = requests.get(url)
                response_dict = json.loads(response.content)
                if not response_dict:
                    print(f'No response of id {kid}')
                    continue
                # Extract the necessary data to save for the comment
                data_to_save = {
                    "post_id" : response_dict.get('id'),
                    "by" : response_dict.get('by'),
                    "text" : response_dict.get('text'),
                    "type" : response_dict.get('type'),
                    "time" : response_dict.get('time'),
                    "parent" : response_dict.get('parent'),
                    "source": 'Hacker API',
                }
                post_id = data_to_save.pop('post_id')

                # Check if the kid comment already exists in the database, otherwise create a new one
                comment,created = HackerNewsPost.objects.get_or_create(post_id=post_id, defaults=data_to_save)
                if not created:
                    # If the kid comment already exists, update its attributes with the values from data_to_save
                    for key, value in data_to_save.items():
                        setattr(comment, key, value)
                    commits.append(comment)

    # Bulk update the modified kid comments in the database
    HackerNewsPost.objects.bulk_update(commits, ['by', 'kids', 'time', 'text', 'type', 'source'])
    print('get children finished', datetime.now())


def schedule_job():
    time_now = datetime.now()
    # Schedule the job to make the initial request(get latest 100 published news) every 5 minutes
    scheduler.add_job(make_request, 'interval', minutes=5, id=str(uuid.uuid4()), next_run_time=time_now + timedelta(seconds=5))

    # Schedule the job to get children (comments) every 33 minutes
    scheduler.add_job(get_children, 'interval', minutes=33, id=str(uuid.uuid4()), next_run_time=time_now + timedelta(minutes=2))

    # Start the scheduler
    scheduler.start()

