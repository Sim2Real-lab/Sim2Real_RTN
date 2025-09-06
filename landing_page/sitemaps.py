# landing_page/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class LandingPageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9   # slightly lower than homepage if you add more

    def items(self):
        # Use the named URLs defined in landing_page/urls.py
        return [
            "landing_page:main_landing_page",
            "landing_page:sponsor_page",
        ]

    def location(self, item):
        return reverse(item)
