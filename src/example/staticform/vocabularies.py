# -*- coding: utf-8 -*-
from plone import api

from zope.interface import implementer
from zope.interface import provider

from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from plone.app.content.browser import vocabulary

from z3c.formwidget.query.interfaces import IQuerySource
from zope.schema.interfaces import IContextSourceBinder

import logging

logger = logging.getLogger(__name__)

# see https://github.com/plone/plone.formwidget.autocomplete/tree/master/plone/formwidget/autocomplete
@implementer(IQuerySource)
class ItalianCities(object):
    vocabulary = SimpleVocabulary((
        SimpleTerm(u'Bologna', 'bologna', u'Bologna'),
        SimpleTerm(u'Palermo', 'palermo', u'Palermo'),
        SimpleTerm(u'Sorrento', 'sorrento', u'Sorrento'),
        SimpleTerm(u'Torino', 'torino', u'Torino')))

    def __init__(self, context):
        self.context = context

    __contains__ = vocabulary.__contains__
    __iter__ = vocabulary.__iter__
    getTerm = vocabulary.getTerm
    getTermByToken = vocabulary.getTermByToken

    def search(self, query_string):
        return [v for v in self if query_string.lower() in v.value.lower()]

@implementer(IContextSourceBinder)
class ItalianCitiesSourceBinder(object):
    def __call__(self, context):
        return ItalianCities(context)


@provider(IVocabularyFactory)
def TestVocabulary(object):
    """ return the a test vocabulary
    """

    terms = (
        { 'token':'t1', 'title':'Ham'  },
        { 'token':'t2', 'title':'Spam' },
        { 'token':'t3', 'title':'Eggs' },
        )
    terms = [ SimpleTerm(value=term['token'], token=term['token'], title=term['title'])
            for term in terms]
    data = SimpleVocabulary(terms)

    return data

vocabulary.PERMISSIONS.update({
            'example.staticform.TestVocabulary': 'View',
})

