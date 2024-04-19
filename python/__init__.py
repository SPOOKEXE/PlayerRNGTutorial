
from __future__ import annotations
from roblox import UserProfile, search_username, search_user_id
from ranking import get_profile_star_rating, get_star_rating_name

import asyncio

async def main() -> None:
	profile : UserProfile = await search_username('Roblox')
	print(profile.username)
	rating : int = await get_profile_star_rating( profile )
	print(rating)
	rating_name : str = await get_star_rating_name( rating )
	print(rating_name)

if __name__ == '__main__':
	asyncio.get_event_loop().run_until_complete(main())
