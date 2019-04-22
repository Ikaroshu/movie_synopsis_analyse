from scrapy.cmdline import execute

def debug():
    execute(['scrapy', 'crawl', 'imdb_movie', '-o ../imdb_movie.json'])


if __name__ == '__main__':
    debug()