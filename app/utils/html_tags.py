import re

def remove_html_tags(text):
    """Remove HTML tags from a string."""
    # Remove JavaScript
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Remove CSS
    text = re.sub(r'<style.*?>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Replace line breaks with spaces to preserve spacing
    text = text.replace('\r\n', ' ')
    # Use regular expression to remove HTML tags
    clean = re.compile('<.*?>')

    return re.sub(clean, '', text)