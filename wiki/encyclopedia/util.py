import re
import random

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))

def entry_existance(title):
    """
    Searches whether entity exist.
    """
    lowercase_list_entries = [entry.lower() for entry in list_entries()]
    if title.lower() in lowercase_list_entries:
        return True
    else:
        return False
    
def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def search_entry(query):
    """
    Retrieves a list of entries which match query. 
    In case of a full match outputs only 1 result.
    """
    entries = list_entries()
    lowercase_list_entries = [entry.lower() for entry in entries]
    if query.lower() in lowercase_list_entries:
        return query, True
    
    search_results = []
    pattern = re.compile(rf".*{re.escape(query.lower())}.*")
    print(pattern)
    i = 0
    for entry in lowercase_list_entries:
        if pattern.search(entry):
            search_results.append(entries[i])
        i+=1
    return search_results, False
    
def random_page_selector():
    """
    Return a random page
    """
    return random.choice(list_entries())
    