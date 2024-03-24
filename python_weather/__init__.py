"""
python-weather
"""

from .enums import HeatIndex, Kind, Locale, Phase, UltraViolet, WindDirection
from .constants import METRIC, IMPERIAL
from .client import Client
from .errors import Error

__version__ = '2.0.0'
__all__ = (
  'METRIC',
  'IMPERIAL',
  'Client',
  'Error',
  'HeatIndex',
  'Kind',
  'Locale',
  'Phase',
  'UltraViolet',
  'WindDirection',
)
