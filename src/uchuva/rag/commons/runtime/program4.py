#------------------------------------------
# Importing modules.
#------------------------------------------
import datetime
import re
import bs4
import logging
import requests
from lxml import html
from html import unescape

#------------------------------------------
# Defining functions.
#------------------------------------------

def get_soup(url):
    """Returns a soup object from a given url."""
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    return soup

def clear_text(text):
    """Returns a clean text from a given text."""
    text = text.lower()
    # parse the HTML
    tree = html.fromstring(text)
    # Remove all script tags (JavaScript code)
    for element in tree.xpath("//script"):
        element.getparent().remove(element)
    # remove all tags and get the text content
    clean_text = tree.text_content()
    # remove escape characters from HTML (noise generators)
    #clean_text = html.unescape(clean_text)
    # remove line breaks and extra spaces
    clean_text = re.sub('\n+', '\n', clean_text)
    clean_text = re.sub('\s+', ' ', clean_text)
    clean_text = clean_text.replace('[[_TOC_]]', '')
    # remove mk bold (**text**), italics (*text*), headers (##) (noise generators)
    clean_text = re.sub(r'\*\*(.*?)\*\*', r'\1', clean_text)
    clean_text = re.sub(r'\*(.*?)\*', r'\1', clean_text)
    clean_text = unescape(clean_text)
    return clean_text

#------------------------------------------
# Main functions.
#------------------------------------------

def extract_text(log, url):
    try:
        soup = get_soup(url)
        text = clear_text(soup.prettify())
        return text
    except Exception as e:
        log.error('Error in program.')
        log.error(e)

def create_observer(log, data):
    try:
        from commons.models import ConceptObserver
        user = data['user']
        url = data['url']
        title = data['title']
        concept = data['concept']
        concept_properties = data['concept_properties']
        # Make formate to concept properties.
        concept_properties_split = concept_properties.split(',')
        concept_properties = []
        for concept_property in concept_properties_split:
            concept_property = concept_property.split()
            concept_property = ' '.join(concept_property)
            concept_property = concept_property.replace(' ', '_')
            concept_properties.append(concept_property)
        concept_properties = ','.join(concept_properties)
        # Create observer.
        conceptObserver = ConceptObserver()
        conceptObserver.User = user
        conceptObserver.url = url
        conceptObserver.active = True
        conceptObserver.created = datetime.datetime.now()
        conceptObserver.title = title
        conceptObserver.json_content = {}
        conceptObserver.concept = concept
        conceptObserver.concept_properties = concept_properties
        conceptObserver.save()
        return True
    except Exception as e:
        log.error('Error in program.')
        log.error(e)
        return False


def stop_observer(log, data):
    """Stop observer."""
    try:
        from commons.models import ConceptObserver
        user = data['user']
        title = data['title']
        # Stop observer.
        conceptObserver = ConceptObserver.objects.get(User=user, title=title)
        conceptObserver.active = False
        conceptObserver.save()
        return True
    except Exception as e:
        log.error('Error in program.')
        log.error(e)
        return False

def delete_observer(log, data):
    """Delete observer."""
    try:
        from commons.models import ConceptObserver
        user = data['user']
        title = data['title']
        # Stop observer.
        conceptObserver = ConceptObserver.objects.get(User=user, title=title)
        conceptObserver.delete()
        return True
    except Exception as e:
        log.error('Error in program.')
        log.error(e)
        return False