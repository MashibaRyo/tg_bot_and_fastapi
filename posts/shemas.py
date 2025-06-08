from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SPosts(BaseModel):
    headline: str
    text: str
    created: datetime

class SPostsUpdate(BaseModel):
    headline: Optional[str] = None
    text: Optional[str] = None
    created: Optional[datetime] = None