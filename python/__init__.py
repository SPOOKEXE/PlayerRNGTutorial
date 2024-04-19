
from __future__ import annotations
from roblox import UserProfile, search_username, search_user_id
from ranking import StarIncrement, get_profile_star_rating, get_star_rating_name

import asyncio

# async def main() -> None:
# 	profiles : list[UserProfile] = []
# 	for value in range(2):
# 		profiles.append(await search_user_id(5000 + value))

# 	ratings : list[tuple[UserProfile, int, StarIncrement]] = [
# 		(item, *(await get_profile_star_rating(item))) for item in profiles
# 	]

# 	for profile, rating, _ in ratings:
# 		rating_name : str = await get_star_rating_name( rating )
# 		print(profile.user_id, profile.username, rating, rating_name)

async def main() -> None:
	profile : UserProfile = await search_user_id(1)
	print(profile.username)
	rating, incrementors = await get_profile_star_rating( profile )
	print(rating)
	print([dict(item) for item in incrementors])
	rating_name : str = await get_star_rating_name( rating )
	print(rating_name)

if __name__ == '__main__':
	asyncio.get_event_loop().run_until_complete(main())
