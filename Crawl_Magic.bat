del .\log.txt
del .\magic_log.txt
del .\magic.json
scrapy crawl magic
ren .\file.json magic.json
ren .\log.txt magic_log.txt