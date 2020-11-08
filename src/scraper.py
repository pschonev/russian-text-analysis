import scrapy


class HPSpider(scrapy.Spider):
    name = "hpspider"
    start_urls = ['']
    
    def parse(self, response):
            BOOK_SELECTOR = '.read'
            for book in response.css(BOOK_SELECTOR):
                LINK_SELECTOR = 'a::attr(href)'
                booklink = book.css(LINK_SELECTOR).extract_first()
                if booklink:
                    yield scrapy.Request(
                        response.urljoin(booklink),
                        callback=self.parse_index
                    )

    def parse_index(self, response):
        CHAPTER_SELECTOR = '#list'
        chapter = response.css(CHAPTER_SELECTOR)
        print(chapter)

        LINK_SELECTOR = 'a::attr(href)'
        for chapter_link in chapter.css(LINK_SELECTOR).extract():
            if chapter_link:
                yield scrapy.Request(
                    response.urljoin(chapter_link),
                    callback=self.parse_chapter
                )

    def parse_chapter(self, response):
        BOOK_SELECTOR = "#title a::text"
        book = response.css(BOOK_SELECTOR).extract_first()

        CHAPTER_SELECTOR = "#chapter::text"
        chapter = response.css(CHAPTER_SELECTOR).extract_first()

        TEXT_SELECTOR = "#main p::text"
        text = response.css(TEXT_SELECTOR).extract()
        text = "\n".join(text)
        
        yield {
            "book": book,
            "chapter": chapter,
            "text": text
        }