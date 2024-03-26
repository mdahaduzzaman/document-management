from rest_framework.throttling import SimpleRateThrottle

class HundredPerDayThrottle(SimpleRateThrottle):
    scope = 'hundred_per_day'

    def get_cache_key(self, request, view):
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }

    def get_rate(self):
        return '1/day'