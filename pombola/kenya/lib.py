from django.db.models import Q

def significant_positions_filter(qs):
    """Return a queryset only with 'significant' positions from it

    If you pass in a Position queryset, this should return a queryset
    which has filtered out any positions that aren't considered
    'significant' for this country; this is used to determine which
    positions are shown on place pages, for instance.

    In the case of Kenya, we want to include anyone with the title
    'Senator', with the title 'Member of the National Assembly', or
    the President of the Republic of Kenya.
    """

    return qs.filter(
        Q(title__slug='president', organisation__slug='republic-of-kenya') |
        Q(title__slug__in=('senator',
                           # 'governor',
                           # 'ward-representative',
                           'member-national-assembly')))
