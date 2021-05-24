from pyzabbix import ZabbixAPI
import logging
logging.basicConfig(filename="zabbix_api.log", level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())

zapi = ZabbixAPI(
    'https://zabbix-server-address/api_jsonrpc.php')
zapi.login('----', '----')

##### openscada brigades

brigades_array = [
    '22', '14', '43', '49', '13', '1', '2', '3', '4', '5', '7', '8', '9', '11',
    '12', '47'
]
brigadeName_prefix = "VB"

userList = [
    # ['Test1', 'Test1', 'test1-login', 'VB01'],
    # ['Test2', 'Test2', 'test2-login', 'VB02'],
]


# return Id for User group from Zabbix
def get_usergroup_id(_brigadeName):
    return zapi.usergroup.get(filter={'name': _brigadeName})[0]['usrgrpid']


# return Id for HOST group from Zabbix
def get_hostgroup_id(_brigadeName):
    return zapi.hostgroup.get(filter={'name': _brigadeName})[0]['groupid']


def user_group_create(_brigadeName):
    # get brigade host group id
    zhostGroupID = get_hostgroup_id(_brigadeName)
    # create user group with read permission to host group zhostGroupID
    resultRequest = zapi.usergroup.create(name=_brigadeName,
                                          rights=[{
                                              "permission": 2,
                                              "id": zhostGroupID
                                          }])
    logging.info("ADD USER GROUP: ---  " + _brigadeName)
    logging.info("id " + resultRequest['usrgrpids'][0])
    # print(resultRequest['groupids'][0])
    # return resultRequest['usrgrpids'][0]


def user_create(_user):
    brigadeName = _user[3]
    zuserGroupID = get_usergroup_id(brigadeName)
    userLogin = _user[2]
    userName = _user[1]
    userSurname = _user[0]
    userEmail = userLogin + '@mhp.com.ua'
    logging.info("ADD USER: ---  " + userLogin)

    resultRequest = zapi.user.create(
        name=userName,
        surname=userSurname,
        alias=userLogin,
        usrgrps=[{
            "usrgrpid": zuserGroupID
        }],
        user_medias=[{
            "mediatypeid": "1",
            "sendto": [userEmail],
            "active": 0,
            "severity": 56,  # bit mask for severity (000111)
            "period": "1-7,00:00-24:00"
        }])
    logging.info("id " + resultRequest['userids'][0])


# for brigade in brigades_array:
#     brigadeNumStr = (f"{int(brigade):02}") + ''
#     brigadeName = brigadeName_prefix + brigadeNumStr
#     try:
#         user_group_create(brigadeName)
#     except expression as identifier:
#         pass

for user in userList:
    try:
        user_create(user)
    except expression as identifier:
        pass

zapi.user.logout()
