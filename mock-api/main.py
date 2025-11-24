from fastapi import FastAPI, APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import fastapi_swagger_dark as fsd
import json


with open("shay_tweets2.json", 'r') as file:
    data = json.load(file)

#print(data)
print(len(data['results']))

api = FastAPI(title="Mock Twitter API", docs_url=None)
router = APIRouter()

fsd.install(router)
api.include_router(router)


class UserProfile(BaseModel):
    username: str
    name: str
    followers: int


class Tweet(BaseModel):
    id: str
    text: str
    author: str
    created_at: datetime


def get_user(username: str):
    user = mock_users.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@api.get("/users/{username}", response_model=UserProfile)
def get_user_profile(username: str):
    return get_user(username)


# change mock_tweets to read from json
@api.get("/users/{username}/tweets", response_model=List[Tweet])
def get_user_tweets(username: str):
    get_user(username) # check if user exist
    user_tweets = [tweet for tweet in data if tweet['author'] == username]
    return sorted(user_tweets, key=lambda x: x["created_at"], reverse=True)


# also change mock_tweets
@api.get("/tweets/{tweet_id}", response_model=Tweet)
def get_tweet(tweet_id: str):
    tweet = next((t for t in data if t["id"] == tweet_id), None)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    return tweet


@api.get("/tweets", response_model=List[Tweet])
def get_all_tweets():
    return sorted(mock_tweets, key=lambda x: x["created_at"], reverse=True)
