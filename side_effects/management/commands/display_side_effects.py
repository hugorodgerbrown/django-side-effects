# -*- coding: utf-8 -*-
"""display_side_effects management command."""
from django.core.management.base import BaseCommand
import side_effects.registry


class Command(BaseCommand):

    help = "Displays project side_effects."

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help="Display full docstring for all side-effect functions."
        )

    def handle(self, *args, **options):
        self.stdout.write("The following side-effects are registered:")
        self.stdout.write("")
        side_effects.registry.display_side_effects(verbose=options['verbose'])
