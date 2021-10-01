#####################
#### This script sends HTTP calls to fetch the data from websites and parses the data as JSON objects
#### Copyright: SoGoo International GmbH
#####################

import requests
import csv

baseUrl = 'https://www.hikrobotics.com'
summaryListUrl = baseUrl + '/en/Api/Foreground/Vision/VisionProductContent?'
detailUrl = baseUrl + '/en/Api/Foreground/Vision/VisionProductConfig?'
introductionUrl = baseUrl + '/en/Api/Foreground/Vision/VisionProductIntroduction?'


def getSummaryData(firstModuleId, secondaryModuleId, page): # 1 file, 29 lines
    paramsSummary = {'firstModuleId': firstModuleId, 'page': page, 'secondaryModuleId': secondaryModuleId, 'size': 100, 'screening': None}
    resp = requests.get(summaryListUrl, paramsSummary)
    data = resp.json()
    visionProductConfig = data['data']['VisionProductConfig'] # list, len = 29
    visionProductContent = data['data']['VisionProductContent']['records'] # list, len = 29
    # make sure that the title list and the data have the same dimension
    titleList = ['id', 'productModel', 'productIntroduction', 'Sensor', 'Resolution', 'Max. frame rate',
                 'Data Interface', 'Mono/Color']  # CS, CA, CE, CB, GL
    # make sure that the title list and the data have the same dimension
    # titleList = ['id', 'productModel', 'productIntroduction', 'Sensor', 'Resolution', 'Max. frame rate', 'Data Interface', 'Mono/Color'] #CS, CA, CE,CH, CB, GL
    # titleList = ['id', 'productModel', 'productIntroduction', 'Resolution', 'Max. Line Rate', 'Data Interface', 'Mono/Color'] #CL
    # titleList = ['id', 'productModel', 'productIntroduction', 'Focal Length', 'F-Number', 'Image Size', 'Mount'] #Lens FA
    # titleList = ['id', 'productModel', 'productIntroduction', 'Magnification', 'Working Distance', 'Image Size', 'Mount'] #Telecentric lens 远心镜头
    # titleList = ['id', 'productModel', 'Type', 'Interface 1', 'Interface 2', 'Length'] #IO Cable, Power
    ###################  3->2
    dataList = []
    for i, productConfig in enumerate(visionProductConfig):
        dataDict = {}
        for j in range(len(titleList)):
            if j < 3:
                # delete return lines for introductions
                if titleList[j] == 'productIntroduction':
                    dataDict[titleList[j]] = replaceLineTerminator(visionProductContent[i][titleList[j]], '\n')
                else:
                    dataDict[titleList[j]] = visionProductContent[i][titleList[j]]
            else:
                dataDict[titleList[j]] = replaceLineTerminator(productConfig[j - 3], '\n')
        dataList.append(dataDict)
    print('Now exporting summary(table) data as CSV file')
    exportObjectAsCSV(titleList, dataList, 'Table', True)
    return visionProductContent

def replaceLineTerminator(orgString, terminator):
    return orgString.replace(terminator, ' ')

def getValueByName(data, name):
    for respLine in data:
        if respLine['name'] == name:
            return respLine['value']
    return 'null'


def getDetailedData(productSummary): # 29 files, each file has 33 columns -> each dict creates a file
    titleList = ['Product Model', 'Model', 'Type', 'Resolution', 'Data Interface', 'Mono/Color', 'Digital I/O', 'Power supply', 'Lens mount', 'Dimension', 'Weight', 'Temperature', 'Humidity', 'Client software', 'Certification',
                 'Sensor', 'Sensor type', 'Pixel size', 'Sensor size', 'Dynamic range', 'SNR', 'Gain', 'Exposure time', 'Pixel format', 'Image buffer', 'Power consumption', 'Ingress protection', 'Compatibility',
                 'Operating system', 'Max. Frame Rate', 'Shutter mode', 'Binning', 'Decimation', 'Reverse image']#, 'Max. Line Rate', 'External trigger mode', 'Synchronization trigger mode']
    dataList = []
    for productIdx, product in enumerate(productSummary):
        print('Now fetching detailed data, please wait. Progress: ', productIdx + 1, '/', len(productSummary))
        dataDict = {}
        paramsDetail = {'id': product['id']}
        respData = requests.get(detailUrl, paramsDetail).json()['data']
        for j in range(len(titleList)):
            dataDict[titleList[j]] = replaceLineTerminator(getValueByName(respData, titleList[j]), '\n')
        dataList.append(dataDict)
    print('Now exporting detailed data as CSV file')
    exportObjectAsCSV(titleList, dataList, 'Detail', True)
    print('Successfully fetched all Hikrobot data!')



def exportObjectAsCSV(titles, dataList, filePattern, onlyOneFile=False):
    """
    :param titles: List
    :param data:  List -> a dataList can have multiple dicts. Each dict generates a file
    """
    print('Now trying to dump CSV with the title', titles)
    if onlyOneFile:
        with open('c:\\hikdata\\' + filePattern + '.csv', mode='w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter='#', quotechar="'", lineterminator='\n')
            csv_writer.writerow(titles)
            for index, data in enumerate(dataList):
                csv_writer.writerow(list(data.values()))
    else:
        for index, data in enumerate(dataList):
            with open('c:\\hikdata\\' + str(index) + '-' + filePattern + '.csv', mode='w') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter='#', quotechar="'", lineterminator='\n')
                csv_writer.writerow(titles)
                csv_writer.writerow(list(data.values()))


# Press the green button in the gutter to run the script.
# ID2000: 111,158; ID3000: 111,112;
# CS: 78,134; CE: 78,42; CA: 78,43; CH: 78,44; GL: 78,116; CB: 78,80; CL: 146,155
# Lens: FA Lens: 40,49; MVL-HT: 40,50
# power,IO cable: 143,148
if __name__ == '__main__':
    productSummary = getSummaryData(78, 134, 1)
    getDetailedData(productSummary)
