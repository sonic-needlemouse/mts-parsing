import scrapy

def parse_film_data(response):
    title = response.xpath('//*[@class="infobox-above"]//text()').getall()[-1]
    genre = response.xpath('//*[@data-wikidata-property-id="P136"]//text()').getall()
    director = response.xpath('//*[@data-wikidata-property-id="P57"]//text()').getall()
    country = response.xpath('//*[@data-wikidata-property-id="P495"]//text()').getall()

    yield {
        'Название': title,
        'Жанр': genre,
        'Режиссер': director,
        'Страна': country,
    }


class WikiMoviesSpider(scrapy.Spider):
    name = "wiki_movies"
    allowed_domains = ["ru.wikipedia.org"]
    start_urls = ["https://ru.wikipedia.org/wiki/Категория:Фильмы_по_алфавиту"]

