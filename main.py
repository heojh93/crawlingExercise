from naverSiteCrawler import *
from logaCrawler2 import *

import xlsxwriter

keyword = crawl(maxPage())
workbook = xlsxwriter.Workbook('analysis.xlsx')
worksheet = workbook.add_worksheet(keyword)

logaCrawl(worksheet)


worksheet.write(0, 0, '이름')
worksheet.write(0, 1, 'URL')
worksheet.write(0, 2, '네이버 프리미엄')
worksheet.write(0, 3, '네이버 일반')
worksheet.write(0, 4, '다음 프리미엄')
worksheet.write(0, 5, '다음 일반')

workbook.close()
