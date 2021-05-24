from pyzabbix import ZabbixAPI
import logging
logging.basicConfig(filename="zabbix_api.log", level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())

zapi = ZabbixAPI(
    'https://zabbix-server-address/api_jsonrpc.php')
zapi.login('---', '---')
#const
##### brigades
# brigades_array = ['1','2', '3', '4', '5','6', '7', '8', '9', '11', '12','42', '47']

kur_houses_count = 9
brigadeName_prefix = "SP"


def brigade_create(_brigadeName):

    resultRequest = zapi.hostgroup.create(name=_brigadeName)
    logging.info("CREATING: ---  " + _brigadeName)
    logging.info("id " + resultRequest['groupids'][0])
    # print(resultRequest['groupids'][0])
    return resultRequest['groupids'][0]


def kurhouse_create(_brigadeNumStr, _kurhouseName, _kurhouseNumStr,
                    _zabbix_group_id):
    logging.info("ADD: ---  " + _kurhouseName)
    # create zabbix host
    #orel - 'groupid': '67', VB - 'groupid': '24'
    requestHostCreate = zapi.host.create(host=_kurhouseName,
                                         name=_kurhouseName,
                                         proxy_hostid='0',
                                         macros=[{
                                             'macro': '{$BRIGADE}',
                                             'value': _brigadeNumStr
                                         }, {
                                             'macro': '{$HOUSE}',
                                             'value': _kurhouseNumStr
                                         }, {
                                             'macro': '{$NAME}',
                                             'value': brigadeName_prefix
                                         }],
                                         interfaces=[{
                                             'main': '1',
                                             'type': '1',
                                             'useip': '0',
                                             'dns':
                                             'mhp-dwh.database.windows.net',
                                             'port': '10050',
                                             'bulk': '1',
                                             'ip': ''
                                         }],
                                         groups=[{
                                             'groupid': '67'
                                         }, {
                                             'groupid': '1'
                                         }, {
                                             'groupid': _zabbix_group_id
                                         }])
    # attach template "Poultry Growth Sensors" id 10320 to created host
    zapi.template.massadd(templates=[{
        "templateid": "10320"
    }],
                          hosts=[{
                              'hostid': requestHostCreate['hostids'][0]
                          }])


for brigade in brigades_array:
    brigadeNumStr = (f"{int(brigade):02}") + ''
    brigadeName = brigadeName_prefix + brigadeNumStr
    zabbix_group_id = brigade_create(brigadeName)
    for kur_house in range(1, kur_houses_count + 1):
        kurhouseNumStr = f"{int(kur_house):02}" + ''
        kurhouseName = brigadeName + kurhouseNumStr
        # print(kurhouseName)
        kurhouse_create(brigadeNumStr, kurhouseName, kurhouseNumStr,
                        zabbix_group_id)

zapi.user.logout()