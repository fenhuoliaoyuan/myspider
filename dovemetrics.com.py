import re

import requests

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'brw=brwPVOSDzoIiAOeWh; AWSELBCORS=F5E9CFCB0C87D62DB5D03914FDC2A2D2D45FBECE928DF16D8E12854A4A958CD126842E8B660BC1262B9940A7DF1D234855648842F3135A095D1EFD5F46A1E9A1457DE6E100; phg=0; __Host-airtable-session=eyJzZXNzaW9uSWQiOiJzZXNKVFBsS3NlUjNSTHZHaiIsImNzcmZTZWNyZXQiOiItY1RMd05UMlNya2dKdmJJeVpXTW05NVkiLCJoaWdoU2VjdXJpdHlNb2RlRW5hYmxlZFRpbWUiOjE2NDA1OTc1MDQ3ODUsInVzZXJJZCI6InVzcnNrc01CYkpIUVhqSVdIIn0=; __Host-airtable-session.sig=oAgXZHis9w2hCb8V1-zJdVG5LhY_yo7MJNWmQRUAWAY; mv=eyJzdGFydFRpbWUiOiIyMDIxLTEyLTI3VDEyOjA5OjE4LjI4OFoiLCJyZWZlcnJlciI6Imh0dHBzOi8vd3d3LmRvdmVtZXRyaWNzLmNvbS8iLCJsb2NhdGlvbiI6Imh0dHBzOi8vYWlydGFibGUuY29tL2VtYmVkL3NoclA3dUUqKioqKioqKioqL3RibEVmSkU5MTd5MURoZjUxIiwiaW50ZXJuYWxUcmFjZUlkIjoidHJjV1dwYzNNYWI1WEFCZ2oifQ==; mbpg=2022-12-27T12:11:51.303ZusrsksMBbJHQXjIWHpro; mbpg.sig=gNKj1UINqEJ-iXf8-U_XCNWqMbe_oANWACKh5yCBXpc',
    'Host': 'airtable.com',
    'ot-tracer-sampled': 'true',
    'ot-tracer-spanid': '1143729609c9bdb3',
    'ot-tracer-traceid': '3c2c190211e73c42',
    'Pragma': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'x-airtable-application-id': 'apppcI0nClUwo3GCb',
    'x-airtable-client-queue-time': '3498.2000000476837',
    'x-airtable-inter-service-client': 'webClient',
    'x-airtable-inter-service-client-code-version': 'f8a1ae006732e3cb41b78bd7cb41d1187895e8f9',
    'x-airtable-page-load-id': 'pglVqi8BxLsW0TF2n',
    'X-Requested-With': 'XMLHttpRequest',
    'x-time-zone': 'Asia/Shanghai',
    'x-user-locale': 'zh-cn'
}
url = 'https://airtable.com/v0.3/application/apppcI0nClUwo3GCb/read?stringifiedObjectParams=%7B%22includeDataForTableIds%22%3A%5B%22tblEfJE917y1Dhf51%22%5D%2C%22includeDataForViewIds%22%3Anull%2C%22shouldIncludeSchemaChecksum%22%3Atrue%2C%22mayOnlyIncludeRowAndCellDataForIncludedViews%22%3Atrue%7D&requestId=req58hOqBcOcKErou&accessPolicy=%7B%22allowedActions%22%3A%5B%7B%22modelClassName%22%3A%22application%22%2C%22modelIdSelector%22%3A%22apppcI0nClUwo3GCb%22%2C%22action%22%3A%22read%22%7D%2C%7B%22modelClassName%22%3A%22application%22%2C%22modelIdSelector%22%3A%22apppcI0nClUwo3GCb%22%2C%22action%22%3A%22readForDetailView%22%7D%2C%7B%22modelClassName%22%3A%22table%22%2C%22modelIdSelector%22%3A%22apppcI0nClUwo3GCb+*%22%2C%22action%22%3A%22read%22%7D%2C%7B%22modelClassName%22%3A%22table%22%2C%22modelIdSelector%22%3A%22apppcI0nClUwo3GCb+*%22%2C%22action%22%3A%22readData%22%7D%2C%7B%22modelClassName%22%3A%22table%22%2C%22modelIdSelector%22%3A%22apppcI0nClUwo3GCb+*%22%2C%22action%22%3A%22readDataForRowCards%22%7D%2C%7B%22modelClassName%22%3A%22view%22%2C%22modelIdSelector%22%3A%22apppcI0nClUwo3GCb+*%22%2C%22action%22%3A%22readRowOrder%22%7D%2C%7B%22modelClassName%22%3A%22view%22%2C%22modelIdSelector%22%3A%22apppcI0nClUwo3GCb+*%22%2C%22action%22%3A%22readData%22%7D%2C%7B%22modelClassName%22%3A%22view%22%2C%22modelIdSelector%22%3A%22apppcI0nClUwo3GCb+*%22%2C%22action%22%3A%22getMetadataForPrinting%22%7D%2C%7B%22modelClassName%22%3A%22row%22%2C%22modelIdSelector%22%3A%22apppcI0nClUwo3GCb+*%22%2C%22action%22%3A%22readDataForDetailView%22%7D%2C%7B%22modelClassName%22%3A%22row%22%2C%22modelIdSelector%22%3A%22apppcI0nClUwo3GCb+*%22%2C%22action%22%3A%22createBoxDocumentSession%22%7D%2C%7B%22modelClassName%22%3A%22row%22%2C%22modelIdSelector%22%3A%22apppcI0nClUwo3GCb+*%22%2C%22action%22%3A%22createDocumentPreviewSession%22%7D%5D%2C%22shareId%22%3A%22shrP7uEmnxbv7dUEV%22%2C%22applicationId%22%3A%22apppcI0nClUwo3GCb%22%2C%22sessionId%22%3A%22sesJTPlKseR3RLvGj%22%2C%22generationNumber%22%3A0%2C%22signature%22%3A%22b9221d3cdbcf703dbfa84051b2c1ed01bf478427975f220faf9860589eb9b29e%22%7D'
res = requests.get(url=url, headers=headers).json()
choices_TICCKER = res['data']['tableSchemas'][4]['columns'][2]['typeOptions']['choices']#'data.tableSchemas[4].columns[2].typeOptions.choices'
choices_LOCATION = res['data']['tableSchemas'][4]['columns'][10]['typeOptions']['choices']#‘data.tableSchemas[4].columns[10].typeOptions.choices
rows = res['data']['tableDatas'][0]['rows']
# print()
for row in rows:
    COMPANY = row['cellValuesByColumnId']['fldYopilw6pRY334s']
    # TICKER = choices[row['cellValuesByColumnId']['fldK0vbIANJe4oZgL']]['name']
    TICKER = choices_TICCKER[row['cellValuesByColumnId']['fldK0vbIANJe4oZgL']]['name']
    LOCATION = choices_LOCATION[row['cellValuesByColumnId']['fldcS8EC1HmIuKx7k']]['name']
    YEAR_FOUNDED = row['cellValuesByColumnId']['fldYaVxLsnQ8BsaR2']
    FOUNDER = row['cellValuesByColumnId']['fldbGZmPcgWw1UomW']['valuesByForeignRowId']['recNniOlJpoflM0L4']
    if FOUNDER is list and len(FOUNDER)>1:
        FOUNDER = ','.join(FOUNDER)
    WEBSITE = row['cellValuesByColumnId']['fldiL1KEOZO4MHcvW']['valuesByForeignRowId']['recNniOlJpoflM0L4']
    if WEBSITE is list and len(WEBSITE)>1:
        WEBSITE = ','.join(WEBSITE)
    TWITTER = row['cellValuesByColumnId']['fldfxvX3xyd1uBTM4']
    pass
    print()
# pageText = res.text
# title = re.compile("").findall(pageText)
