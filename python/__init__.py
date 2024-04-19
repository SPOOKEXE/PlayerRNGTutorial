
from __future__ import annotations
from enum import Enum
from typing import Union
from pydantic import BaseModel

from rprofile import UserProfile, search_username, search_user_id
from ranking import get_user_id_star_rating, get_username_star_rating

import aiohttp

if __name__ == '__main__':
	pass
