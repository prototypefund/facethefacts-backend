from abc import ABC

import scrapy


class SaarlandHomepageSpider(scrapy.Spider, ABC):
    name = "saarland-homepage"

    start_urls = ["https://www.landtag-saar.de/abgeordnete-und-fraktionen/abgeordnete/"]

    def _parse(self, response, **kwargs):
        for item in response.css("div.ltContainerItem.clearfix"):
            name = item.css("div.ProfileData").css("h4.ProfileName::text")[0].get()
            party = (
                item.css("div.ProfileImageWrapper")
                .css("div.fraction-logo-wrapper")
                .css("img::attr(alt)")[0]
                .get()
            )

            url = (
                item.css("div.ProfileData")
                .css("div.ProfileLink")
                .css("a::attr(href)")[0]
                .get()
            )

            yield {
                "name": name,
                "party": party,
                "url": url,
            }
