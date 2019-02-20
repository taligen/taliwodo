import re

def formatTaligenString( s ):
    """
    Format a Taligen-formatted string in HTML
    """
    ret = s

    for ( key, value ) in {
            "&": "&amp;",
            '"': "&quot;",
            "'": "&apos;",
            ">": "&gt;",
            "<": "&lt;" }.items() :
        ret = ret.replace( key, value )

    ret = re.sub( '``([^`]*)``', '<pre>\\1</pre>', ret ) # Double-`` means <pre> with linebreaks
    ret = re.sub( '`([^`]*)`', '<code>\\1</code>', ret ) # Single-` means <code> without linebreaks


    return ret
