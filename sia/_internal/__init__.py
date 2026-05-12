"""Internal helpers vendored from the source project.

These are not part of the public SIA API and may change without notice.
They are vendored here so the orchestrator can replay the FCMFD-style
strategy signal construction (Donchian breakout + funding gate + macro
filter) without depending on the source project's strategy code.

External callers should NOT import from sia._internal directly. Use
the public API in sia.__init__ instead.
"""

from sia._internal.donchian import donchian_high, donchian_low
from sia._internal.funding_gate import funding_gate, load_funding_aligned_to_4h
from sia._internal.macro_ema import macro_filter

__all__ = [
    "donchian_high",
    "donchian_low",
    "funding_gate",
    "load_funding_aligned_to_4h",
    "macro_filter",
]
