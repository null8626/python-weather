# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021-2026 null8626


class Error(Exception):
  """The base error class. Extends :py:class:`Exception`."""

  __slots__: tuple[str, ...] = ()


class RequestError(Error):
  """Thrown upon HTTP request failure. Extends :class:`.Error`."""

  __slots__: tuple[str, ...] = 'status', 'reason'

  status: int | None
  """The status code."""

  reason: str | None
  """The reason for this status code."""

  def __init__(self, status: int | None, reason: str | None):
    self.status = status
    self.reason = reason

    super().__init__(f'{status}: {reason}')

  def __repr__(self) -> str:  # pragma: nocover
    return f'<{__class__.__module__}.{__class__.__name__} status={self.status} reason={self.reason!r}>'
