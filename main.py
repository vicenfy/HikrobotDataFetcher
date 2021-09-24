#####################
#### This script sends HTTP calls to fetch the data from websites and parses the data as JSON objects
#### Copyright: SoGoo International GmbH
#####################

import requests

baseUrl = 'https://www.hikrobotics.com'
summaryListUrl = baseUrl + '/en/Api/Foreground/Vision/VisionProductContent?'
detailUrl = baseUrl + '/en/Api/Foreground/Vision/VisionProductConfig?'


def getSummaryData(): # 1 file, 29 lines
    paramsSummary = {'firstModuleId': 78, 'page': 1, 'secondaryModuleId': 42, 'size': 100, 'screening': None}
    resp = requests.get(summaryListUrl, paramsSummary)
    data = resp.json()
    visionProductConfig = data['data']['VisionProductConfig'] # list, len = 29
    visionProductContent = data['data']['VisionProductContent']['records'] # list, len = 29
    # make sure that the title list and the data have the same dimension
    titleList = ['id', 'productModel', 'Sensor', 'Resolution', 'Max. Frame Rate', 'Data Interface', 'Mono/Color']
    dataList = []
    for productConfig in visionProductConfig:
        dataDict = {}
        for i in range(len(productConfig)):
            if i < 2:
                dataDict[titleList[i]] = visionProductContent[i][titleList[i]]
            else:
                dataDict[titleList[i]] = productConfig[i - 2]
        dataList.append(dataDict)
    print('Now exporting summary(table) data as CSV file')
    exportObjectAsCSV(titleList, dataList)
    return visionProductContent


def getDetailedData(productSummary): # 29 files, each file has 33 lines -> each dict creates a file
    titleList = []
    dataList = []
    for productIdx, product in enumerate(productSummary):
        print('Now fetching detailed data, please wait. Progress: ', productIdx + 1, '/', len(productSummary))
        dataDict = {}
        paramsDetail = {'id': product['id']}
        respData = requests.get(detailUrl, paramsDetail).json()['data']
        if len(respData) > 0:
            titleList = list(respData[0].keys())
            for respLine in respData:
                dataDict[respLine['name']] = respLine['value']
            dataList.append(dataDict)
    print('Now exporting detailed data as CSV file')
    exportObjectAsCSV(titleList, dataList)
    print('Successfully fetched all Hikrobot data!')




def parseResponseAsJson():
    pass


def exportObjectAsCSV(titles, dataList):
    """
    :param titles: List
    :param data:  List -> a dataList can have multiple dicts. Each dict generates a file
    """
    print(titles)
    for index, data in enumerate(dataList):
        # To-Do: instead of printing, generate a CSV file for each dict in the list
        print('Line', index + 1, ':', data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    productSummary = getSummaryData()
    getDetailedData(productSummary)
