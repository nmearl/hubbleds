import ipyvue
from pathlib import Path
from cosmicds import STORY_PATHS
from .story import *
from .stages import *
from .tools import *
from .viewers import *
from .components import *


STORY_PATHS['hubble'] = Path(__file__).parent / "HubbleDS.ipynb"
