import datetime
from optparse import make_option

from facebook_sdk.management.commands.base import CustomBaseCommand
from facebook_sdk.utils import queryset_iterator


class ExtendTokensCommand(CustomBaseCommand):
    help = 'Extend all the users access tokens\'s, per hour'
    option_list = CustomBaseCommand.option_list + (
        make_option('--all',
                    action='store_true',
                    dest='all',
                    default=False,
                    help='Extend all of them at once'
                    ),
    )

    def handle(self, *args, **kwargs):

        queryset_iterator
