import scrapy


def parse_film_data(response):
    title = response.xpath('//*[@class="infobox-above"]//text()').getall()[-1]
    genre = response.xpath('//*[@data-wikidata-property-id="P136"]//text()').getall()
    director = response.xpath('//*[@data-wikidata-property-id="P57"]//text()').getall()
    country = response.xpath('//*[@data-wikidata-property-id="P495"]//text()').getall()
    year = response.xpath(
        '//*[@data-wikidata-property-id="P577"]//a[@title]//text() | '
        '//*[@class="dtstart"]//text()'
    ).getall()

    yield {
        "Название": title,
        "Жанр": genre,
        "Режиссер": director,
        "Страна": country,
        "Год": year,
    }


class WikiMoviesSpider(scrapy.Spider):
    name = "wiki_movies"
    allowed_domains = ["ru.wikipedia.org"]
    start_urls = ["https://ru.wikipedia.org/wiki/Категория:Фильмы_по_алфавиту"]

    def parse(self, response):
        links = response.xpath(
            '//div[@id="mw-pages"]//div[@class="mw-category-group"]//a/@href'
        ).getall()
        for link in links:
            yield response.follow(link, callback=parse_film_data)

        next_page = response.xpath(
            '//a[contains(text(), "Следующая страница")]/@href'
        ).extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
