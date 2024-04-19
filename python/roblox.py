
from __future__ import annotations
from typing import Union
from pydantic import BaseModel, Field
from dateutil import parser

import json
import time
import aiohttp
import asyncio

class RobloxBadge(BaseModel):
	id : int = Field(-1)
	name : str = Field('unknown')

class UserProfile(BaseModel):
	user_id : int = Field(-1)
	username : str = Field('unknown')
	display_name : str = Field('unknown')
	join_date : int = Field(-1)
	account_age : int = Field(-1)
	total_visits : int = Field(-1)
	followers_count : int = Field(-1)
	verified : bool = Field(False)
	friends : list[int] = Field(default_factory=list)
	roblox_badges : list[RobloxBadge] = Field(default_factory=list)
	update_timestamp : int = Field(-1)

async def get_time() -> int:
	return int(round(time.time()))

UPDATE_COOLDOWN : int = 24 * 60 * 60
DEFAULT_HEADERS : dict = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' }

user_profile_cache : dict[int, UserProfile] = dict()
processing : list[int] = list()

async def fetch_text(client : aiohttp.ClientSession, url : str) -> Union[str, None]:
	print(url)
	async with client.get(url) as resp:
		resp : aiohttp.ClientResponse = resp
		if resp.status == 200:
			return await resp.text()
		# print(resp.status, resp.reason)
		return None

async def fetch_json(client : aiohttp.ClientSession, url : str) -> Union[str, None]:
	# print(url)
	async with client.get(url) as resp:
		resp : aiohttp.ClientResponse = resp
		if resp.status == 200:
			return await resp.json()
		# print(resp.status, resp.reason)
		return None

async def post_json(client : aiohttp.ClientSession, url : str, body : dict | list) -> Union[str, None]:
	# print(url)
	body : str = json.dumps(body, separators=(',', ':'))
	async with client.post(url, data=body) as resp:
		resp : aiohttp.ClientResponse = resp
		if resp.status == 200:
			return await resp.json()
		# print(resp.status, resp.reason)
		return None

async def process_user_id( user_id : int ) -> Union[UserProfile, None]:
	now : int = await get_time()

	profile : UserProfile = user_profile_cache.get(user_id)
	if profile is not None:
		expiry : int = profile.update_timestamp + UPDATE_COOLDOWN
		if now < expiry:
			return profile
		user_profile_cache.pop(user_id)
		del profile

	if user_id not in processing:
		processing.append(user_id)

	profile : UserProfile = UserProfile(friends=[],roblox_badges=[])

	async with aiohttp.ClientSession(headers=DEFAULT_HEADERS) as client:
		# get their profile info
		profile_data_url : str = f'https://users.roblox.com/v1/users/{user_id}'
		profile_data = await fetch_json(client, profile_data_url)

		profile.user_id = profile_data['id']
		profile.username = profile_data['name']
		profile.display_name = profile_data['displayName']
		profile.join_date = parser.isoparse(profile_data['created']).timestamp()
		profile.account_age = now - profile.join_date
		profile.verified = profile_data['hasVerifiedBadge']

		# get their follower count
		profile_followers_url : str = f'https://friends.roblox.com/v1/users/{user_id}/followers/count'
		followers_data = await fetch_json(client, profile_followers_url)
		profile.followers_count = followers_data['count']

		# get their roblox badges
		profile_badges_url : str = f'https://accountinformation.roblox.com/v1/users/{user_id}/roblox-badges'
		badges_data = await fetch_json(client, profile_badges_url)
		profile.roblox_badges = [ RobloxBadge(id=item['id'], name=item['name']) for item in badges_data ]

		# TODO:
		# total_visits : int
		# groups : list[(int, int)] = list() # (group_id, rank_id)
		# friends : list[int] = list()

	profile.update_timestamp = now
	user_profile_cache[user_id] = profile
	return profile

async def is_processing_user_id( user_id : int ) -> bool:
	return user_id in processing

async def search_user_id( user_id : int ) -> Union[UserProfile, None]:
	processing : bool = await is_processing_user_id( user_id )
	while processing is True:
		asyncio.sleep(0.2)
		processing : bool = await is_processing_user_id( user_id )
	return await process_user_id( user_id )

username_to_userid : dict[str, int] = dict()
async def search_username( username : str ) -> Union[UserProfile, None]:
	if username not in username_to_userid.keys():
		async with aiohttp.ClientSession(headers=DEFAULT_HEADERS) as client:
			url : str = 'https://users.roblox.com/v1/usernames/users'
			js : dict = {"usernames":[username],"excludeBannedUsers":False}
			data = await post_json(client, url, js)
		try:
			user_id : int = data['data'][0]['id']
			username_to_userid[username] = user_id
		except:
			username_to_userid[username] = None
	user_id : int = username_to_userid.get(username)
	if user_id is None:
		return None
	return await search_user_id( user_id )
