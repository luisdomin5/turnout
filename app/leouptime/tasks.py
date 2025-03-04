from celery import shared_task

from common.rollouts import get_feature_bool


@shared_task()
def check_uptime_group(slug, down_sites=False):
    from .uptime import check_group

    check_group(slug, down_sites=down_sites)


@shared_task()
def check_uptime():
    from .uptime import check_all

    if get_feature_bool("leouptime", "check"):
        check_all()

    # from .uptime import MONITORS
    # for slug in MONITORS.keys():
    #    check_uptime_group.delay(slug)


@shared_task()
def check_uptime_downsites():
    from .uptime import MONITORS

    if not get_feature_bool("leouptime", "check"):
        return

    for slug in MONITORS.keys():
        check_uptime_group.delay(slug, down_sites=True)


@shared_task()
def tweet_uptime():
    from .uptime import tweet_all_sites

    tweet_all_sites()


@shared_task()
def check_proxies():
    from .proxy import check_proxies

    check_proxies()


@shared_task()
def check():
    check_proxies()
    check_uptime()
