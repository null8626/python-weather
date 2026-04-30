# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021-2026 null8626


from dataclasses import dataclass


class Error(Exception):
  """The base error class. Extends :py:class:`Exception`."""

  __slots__: tuple[str, ...] = ()


@dataclass(repr=False, slots=True)
class RequestError(Error):
  """Thrown upon HTTP request failure. Extends :class:`.Error`."""

  status: int | None
  """The status code."""

  reason: str | None
  """The reason for this status code."""

  def __post_init__(self) -> None:
    super(Error, self).__init__(f'{self.status}: {self.reason}')

  def __repr__(self) -> str:  # pragma: nocover
    """The error's debug string representation."""
    return f'<{__class__.__module__}.{__class__.__name__} status={self.status} reason={self.reason!r}>'
