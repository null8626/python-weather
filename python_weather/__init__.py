# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021-2026 null8626

from .enums import HeatIndex, Kind, Locale, Phase, UltraViolet, WindDirection
from .constants import METRIC, IMPERIAL
from .errors import Error, RequestError
from .forecast import Forecast
from .version import VERSION
from .client import Client


__title__ = 'python-weather'
__author__ = 'null8626'
__credits__ = (__author__,)
__maintainer__ = __author__
__status__ = 'Production'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2021-2026 null8626'
__version__ = VERSION
__all__ = (
  'METRIC',
  'IMPERIAL',
  'Client',
  'Error',
  'Forecast',
  'RequestError',
  'HeatIndex',
  'Kind',
  'Locale',
  'Phase',
  'UltraViolet',
  'VERSION',
  'WindDirection',
)
