del .\log.txt
del .\abilities_log.txt
del .\abilities.json
scrapy crawl abilities
ren .\file.json abilities.json
ren .\log.txt abilities_log.txt