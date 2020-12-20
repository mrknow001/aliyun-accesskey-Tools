import time

from PyQt5.QtCore import Qt, QThread
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic.properties import QtWidgets
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526.CreateCommandRequest import CreateCommandRequest
from aliyunsdkecs.request.v20140526.InvokeCommandRequest import InvokeCommandRequest
from aliyunsdkecs.request.v20140526.DescribeSecurityGroupAttributeRequest import DescribeSecurityGroupAttributeRequest
import json, base64, random
import OSSTools


def info_message(ui):
    print('msg')
    QtWidgets.QMessageBox.information(ui.pushButton, "提示", 'msg')

def err_message(ui):
    print('msg')
    QtWidgets.QMessageBox.critical(ui.pushButton, "警告", 'msg')


def CreateCommand(ui, AccessKeyID, AccessKeySecret, com_type, command, ZoneId):
    client = AcsClient(AccessKeyID, AccessKeySecret, ZoneId)

    request = CreateCommandRequest()
    request.set_accept_format('json')
    name = ''.join(random.sample(
        ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e',
         'd', 'c', 'b', 'a'], 5))
    # name = 'test11111'
    try:
        request.set_Name(name)
        request.set_Type(com_type)
        command = base64.b64encode(command.encode()).decode()

        request.set_CommandContent(command)

        response = client.do_action_with_exception(request)
        # python2:  print(response)
        # print(str(response, encoding='utf-8'))
        return json.loads(response, encoding='utf-8')['CommandId']
    except:
        print('命令创建失败')
        OSSTools.show_message(ui,'命令创建失败')


def InvokeCommand(ui, AccessKeyID, AccessKeySecret, ZoneId, InstanceId, CommandId):
    client = AcsClient(AccessKeyID, AccessKeySecret, ZoneId)

    try:
        request = InvokeCommandRequest()
        request.set_accept_format('json')

        request.set_CommandId(CommandId)
        request.set_InstanceIds([InstanceId])

        response = client.do_action_with_exception(request)
        # python2:  print(response)
        # print(str(response, encoding='utf-8'))
        if json.loads(response)['InvokeId'] == '':
            print('命令执行错误')
            OSSTools.show_message(ui, '命令执行错误')
        else:
            print('命令执行完成')
            OSSTools.show_message(ui, '命令执行完成')
        # return str(response)
    except:
        print('命令执行失败')
        OSSTools.show_message(ui, '命令执行失败')


def DescribeSecurityGroupAttribute(ui, AccessKeyID, AccessKeySecret, ZoneId, SecurityGroupId):
    client = AcsClient(AccessKeyID, AccessKeySecret, ZoneId)

    try:
        request = DescribeSecurityGroupAttributeRequest()
        request.set_accept_format('json')

        request.set_SecurityGroupId(SecurityGroupId)

        response = client.do_action_with_exception(request)
        item = ui.listWidget.item(1)
        item.setText("1111111111111")
    except:
        print('请输入正确参数')
        OSSTools.show_message(ui, '请输入正确参数')
        return
    # python2:  print(response)
    print(str(response, encoding='utf-8'))


def DescribeInstances(ui, AccessKeyID, AccessKeySecret):
    ui.pushButton.setEnabled(False)
    ui.pushButton.setText('正在查询')
    RegionIds = {"cn-hangzhou": "华东1（杭州）", "cn-chengdu": "成都", "cn-qingdao": "华北1（青岛）", "cn-beijing": "华北2（北京）",
                 "cn-huhehaote": "华北5（呼和浩特）", "cn-shanghai": "华东2（上海）",
                 "cn-shenzhen": "华南1（深圳）", "cn-zhangjiakou": "华北3（张家口）",
                 "cn-hongkong": "香港", "ap-southeast-1": "新加坡", "ap-southeast-2": "澳大利亚（悉尼）",
                 "ap-southeast-3": "马来西亚（吉隆坡）",
                 "ap-southeast-5": "印度尼西亚（雅加达）", "ap-northeast-1": "日本（东京）", "us-west-1": "美国（硅谷）",
                 "us-east-1": "美国（弗吉尼亚）",
                 "eu-central-1": "德国（法兰克福）", "me-east-1": "阿联酋（迪拜）", "ap-south-1": "印度（孟买）", "eu-west-1": "英国（伦敦）",
                 "cn-shenzhen-finance-1": "深圳金融云", "cn-shanghai-finance-1": "上海金融云",
                 "cn-north-2-gov-1": "华北 2 阿里政务云1", "cn-heyuan": "华南2（河源）"}
    for RegionId in RegionIds:
        client = AcsClient(AccessKeyID, AccessKeySecret, RegionId)
        # print(RegionId)

        try:
            request = DescribeInstancesRequest()
            request.set_accept_format('json')

            response = client.do_action_with_exception(request)
        except:
            #print('请检查输入Key与Secret值,或重新执行')
            ui.pushButton.setText('查询')
            ui.pushButton.setEnabled(True)
            return ui, '请检查输入Key与Secret值,或重新执行'
        if json.loads(response)['TotalCount'] == 0:
            #print(RegionId)
            if RegionId == 'cn-heyuan':
                ui.pushButton.setText('查询')
                ui.pushButton.setEnabled(True)
                return ui,'查询完成'
            else:

                continue
        # python2:  print(response)
        # print(str(response, encoding='utf-8'))
        # item1 = json.loads(response)['Instances']['Instance'][0]['OSName']
        PrivateIps = ''
        PublicIps = ''

        for i in range(json.loads(response)['TotalCount']):

            row_cnt = ui.tableWidget.rowCount()  # 读取列
            ui.tableWidget.insertRow(row_cnt)  # 创建列
            # print(json.loads(response)['Instances']['Instance'][i]['VpcAttributes']['PrivateIpAddress']['IpAddress'])
            for PrivateIp in json.loads(response)['Instances']['Instance'][i]['VpcAttributes']['PrivateIpAddress'][
                'IpAddress']:
                PrivateIps = str(PrivateIp) + ';'
                # print(PrivateIps)
            for PublicIp in json.loads(response)['Instances']['Instance'][i]['PublicIpAddress']['IpAddress']:
                PublicIps = str(PublicIp) + ';'
                # print(PrivateIps)
            for SecurityGroup in json.loads(response)['Instances']['Instance'][i]['SecurityGroupIds'][
                'SecurityGroupId']:
                SecurityGroups = str(SecurityGroup) + ';'
                # print(PrivateIps)

            InstanceId = QTableWidgetItem(json.loads(response)['Instances']['Instance'][i]['InstanceId'])
            RegionId = QTableWidgetItem(RegionIds[json.loads(response)['Instances']['Instance'][i]['RegionId']])
            HostName = QTableWidgetItem(json.loads(response)['Instances']['Instance'][i]['HostName'])
            OSName = QTableWidgetItem(json.loads(response)['Instances']['Instance'][i]['OSName'])
            InstanceNetworkType = QTableWidgetItem(json.loads(response)['Instances']['Instance'][i]['Status'])
            PrivateIpAddress = QTableWidgetItem(PrivateIps)
            PublicIpAddress = QTableWidgetItem(PublicIps)
            SecurityGroupIds = QTableWidgetItem(SecurityGroup)
            yunzhushou = QTableWidgetItem('未知')
            performance = QTableWidgetItem(
                str(json.loads(response)['Instances']['Instance'][i]['Cpu']) + '核处理器\n' + str(
                    json.loads(response)['Instances']['Instance'][0]['Memory']) + 'MB内存')
            CreationTime = QTableWidgetItem(json.loads(response)['Instances']['Instance'][i]['CreationTime'])
            ExpiredTime = QTableWidgetItem(json.loads(response)['Instances']['Instance'][i]['ExpiredTime'])

            ui.tableWidget.setItem(row_cnt, 0, InstanceId)
            ui.tableWidget.setItem(row_cnt, 1, RegionId)
            ui.tableWidget.setItem(row_cnt, 2, HostName)
            ui.tableWidget.setItem(row_cnt, 3, OSName)
            ui.tableWidget.setItem(row_cnt, 4, InstanceNetworkType)
            ui.tableWidget.setItem(row_cnt, 5, PrivateIpAddress)
            ui.tableWidget.setItem(row_cnt, 6, PublicIpAddress)
            ui.tableWidget.setItem(row_cnt, 7, SecurityGroupIds)
            ui.tableWidget.setItem(row_cnt, 8, yunzhushou)
            ui.tableWidget.setItem(row_cnt, 9, performance)
            ui.tableWidget.setItem(row_cnt, 10, CreationTime)
            ui.tableWidget.setItem(row_cnt, 11, ExpiredTime)
    ui.pushButton.setText('查询')
    ui.pushButton.setEnabled(True)
    return ui,'查询完成'


def DescribeSecurityGroupAttribute(ui, AccessKeyID, AccessKeySecret, ZoneId, SecurityGroupId):
    # print(AccessKeyID, AccessKeySecret, ZoneId, SecurityGroupId)
    client = AcsClient(AccessKeyID, AccessKeySecret, ZoneId)

    request = DescribeSecurityGroupAttributeRequest()
    request.set_accept_format('json')

    request.set_SecurityGroupId(SecurityGroupId)

    response = client.do_action_with_exception(request)
    # python2:  print(response)
    print(str(response, encoding='utf-8'))


def server_check_input(ui):
    AccessKeyID = ui.lineEdit.text()
    AccessKeySecret = ui.lineEdit_2.text()

    for rowNum in range(0, ui.tableWidget.rowCount())[::-1]:
        ui.tableWidget.removeRow(rowNum)

    for rowNum in range(0, ui.tableWidget.rowCount())[::-1]:
        ui.tableWidget.removeRow(rowNum)

    if AccessKeyID == '':
        #OSSTools.err_message(ui,'请输入AccessKeyID')
        #print('请输入AccessKeyID')
        return ui,'请输入AccessKeyID'
    elif AccessKeySecret == '':
        #print('请输入AccessKeySecret')
        return ui,'请输入AccessKeySecret'
    else:
        # RegionIds = {"cn-hangzhou": "华东1（杭州）"}

        return DescribeInstances(ui, AccessKeyID, AccessKeySecret)



def commad_check_input(ui):
    RegionIds = {'华东1（杭州）': 'cn-hangzhou', '成都': 'cn-chengdu', '华北1（青岛）': 'cn-qingdao', '华北2（北京）': 'cn-beijing',
                 '华北5（呼和浩特）': 'cn-huhehaote', '华东2（上海）': 'cn-shanghai', '华南1（深圳）': 'cn-shenzhen',
                 '华北3（张家口）': 'cn-zhangjiakou', '香港': 'cn-hongkong', '新加坡': 'ap-southeast-1',
                 '澳大利亚（悉尼）': 'ap-southeast-2', '马来西亚（吉隆坡）': 'ap-southeast-3', '印度尼西亚（雅加达）': 'ap-southeast-5',
                 '日本（东京）': 'ap-northeast-1', '美国（硅谷）': 'us-west-1', '美国（弗吉尼亚）': 'us-east-1', '德国（法兰克福）': 'eu-central-1',
                 '阿联酋（迪拜）': 'me-east-1', '印度（孟买）': 'ap-south-1', '英国（伦敦）': 'eu-west-1',
                 '深圳金融云': 'cn-shenzhen-finance-1', '上海金融云': 'cn-shanghai-finance-1', '华北 2 阿里政务云1': 'cn-north-2-gov-1',
                 '华南2（河源）': 'cn-heyuan'}
    AccessKeyID = ui.lineEdit.text()
    AccessKeySecret = ui.lineEdit_2.text()
    try:
        InstanceId_row = ui.tableWidget.selectedItems()[0].row()
        InstanceId = ui.tableWidget.item(InstanceId_row, 0).text()
    except:
        InstanceId = ui.lineEdit_3.text()

    com_type = ui.comboBox.currentIndex()
    command = ui.lineEdit_4.text()

    if com_type == 0:
        com_type = 'RunShellScript'
    elif com_type == 1:
        com_type = 'RunBatScript'
    elif com_type == 2:
        com_type = 'RunPowerShellScript'
    elif com_type == 3:
        com_type = 'RunShellScript'

    if AccessKeyID == '':
        print('请输入AccessKeyID')
        OSSTools.show_message(ui,'请输入AccessKeyID')
        return
    elif AccessKeySecret == '':
        print('请输入AccessKeySecret')
        OSSTools.show_message(ui, '请输入AccessKeySecret')
        return
    elif InstanceId == '':
        print('请输入实例ID,或者选中实例ID')
        OSSTools.show_message(ui, '请输入实例ID,或者选中实例ID')
        return
    elif command == '':
        print('请输入执行命令')
        OSSTools.show_message(ui, '请输入执行命令')
        return
    else:
        try:
            item = ui.tableWidget.findItems(InstanceId, Qt.MatchExactly)
            row = item[0].row()
            ZoneId = RegionIds[ui.tableWidget.item(row, 1).text()]
        except:
            print('未获取到区域ID，请先获取实例信息，或者输入正确实例ID')
            OSSTools.show_message(ui, '未获取到区域ID，请先获取实例信息，或者输入正确实例ID')
            return
            # CreateCommand(ui,AccessKeyID,AccessKeySecret,InstanceId,com_type,command,'cn-hangzhou')

        # ui.lineEdit_3.setText(ui.TableWidget.selectedItems()[0].text())
        # print(AccessKeyID,AccessKeySecret,com_type,command,ZoneId)
        command_ID = CreateCommand(ui, AccessKeyID, AccessKeySecret, com_type, command, ZoneId)
        a = InvokeCommand(ui, AccessKeyID, AccessKeySecret, ZoneId, InstanceId, command_ID)
        # print(a)

        # DescribeInstances(ui,AccessKeyID,AccessKeySecret,'cn-hangzhou')


def SecurityGroup_check(ui):
    AccessKeyID = ui.lineEdit.text()
    AccessKeySecret = ui.lineEdit_2.text()

    try:
        SecurityGroup_row = ui.tableWidget.selectedItems()[0].row()
        SecurityGroupId = ui.tableWidget.item(SecurityGroup_row, 7).text()
    except:
        SecurityGroupId = ui.lineEdit_3.text()
    if AccessKeyID == '':
        print('请输入AccessKeyID')
        return
    elif AccessKeySecret == '':
        print('请输入AccessKeySecret')
        return
    elif SecurityGroupId == '':
        print('请输入安全组ID,或者选中安全组ID')
    else:
        item = ui.tableWidget.findItems(SecurityGroupId, Qt.MatchExactly)
        row = item[0].row()
        ZoneId = ui.tableWidget.item(row, 1).text()
        # SecurityGroup = ui.tableWidget.item(SecurityGroup_row, 7).text()

        DescribeSecurityGroupAttribute(ui, AccessKeyID, AccessKeySecret, ZoneId, SecurityGroupId)
