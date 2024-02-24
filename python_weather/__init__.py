"""
python-weather
"""

from .enums import Kind, Locale, Phase, Ultraviolet, WindDirection
from .constants import METRIC, IMPERIAL
from .client import Client
from .errors import Error

__version__ = '1.0.3'
__all__ = (
  'METRIC', 'IMPERIAL', 'Client', 'Error', 'Kind', 'Locale', 'Phase',
  'Ultraviolet', 'WindDirection'
)
