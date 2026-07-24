# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021-2026 null8626

from .client import Client
from .constants import IMPERIAL, METRIC
from .enums import HeatIndex, Kind, Locale, Phase, UltraViolet, WindDirection
from .errors import Error, RequestError
from .forecast import Forecast
from .version import VERSION

__title__ = 'python-weather'
__author__ = 'null8626'
__credits__ = (__author__,)
__maintainer__ = __author__
__status__ = 'Production'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2021-2026 null8626'
__version__ = VERSION
__all__ = (
  'IMPERIAL',
  'METRIC',
  'VERSION',
  'Client',
  'Error',
  'Forecast',
  'HeatIndex',
  'Kind',
  'Locale',
  'Phase',
  'RequestError',
  'UltraViolet',
  'WindDirection',
)
