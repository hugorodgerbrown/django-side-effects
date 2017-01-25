# -*- coding: utf-8 -*-
"""side_effects.settings"""
# from env_utils import get_env, get_bool

# from django.conf import settings

# try:
#     import django_rq  # noqa
#     QUEUE_ENABLED = True
# except ImportError:
#     QUEUE_ENABLED = False


# # the name of the side_effects RQ queue - defaults to 'side_effects'
# QUEUE_NAME = (
#     get_env('SIDE_EFFECTS_QUEUE_NAME', None) or
#     getattr(settings, 'SIDE_EFFECTS_QUEUE_NAME', 'side_effects')
# )

# # whether to process RQ jobs sync or async - defaults to async
# QUEUE_ASYNC = (
#     get_bool('SIDE_EFFECTS_QUEUE_ASYNC', False) or
#     getattr(settings, 'SIDE_EFFECTS_QUEUE_ASYNC', True)
# )

# if settings.DEBUG:
#     print
#     (
#         """
#         side_effects.settings:

#         QUEUE_ENABLED: {}
#         QUEUE_NAME:    {}
#         QUEUE_ASYNC:   {}
#         """.format(QUEUE_ENABLED, QUEUE_NAME, QUEUE_ASYNC)
#     )
