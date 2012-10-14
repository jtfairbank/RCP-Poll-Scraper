"""
This module provides common functions to extract polling data from a state page
that lists polls.  See each function's documentation for details.

It also contains some common pre-populated data structures:
    attributeToHeader
        Maps a state page's Poll Data table headers to pollitem attributes.
"""

# TODO: make into a private var with an accessor funciton?
headerToAttribute = {
    "Poll": "service",
    "Date": "date",
    "Sample": "sample",
    "MoE": "error",
    "Romney (R)": "rep",
    "Obama (D)": "dem",
}
