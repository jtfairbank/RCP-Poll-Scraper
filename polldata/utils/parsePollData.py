"""
This module provides common functions to extract polling data from a state page
that lists polls.  See each function's documentation for details.

It also contains some common pre-populated data structures:
    attributeToHeader
        Maps a state page's Poll Data table headers to pollitem attributes.
"""

_headerToAttribute = {
    "Poll": "service",
    "Date": "date",
    "Sample": "sample",
    "MoE": "error",
    "(R)": "rep",
    "(D)": "dem",
}

def getAttribute(header):
    """
    Return the attribute given a header.  Note that since the (R) and (D)
    headers are non standard and have the candidate name before them, we
    have to also check the last three characters of the header for matches
    to these headers.

    Params:
        header - the RCP State Poll page's  table header for a column of data

    Returns:
        the matching attribute value if the header exists in _headerToAttribute
        None if the header doesn't exist in the _headerToAttribute lookup
    """
    if header in _headerToAttribute:
        return _headerToAttribute[header]
    elif header[-3:] in _headerToAttribute:
        return _headerToAttribute[ header[-3:] ]
    return None
