
from pydantic import BaseModel, Field
from roblox import RobloxBadge, UserProfile

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

class StarIncrement(BaseModel):
	name : str = Field('unknown')
	amount : int = Field(-1)

async def badge_value_by_id( badge_id : int ) -> int:
	for other in BADGE_VALUES:
		if other[0] == badge_id:
			return other[1]
	return 10

async def get_profile_star_rating( profile : UserProfile ) -> tuple[int, list[StarIncrement]]:

	star_count : int = 0
	star_incrementors : list[StarIncrement] = []

	# roblox badges
	for item in profile.roblox_badges:
		value : int = await badge_value_by_id( item.id )
		star_incrementors.append(StarIncrement(name=f'Owns Badge: {item.name}', amount=value))
		star_count += value

	# followers
	for item in FOLLOWERS:
		if profile.followers_count > item[0]:
			star_count += item[1]
			star_incrementors.append(StarIncrement(name=f'Followers - >{int(item[0])}', amount=item[1]))
			break

	# place visits
	for item in PLACE_VISITS:
		if profile.total_visits > item[0]:
			star_count += item[1]
			star_incrementors.append(StarIncrement(name=f'Profile Visits - >{item[0]}', amount=item[1]))
			break

	# username length
	for item in USERNAME_LETTER_COUNT:
		if len(profile.username) <= item[0]:
			star_count += item[1]
			star_incrementors.append(StarIncrement(name=f'{item[0]} Letter Username', amount=item[1]))
			break

	# account age
	for item in ACCOUNT_AGE:
		if profile.account_age > item[0]:
			star_count += item[1]
			star_incrementors.append(StarIncrement(name=f'Account Age - >{round(item[0] / SECONDS_PER_YEAR)}yrs', amount=item[1]))
			break

	star_incrementors.sort(key=lambda x : x.amount, reverse=True)
	return star_count, star_incrementors

async def get_star_rating_name( rating : int ) -> str:
	for item in RANKING_BOUNDARIES:
		if rating > item[0]:
			return item[1]
	return RANKING_BOUNDARIES[-1][1]
