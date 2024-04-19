
from datetime import datetime
from typing import Union
from roblox import search_user_id, search_username, UserProfile

import aiohttp
import asyncio

BADGE_VALUES = [
	[ 1, 100, ], # administrator badge
	[ 2, 5, ], # friendship badge
	[ 3, 5, ], # combat initiation
	[ 4, 10, ], # warrior
	[ 5, 25, ], # bloxxer
	[ 6, 5, ], # homestead
	[ 7, 10, ], # bricksmith
	[ 8, 10, ], # inviter
	[ 12, 5, ], # veteran
	[ 17, 15, ], # official model maker
	[ 18, 10, ], # welcome to the club
]

PLACE_VISITS = [
	[ 1e9, 60 ], # 1 bill
	[ 1e8, 50 ], # 100 mill
	[ 1e7, 40 ], # 10 mill
	[ 1e6, 30 ], # 1 mill
	[ 1e5, 20 ], # 100k
	[ 1e4, 10 ], # 10k
	[ 1e3, 5 ], # 1k
]

FOLLOWERS = [
	[ 1e6, 30 ], # 1 mill
	[ 1e5, 20 ], # 100k
	[ 1e4, 10 ], # 10k
	[ 1e3, 5 ], # 1k
]

USERNAME_LETTER_COUNT = [
	[ 4, 20 ],
	[ 5, 10 ],
	[ 6, 5 ],
]

SECONDS_PER_YEAR : int = 60 * 60 * 24 * 365
ACCOUNT_AGE = [
	[ SECONDS_PER_YEAR * 17, 80 ],
	[ SECONDS_PER_YEAR * 15, 60 ],
	[ SECONDS_PER_YEAR * 13, 40 ],
	[ SECONDS_PER_YEAR * 11, 20 ],
	# <10 years
	[ SECONDS_PER_YEAR * 9, 10 ],
	[ SECONDS_PER_YEAR * 7, 7 ],
	[ SECONDS_PER_YEAR * 5, 5 ],
	[ SECONDS_PER_YEAR * 4, 4 ],
	[ SECONDS_PER_YEAR * 3, 3 ],
	[ SECONDS_PER_YEAR * 2, 2 ],
	[ SECONDS_PER_YEAR * 1, 1 ],
]

RANKING_BOUNDARIES = [
	[ 280, "Godly" ],
	[ 240, "Ultimate" ],
	[ 180, "Mythic" ],
	[ 140, "Exotic" ],
	[ 120, "Legendary" ],
	[ 100, "Epic" ],
	[ 60, "Rare" ],
	[ 20, "Uncommon" ],
	[ -1, "Common" ],
]

async def get_profile_star_rating( profile : UserProfile ) -> int:

	star_count : int = 0

	# roblox badges
	def find_badge_value( bid : int ) -> int:
		for other in BADGE_VALUES:
			if bid == other[0]:
				return other[1]
		return 5
	for item in profile.roblox_badges:
		star_count += find_badge_value( item.id )

	# followers
	for item in FOLLOWERS:
		if profile.followers_count > item[0]:
			star_count += item[1]
			break

	# place visits
	for item in PLACE_VISITS:
		if profile.total_visits > item[0]:
			star_count += item[1]
			break

	# username length
	for item in USERNAME_LETTER_COUNT:
		if len(profile.username) <= item[0]:
			star_count += item[1]
			break

	# account age
	for item in ACCOUNT_AGE:
		if profile.account_age > item[0]:
			star_count += item[1]
			break

	return star_count

async def get_star_rating_name( rating : int ) -> str:
	for item in RANKING_BOUNDARIES:
		if rating > item[0]:
			return item[1]
	return RANKING_BOUNDARIES[-1][1]
