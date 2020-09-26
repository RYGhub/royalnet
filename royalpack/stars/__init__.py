# Imports go here!
from .api_bio import ApiBioSetStar
from .api_diario import ApiDiarioGetStar
from .api_diario_all import ApiDiarioAllStar
from .api_discord_cv import ApiDiscordCvStar
from .api_fiorygi import ApiFiorygiStar
from .api_diario_random import ApiDiarioRandomStar
from .api_poll import ApiPollStar
from .api_poll_list import ApiPollsListStar
from .api_cvstats_latest import ApiCvstatsLatestStar
from .api_cvstats_avg import ApiCvstatsAvgStar
from .api_user_ryg import ApiUserRygStar
from .api_user_ryg_list import ApiUserRygListStar
from .api_user_avatar import ApiUserAvatarStar
from .api_auth_login_osu import ApiAuthLoginOsuStar
from .api_diario_range import ApiDiarioRangeStar
from .api_diario_latest import ApiDiarioLatestStar
from ..halloween2020.api_user_trionfi import ApiUserTrionfiStar

# Enter the PageStars of your Pack here!
available_page_stars = [
    ApiBioSetStar,
    ApiDiarioGetStar,
    ApiDiarioAllStar,
    ApiDiscordCvStar,
    ApiFiorygiStar,
    ApiDiarioRandomStar,
    ApiPollStar,
    ApiPollsListStar,
    ApiCvstatsLatestStar,
    ApiCvstatsAvgStar,
    ApiUserRygStar,
    ApiUserRygListStar,
    ApiUserAvatarStar,
    ApiAuthLoginOsuStar,
    ApiDiarioRangeStar,
    ApiDiarioLatestStar,
    ApiUserTrionfiStar,
]

# Don't change this, it should automatically generate __all__
__all__ = [star.__name__ for star in available_page_stars]
