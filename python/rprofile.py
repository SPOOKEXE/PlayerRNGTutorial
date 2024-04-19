
from __future__ import annotations
from typing import Union
from pydantic import BaseModel

import aiohttp
import asyncio

class GroupRole:
	id : int
	name : str
	count : int

class Group(BaseModel):
	group_id : int
	group_name : str
	owner_username : str
	owner_user_id : int

	total_members : int
	roles : list[GroupRole] = []

	update_timestamp : int

class UserProfile(BaseModel):
	user_id : int
	username : str
	display_name : str
	join_date : int
	total_visits : int
	followers : int
	verified : bool

	roblox_badges : list[str] = list() # https://www.roblox.com/info/roblox-badges
	groups : list[(int, int)] = list() # (group_id, rank_id)
	friends : list[int] = list()

	update_timestamp : int

async def search_user_id( user_id : int ) -> Union[UserProfile, None]:
	raise NotImplementedError

async def search_username( username : str ) -> Union[UserProfile, None]:
	raise NotImplementedError
