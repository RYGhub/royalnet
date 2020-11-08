import royalnet.constellation.api as rca
import royalnet.utils as ru


class ApiCvstatsMonthsStar(rca.ApiStar):
    path = "/api/cvstats/months/v1"

    tags = ["cvstats"]

    @rca.magic
    async def get(self, data: rca.ApiData) -> ru.JSON:
        """Get some averages on the cvstats."""
        results = data.session.execute("""
SELECT date_part('month', c.m)  pm,
       date_part('hour', c.h)   ph,
       AVG(c.members_connected) members_connected,
       AVG(c.users_connected)   users_connected,
       AVG(c.members_online)    members_online,
       AVG(c.users_online)      users_online,
       AVG(c.members_playing)   members_playing,
       AVG(c.users_playing)     users_playing,
       AVG(c.members_total)     members_total,
       AVG(c.users_total)       users_total
FROM (
         SELECT date_trunc('month', c.timestamp) m,
                date_trunc('hour', c.timestamp) h,
                AVG(c.members_connected)        members_connected,
                AVG(c.users_connected)          users_connected,
                AVG(c.members_online)           members_online,
                AVG(c.users_online)             users_online,
                AVG(c.members_playing)          members_playing,
                AVG(c.users_playing)            users_playing,
                AVG(c.members_total)            members_total,
                AVG(c.users_total)              users_total
         FROM cvstats c
         GROUP BY m, h
     ) c
GROUP BY pm, ph;
        """)

        return [{
            "m": r[0],
            "h": r[1],
            "all_time": {
                "members_connected": float(r[2]) if r[2] is not None else None,
                "users_connected": float(r[3]) if r[3] is not None else None,
                "members_online": float(r[4]) if r[4] is not None else None,
                "users_online": float(r[5]) if r[5] is not None else None,
                "members_playing": float(r[6]) if r[6] is not None else None,
                "users_playing": float(r[7]) if r[7] is not None else None,
                "members_total": float(r[8]) if r[8] is not None else None,
                "users_total": float(r[9]) if r[9] is not None else None,
            }
        } for r in sorted(results.fetchall(), key=lambda s: (s[0], s[1]))]
