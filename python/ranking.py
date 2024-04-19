
from typing import Union
from rprofile import search_user_id, search_username, UserProfile

import aiohttp
import asyncio

BADGE_VALUES = {
	# Membership Badges
	'Welcome To The Club Badge' : 5,
	# Community Badges
	"Administrator Badge" : 100,
	"Veteran Badge" : 20,
	"Friendship Badge" : 10,
	"Ambassador Badge" : 50,
	"Inviter Badge" : 25,
	# Developer Badges
	"Homestead Badge" : 5,
	"Bricksmith Badge" : 10,
	"Official Model Maker Badge" : 20,
	# Gamer Badges
	"Combat Initiation Badge" : 10,
	"Warrior Badge" : 20,
	"Bloxxer Badge" : 30
}

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

RANKING_BOUNDARIES = [
	[ 150, "Mythic" ],
	[ 110, "Legendary" ],
	[ 80, "Epic" ],
	[ 50, "Rare" ],
	[ 20, "Uncommon" ],
	[ -1, "Common" ],
]

USERNAME_LETTER_COUNT = [
	[ 4, 20 ],
	[ 5, 10 ],
	[ 6, 5 ]
]

async def get_user_id_star_rating( user_id : int ) -> Union[int, None]:
	raise NotImplementedError

async def get_username_star_rating( username : str ) -> Union[int, None]:
	raise NotImplementedError
