###############################################################
#
#   Author: Mohammed Almodawah
#   Date: 1/1/2020
#   Version: 1.0 pre-alpha
#
#   Description:
#   This library provides basic functions to
#   interact with PowerCute Business Edition v10.0.1
#   web interface.
#
#   Tested on pbeagent-10.0.1-301-EN.x86_64.rpm.
#   MD5: d4e2c32960d314037e2aa2d9b6bd81be
#
###############################################################

import requests
from bs4 import BeautifulSoup

class PowerChute:
    def __init__(self, server_ip, port, username, password):
        self.__server_ip = server_ip
        self.__port = port
        self.__username = username
        self.__password = password
        # disables TLS warnings. You should not disable tLS warnings in production environment
        requests.packages.urllib3.disable_warnings()

    # authenticates using username and password and sets the token cookie
    def __auth(self):
        logon_page = "https://"+self.__server_ip+":"+self.__port+"/logon"
        r = requests.get(url = logon_page, verify=False)
        cookie = r.headers['Set-Cookie']
        formtoken = BeautifulSoup(r.content,"html.parser").find(id = "formtoken").get("value")
        auth_page = "https://"+self.__server_ip+":"+self.__port+"/j_security_check"
        PARAMS = {"j_username":self.__username, "j_password":self.__password, "formtoken":formtoken, "formtokenid":"/logon_formtoken", "login":"Log On"}
        headers = {"Cookie":cookie}
        r = requests.post(url = auth_page, params = PARAMS,verify=False, headers=headers)
        self.__token = r.headers['Set-Cookie']

    # de-authenticates the token
    def __logoff(self):
        logoff_page = "https://"+self.__server_ip+":"+self.__port+"/logoff"
        headers = {"Cookie":self.__token}
        r = requests.get(url = logoff_page, verify=False, headers=headers)
    
    # status page contains all ups values
    def __get_status_page_content(self):
        self.__auth()
        status_page = "https://"+self.__server_ip+":"+self.__port+"/status"
        headers = {"Cookie":self.__token}
        r = requests.get(url = status_page, verify=False, headers=headers)
        self.__logoff()
        return str(r.content)

    # each ups value has an html id in the status page. you can use this function to get all available field names
    def get_all_html_fields_ids(self):
        content = self.__get_status_page_content()
        splits = content.split('"')
        fields = []
        for x in splits:
            if "value_" in x:
                fields.append(x)
        return fields
    # takes a field id and returns its value
    def get_field_by_html_id(self,id):
        content = self.__get_status_page_content()
        value = BeautifulSoup(content,"html.parser").find(id = id).contents[0]
        return value
        
    # returns the battery charge in percentage
    def get_battery_charge(self):
        value = self.get_field_by_html_id("value_BatteryCharge")
        return float(value)
    
    # returns the input voltage
    def get_input_voltage(self):
        value = self.get_field_by_html_id("value_InputVoltage")
        return float(value)
