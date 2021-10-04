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
    paramsSummary = {'firstModuleId': firstModuleId, 'page': page, 'secondaryModuleId': secondaryModuleId, 'size': 150, 'screening': None}
    resp = requests.get(summaryListUrl, paramsSummary)
    data = resp.json()
    visionProductConfig = data['data']['VisionProductConfig'] # list, len = 29
    visionProductContent = data['data']['VisionProductContent']['records'] # list, len = 29
    # make sure that the title list and the data have the same dimension
    # titleList = ['id', 'productModel', 'productIntroduction', 'Sensor', 'Resolution', 'Max. frame rate', 'Data Interface', 'Mono/Color'] #CS, CA, CE,CH, CB, GL
    # titleList = ['id', 'productModel', 'productIntroduction', 'Resolution', 'Max. Line Rate', 'Data Interface', 'Mono/Color'] #CL
    # titleList = ['id', 'productModel', 'productIntroduction', 'Focal Length', 'F-Number', 'Image Size', 'Mount'] #Lens FA
    # titleList = ['id', 'productModel', 'productIntroduction', 'Magnification', 'Working Distance', 'Image Size', 'Mount'] #Telecentric lens 远心镜头
    # titleList = ['id', 'productModel', 'Type', 'Interface 1', 'Interface 2', 'Length'] #IO Cable, Power     ###################  3->2
    titleList = ['id', 'productModel', 'productIntroduction', 'Resolution', 'Max. Frame Rate', 'Mono/Color', 'Lens focal length'] #samrt camera 2k,3k,7k
    # titleList = ['id', 'productModel', 'productIntroduction', 'Sensor', 'Max. Frame Rate', 'Resolution', 'Data Interface', 'Mono/Color']  # samrt camera op
    # titleList = ['id', 'productModel', 'productIntroduction', 'Resolution', 'Focal length', 'Max. reading speed', 'Max. frame rate'] #ID2000, 3000

    dataList = []
    for i, productConfig in enumerate(visionProductConfig):
        dataDict = {}
        for j in range(len(titleList)):
            if j < 3:
                if titleList[j] == 'productIntroduction':
                # if titleList[j] == 'type': #IO Cable, Power
                    dataDict[titleList[j]] = replaceLineTerminator(visionProductContent[i][titleList[j]], '\n')
                else:
                    dataDict[titleList[j]] = visionProductContent[i][titleList[j]]
            else:
                dataDict[titleList[j]] = productConfig[j - 3]
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
    # titleList = ['Product Model', 'Model', 'Type', 'Resolution', 'Data Interface', 'Mono/Color', 'Digital I/O', 'Power supply', 'Lens mount', 'Dimension', 'Weight', 'Temperature', 'Humidity', 'Client software', 'Certification',
    #              'Sensor', 'Sensor type', 'Pixel size', 'Sensor size', 'Dynamic range', 'SNR', 'Gain', 'Exposure time', 'Pixel format', 'Image buffer', 'Power consumption', 'Ingress protection', 'Compatibility',
    #              'Operating system', 'Max. Line Rate', 'External trigger mode', 'Synchronization trigger mode']
                 # 'Max. Frame Rate', 'Shutter mode', 'Binning', 'Decimation', 'Reverse image'] as
                 # 'Max. Line Rate', 'External trigger mode', 'Synchronization trigger mode'] ls
    # titleList = ['Product Model', 'Model', 'Type', 'Focal Length', 'F-Number', 'Image Size', 'Distortion', 'Minimum Operation Distance', 'Field of View', 'Magnification Range', 'Iris Control', 'Focus Control',
    #              'Mount', 'Flange Back Length', 'Dimension', 'Weight', 'Temperature', 'Certification'] # FA lens
    # titleList = ['Model', 'Type', 'Magnification', 'Working Distance', 'F-Number', 'Image Size', 'Optical Distortion', 'Depth of Field', 'Resolution', 'Telecentricity', 'Object Space NA',
    #              'Object Field of View', 'Field of View', 'Mount', 'Object-image Distance', 'Dimension', 'Weight', 'Temperature', 'Certification'] #HT Lens

    # titleList = ['Model', 'Symbologies', 'Max. frame rate', 'Max. reading speed', 'Sensor type', 'Pixel size', 	'Sensor size', 'Resolution', 'Exposure time', 'Gain', 'Mono/color', 'Communication protocol',
    #              'Focal length', 'Working distance', 'Ambient illumination', 'Light source', 'Aiming system', 'Data interface', 'Digital I/O', 'Power supply', 'Max. power consumption', 'Indicator', 'Dimension',
    #              'Weight', 'Ingress protection', 'Temperature', 'Humidity', 'Client software', 'Certification'] #id2000

    # titleList = ['Name', 'Type', 'Symbologies', 'Max. frame rate', 'Max. reading speed', 'Sensor type', 'Pixel size', 	'Sensor size', 'Resolution', 'Exposure time', 'Gain', 'Mono/color', 'Communication protocol',
    #              'Data interface', 'Digital I/O', 'Power supply', 'Max. power consumption', 'Lens Focal Length', 'Lens mount', 'Lens cap', 'Light source', 'Indicator', 'Dimension',
    #              'Weight', 'Ingress protection', 'Temperature', 'Humidity', 'Client software', 'Certification'] #id3000

    # samrt camera 2k,3k,7k #2k Certifications
    titleList = ['Model', 'Type', 'Vision tools', 'Solution capacity', 'Communication protocol', 'Sensor type', 'Pixel size', 'Sensor size', 'Resolution', 'Max. Frame Rate', 'Dynamic range',
                 'SNR', 'Gain', 'Exposure time', 'Pixel format', 'Exposure time', 'Mono/Color', 'Memory', 'Storage', 'Interface', 'Ethernet', 'Digital I/O', 'Power supply', 'Power consumption', 'Lens mount',
                 'Lens focal length', 'Lens cap', 'Lighting', 'Indicator', 'Dimension', 'Weight', 'Ingress protection', 'Temperature', 'Humidity', 'Operating method', 'Certifications'] #samrt camera

    # # samrt camera op
    # titleList = ['Model', 'Type', 'Function module', 'Sensor type', 'Sensor'
    #              'Pixel size', 'Sensor size', 'Resolution', 'Max. Frame Rate', 'Dynamic range',
    #              'SNR', 'Gain', 'Exposure time', 'Pixel format', 'Exposure time', 'Mono/Color', 'System framework', 'Operating system', 'Memory', 'Storage',
    #              'Data Interface', 'Digital I/O', 'Extended interface', 'Power supply', 'Power consumption', 'Lens mount', 'Lens cap', 'Lighting',
    #              'Indicator', 'Dimension', 'Weight', 'Ingress protection', 'Temperature', 'Humidity', 'Operating method', 'Certifications']  # samrt camera op

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
        with open('C:\\Users\\Pandafan\\Dropbox\\sogoo\\Hik\\' + filePattern + '.csv', mode='w', encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter='#', quotechar="'", lineterminator='\n')
            csv_writer.writerow(titles)
            for index, data in enumerate(dataList):
                csv_writer.writerow(list(data.values()))
    else:
        for index, data in enumerate(dataList):
            with open('C:\\Users\\Pandafan\\Dropbox\\sogoo\\Hik\\' + str(index) + '-' + filePattern + '.csv', mode='w') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", lineterminator='\n')
                csv_writer.writerow(titles)
                csv_writer.writerow(list(data.values()))



# ID2000: 111,158; ID3000: 111,112;
# CS: 78,134; CE: 78,42; CA: 78,43; CH: 78,44; GL: 78,116; CB: 78,80; CL: 146,155
# Lens: FA Lens: 40,49; MVL-HT: 40,50
# power,IO cable: 143,148
# sc2k: 38,121; sc3k: 38,159; sc7k: 38,162; scop: 38,47
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    productSummary = getSummaryData(38, 121, 1)
    getDetailedData(productSummary)