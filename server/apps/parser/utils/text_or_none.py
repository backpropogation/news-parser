def text_or_none(selector_obj, field, css):
    """
    Helper method for extracting data from html tags.
    """

    try:
        if 'link' in field:
            return selector_obj.select_one(css).get('href')
        return selector_obj.select_one(css).get_text()
    except AttributeError:
        return 'No data'
