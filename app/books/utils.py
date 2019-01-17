def is_isbn_or_key(word):
    """
    Determine whether it is a keyword or isbn.
    :param word:
    :return:
    """
    isbn_or_key = 'key'
    if len(word) == 13 and q.isdigit():
        isbn_or_key = 'isbn'
    short_word = word.replace('-', '')
    if '-' in word and len(short_word) == 10 and short_word.isdigit:
        isbn_or_key = 'isbn'
    return isbn_or_key
