def contains_filter_keywords(flat_elem, user_filters):
    """Check if the flat contains any of the filter keywords and return the keywords."""

    # Find all keywords that are in the flat_elem's text
    keywords_found = [
        keyword
        for keyword in user_filters
        if str(keyword).strip().lower() in flat_elem.text.lower()
    ]

    # Return a tuple of boolean and keywords found
    return (bool(keywords_found), keywords_found)
