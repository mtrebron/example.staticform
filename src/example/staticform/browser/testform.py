# -*- coding: utf-8 -*-
from example.staticform import _
from zope import schema
from plone.autoform.form import AutoExtensibleForm
from plone.autoform import directives
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.checkbox import SingleCheckBoxFieldWidget
from plone.app.z3cform.widget import AjaxSelectFieldWidget
#from plone.formwidget.autocomplete import AutocompleteFieldWidget
#from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget
from plone.supermodel import model
from z3c.form import form, button

from Products.statusmessages.interfaces import IStatusMessage

from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider
from zope.component import adapter

#from plone.app.z3cform.interfaces import IFieldPermissionChecker
from plone.app.dexterity.permissions import DXFieldPermissionChecker, GenericFormFieldPermissionChecker

import logging

logger = logging.getLogger(__name__)

class ITestFormMarker(Interface):
    """ marker for product finder form
    """
    pass

@implementer(ITestFormMarker)
class ITestForm(model.Schema):
    """ Testform Schema
    """
    model.fieldset(
        'default',
        label=u'Single Option',
        fields=[
            'select_field',
            'select2_field',
            'radiobutton_field',
        ]
    )

    model.fieldset(
        'multi',
        label=u'Multiple Options',
        fields=[
            'select_multi_field',
            'select2_multi_field',
            'checkbox_field',
        ]
    )

    select_field = schema.Choice(
        title=_(u'Traditional Select Field'),
        description=u"Options should load for anonymous users",
        required=False,
        vocabulary='example.staticform.TestVocabulary',
    )

    select2_field = schema.Choice(
        title=_(u'A Select2 Field'),
        description=u"Options should load for anonymous users",
        required=False,
        vocabulary='example.staticform.TestVocabulary',
    )

    select_multi_field = schema.List(
        title=_(u'A Multiselect Field'),
        description=u"Options should load for anonymous users",
        required=False,
        value_type=schema.Choice(
            vocabulary='example.staticform.TestVocabulary',
        )
    )

    select2_multi_field = schema.List(
        title=_(u'A Select2 field with multiple options'),
        description=u"Options should load for anonymous users",
        required=False,
        value_type=schema.Choice(
            vocabulary='example.staticform.TestVocabulary',
        )
    )

    """
    fails here:
    https://github.com/plone/plone.autoform/blob/master/plone/autoform/widgets.py#L82

    autocomplete_field = schema.List(
        title=_(u'An Autocomplete field'),
        description=u"Options should load for anonymous users",
        required=False,
        value_type=schema.Choice(
            vocabulary='example.staticform.TestVocabulary',
        )
    )

    autocomplete_multi_field = schema.List(
        title=_(u'An Autocomplete field with multiple options'),
        description=u"Options should load for anonymous users",
        required=False,
        value_type=schema.Choice(
            vocabulary='example.staticform.TestVocabulary',
        )
    )

    """
    radiobutton_field = schema.Choice(
        title=_(u'A Radiobutton Field'),
        description=u"Options should load for anonymous users",
        required=False,
        vocabulary='example.staticform.TestVocabulary',
    )

    checkbox_field = schema.List(
        title=_(u'A Checkbox Field'),
        description=u"Options should load for anonymous users",
        required=False,
        value_type=schema.Choice(
            vocabulary='example.staticform.TestVocabulary',
        )
    )
    # these are parsed by the permissions checker
    # see: https://docs.plone.org/external/plone.app.dexterity/docs/reference/form-schema-hints.html#security-related-directives
    # in vocabulary.PERMISSIONS we use the name e.g. 'View'
    # see: https://docs.plone.org/develop/plone/security/permission_lists.html
    directives.write_permission(select2_field='zope2.View')
    directives.write_permission(select2_multi_field='zope2.View')

    # these are NOT parsed by the permissions checker
    directives.read_permission(select2_field='zope2.View')
    directives.read_permission(select2_multi_field='zope2.View')


    """ repeating the vocabulary here has proven useful in translations
        on plone 5.0.x
        it gives us the title of the selected term in the widget rather
        than its token
    """
    directives.widget(
        'select2_field',
        AjaxSelectFieldWidget,
        #vocabulary='example.staticform.TestVocabulary',
        allowNewItems=False,
        orderable=True,
    )

    directives.widget(
        'select2_multi_field',
        AjaxSelectFieldWidget,
        #vocabulary='example.staticform.TestVocabulary',
        allowNewItems=False,
        orderable=True,
    )

    """
    directives.widget(
        'autocomplete_field',
        AutocompleteFieldWidget,
        source='example.staticform.vocabularies.ItalianCitiesSourceBinder',
    )

    directives.widget(
        'autocomplete_multi_field',
        AutocompleteMultiFieldWidget,
        source='example.staticform.vocabularies.ItalianCitiesSourceBinder',
    )
    """

    directives.widget(
        'radiobutton_field',
        RadioFieldWidget,
    )

    directives.widget(
        'checkbox_field',
        CheckBoxFieldWidget,
    )

@adapter(Interface)
@implementer(ITestForm)
class TestFormAdapter(object):
    def __init__(self, context):
        select_field = None
        select2_field = None
        select_multi_field = None
        select2_multi_field = None
        autocomplete_field = None
        autocomplete_multi_field = None
        checkbox_field = None
        radiobutton_field = None


class TestForm(AutoExtensibleForm, form.Form):
    """ boilerplate form copied from Plone docs
    """
    schema = ITestForm
    ignoreContext = True
    form_name = 'testform'

    label = _(u"Testform")
    description = _(u"This is the form description text.")

    def update(self):
        # disable Plone's editable border
        self.request.set('disable_border', True)

        # call the base class version - this is very important!
        # see https://docs.plone.org/develop/addons/schema-driven-forms/creating-a-simple-form/creating-the-form-view.html
        super(TestForm, self).update()


    @button.buttonAndHandler(_(u'Search'))
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        # Handle form submission here. For now, just print it to the console. A more
        # realistic action would be to send the order to another system, send
        # an email, or similar

        for key in data:
            logger.info('%s - %s' % (key, data[key]))

        # Redirect back to the front page with a status message

        IStatusMessage(self.request).addStatusMessage(
                _(u"Thank you for your order. We will contact you shortly"),
                "info"
            )

        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)

class TestFormPermissionChecker(DXFieldPermissionChecker):
    """ this is never applied, why?
    """
    def validate(self, field_name, vocabulary_name=None):
        """ return True for allow or False if denied """
        logger.info('Custom validation returns True')
        return True
