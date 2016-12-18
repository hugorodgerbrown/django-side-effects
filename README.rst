.. image:: https://travis-ci.org/yunojuno/django-onfido.svg?branch=master
    :target: https://travis-ci.org/yunojuno/django-onfido

.. image:: https://badge.fury.io/py/django-onfido.svg
    :target: https://badge.fury.io/py/django-onfido

.. image:: https://codecov.io/gh/yunojuno/django-onfido/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/yunojuno/django-onfido

Django Onfido
==============

Django app for integration with the Onfido API (v2)

Background
----------

Onfido is an online identity verification service. It provides API access to a range of tests (identity, right to work, criminal history, credit report). It is assumed that you are only interested in this project because you are already aware of what Onfido does, and so I won't repeat it here. If you want to find out more, head over to their website.

If you *are* using Onfido, and you are using Django, then this project can be used to manage Onfido checks against your existing Django users. It handles the API interactions, as well as providing the callback webhooks required to support live status updates.

Installation
------------

The project is available through PyPI as ``django-onfido``:

.. code::

    $ pip install django-onfido

And the main package itself is just ``onfido``:

.. code:: python

    >>> from onfido import api, models, views, urls, admin, signals, helpers, decorators

Usage
-----

The main use case is as follows:

1. Create an Onfido **Applicant** from your Django user:

.. code:: python

    >>> from django.contrib.auth.models import User
    >>> from onfido.helpers import create_applicant
    >>> user = User.objects.last()  # any old one will do
    >>> applicant = create_applicant(user)
    DEBUG Making POST request to https://api.onfido.com/v2/applicants
    DEBUG <Response [201]>
    DEBUG {u'first_name': u'hugo', u'last_name': u'rb', u'middle_name': None, ...}
    DEBUG Creating new Onfido applicant from JSON: {u'first_name': u'hugo', u'last_name': u'rb', ...}
    <Applicant id=a2c98eae-XXX user='hugo'>

2. Create your check + reports for the applicant:

.. code:: python

    >>> from onfido.helpers import create_check
    >>> create_check(applicant, 'standard', ['identity', 'right_to_work'])
    >>> assert Check.objects.count() == 1
    >>> assert Report.objects.count() == 2

This will create the **Check** and **Report** objects on Onfido, and store them locally as Django model objects.

3. Wait for callback events to update the status of reports and checks:

.. code:: shell

    DEBUG Received Onfido callback: {"payload":{...}}
    DEBUG Processing 'check.completed' action on check.bd8232c4-...

NB If you are using the callback functionality, you **must** set the ``ONFIDO_WEBHOOK_TOKEN``
property (see settings section below). The callback handler will force verification of the
X-Signature request header as specified in the `webhooks documentation <https://documentation.onfido.com/#webhooks>`_.

The raw JSON
returned from the API for a given entity (``Applicant``, ``Check``, ``Report``) is stored on
the model as the ``raw`` attribute, and this can be parsed into the relevant model
attributes. (Yes this does mean duplication of data.) The core pattern for interaction with the API on a per-object basis is a read-only
fetch / pull pattern (analagous to git operations of the same name). If you call the ``fetch`` method
on an object, it will use the ``href`` value in the raw JSON to fetch the latest
data from the API and parse it, but without saving the changes. If you want
to update the object, use the ``pull`` method instead.

The ``Report`` object is a special case, where the raw data from the API often contains sensitive information that you may not wish to store locally (passport numbers, Visa information, personal data). In order to get around this, there is a ``scrub_report_data`` function that will remove certain attributes of the raw data before it is parsed. By default this will remove the ``breakdown`` and ``properties`` elements.

.. code:: python

    >>> check = Check.objects.last()
    >>> check.raw
    {
        "id": "c26f22d5-4903-401f-8a48-7b0211d03c1f",
        "created_at": "2016-10-15T19:05:50Z",
        "status": "awaiting_applicant",
        "type": "standard",
        "result": "clear",
        "href": "applicants/123/checks/456"
    }
    >>> check.fetch()  # fetch and parse the latest raw data
    >>> check.pull()  # calls fetch and then saves the object

Settings
--------

The following settings can be specified as environment settings or within the Django settings.

* ``ONFIDO_API_KEY``: your API key, found under **setting** in your Onfido account.
* ``ONFIDO_WEBHOOK_TOKEN``: (optional) the Onfido webhook callback token - required if using webhooks.

The following settings can be specified in the Django settings:

* ``ONFIDO_LOG_EVENTS``: (optional) if True then callback events from the API will also be recorded as ``Event`` objects. Defaults to False.
* ``ONFIDO_REPORT_SCRUBBER``: (optional) a function that is used to scrub sensitive data from ``Report`` objects. The default implementation will remove **breakdown** and **properties**.

Tests
-----

The project has pretty good test coverage (>90%) and the tests themselves run through ``tox``.

.. code::

    $ pip install tox
    $ tox

If you want to run the tests manually, make sure you install the requirements, and Django.

.. code::

    $ pip install -r requirements.txt
    $ pip install django==1.8  # your version goes here
    $ python manage.py test onfido.tests

If you are hacking on the project, please keep coverage up.

Contributing
------------

Standard GH rules apply: clone the repo to your own account, create a branch, make sure you update the tests, and submit a pull request.

Status
------

This project is very early in its development. We are using it at YunoJuno, but 'caveat emptor'. It currently only supports 'standard' checks, and has very patchy support for the full API. It does what we need it to do right now, and we will extend it as we evolve. If you need or want additional features, get involved :-).
