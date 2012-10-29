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
    Return the attribute given a header.

    Params:
        header
            The RCP State Poll page's  table header for a column of data
            Preprocessing:
              - If the header contains the 'dem' or 'rep' headers, set it to
                them explicitly.  This is necessary because those headers have
                arbitrary text (candidate names) before them in the raw html.
            Ex: 'Poll' or 'Obama (D)'


    Returns:
        The matching attribute value if the header exists in _headerToAttribute.
        Ex: 'service' or 'dem'

        None if the header doesn't exist in the _headerToAttribute lookup
    """
    # preprocessing
    if '(D)' in header:
        header = '(D)'
    if '(R)' in header:
        header = '(R)'

    # lookup
    if header in _headerToAttribute:
        return _headerToAttribute[header]
    return None
