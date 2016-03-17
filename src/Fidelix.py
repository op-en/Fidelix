# coding: utf-8
import requests
import json
import paho.mqtt.publish as publish
import urllib
import re

class Fidelix():

    session_id = None
    verbose = False
    stem = ""

    def login(self, user = "user", password = "pass"):

        data = 'Login=&UserName=%s&PassWord=%s' % (user, password)

        #Set header
        headers={
            "Origin": "http://bergen1ec.dyndns.org:81",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer":"http://bergen1ec.dyndns.org:81/Report?File=Fx2020Main.htm",
        }

        url = "http://bergen1ec.dyndns.org:81/Report"

        #Request password cookie
        r = requests.post(url,data=data,headers=headers,allow_redirects=False)

        regexp = re.search('parent.document.cookie=\'UserID=(.*)\'', r.text)
        data = regexp.group(1)

        print('type=info msg="login successfull" session_id=' + data)

        self.session_id = data

    #Login
    def read_value(self):

        #Set header
        headers={"Referer":"http://bergen1ec.dyndns.org:81/Report?File=Fx2020.htm", "user-agent": "curl/7.43.0","Accept-Encoding": "gzip, deflate, sdch"}
        cookies = {"UserID": self.session_id}

        # Request all values
        url = "http://bergen1ec.dyndns.org:81/Report?XML&GET&PointList&LIST92879685&ActivePicture=ENERGI_AS01.htm&ID97893=AS01_KB01_EM11_F_TEMP_MV,0&ID36231=AS01_KB01_EM11_R_TEMP_MV,0&ID55871=AS01_KB01_EM11_ENERGI_MV,0&ID69301=AS01_KB01_EM11_EFFEKT_MV,0&ID79613=AS01_KB01_EM11_FLODE_MV,0&ID98525=AS01_VS01_EM11_ENERGI_MV,0&ID90458=AS01_VS01_EM11_EFFEKT_MV,0&ID14973=AS01_VS01_EM11_FLODE_MV,0&ID55910=AS01_VS01_EM11_F_TEMP_MV,0&ID63580=AS01_VS01_EM11_R_TEMP_MV,0&ID63899=AS01_VS01_EM12_ENERGI_MV,0&ID21759=AS01_VS01_EM12_EFFEKT_MV,0&ID40668=AS01_VS01_EM12_FLODE_MV,0&ID13389=AS01_VS01_EM12_F_TEMP_MV,0&ID25325=AS01_VS01_EM12_R_TEMP_MV,0&ID66187=AS01_VS01_EM13_ENERGI_MV,0&ID96968=AS01_VS01_EM13_EFFEKT_MV,0&ID88509=AS01_VS01_EM13_FLODE_MV,0&ID4399=AS01_VS01_EM13_F_TEMP_MV,0&ID7679=AS01_VS01_EM13_R_TEMP_MV,0&ID73501=AS01_VS01_EM14_ENERGI_MV,0&ID41313=AS01_VS01_EM14_EFFEKT_MV,0&ID44163=AS01_VS01_EM14_FLODE_MV,0&ID46265=AS01_VS01_EM14_F_TEMP_MV,0&ID3346=AS01_VS01_EM14_R_TEMP_MV,0&ID18304=AS01_VS02_EM11_EFFEKT_MV,0&ID27118=AS01_VS02_EM11_FLODE_MV,0&ID20902=AS01_GT31_MV,0&ID48190=AS01_SOMMAR_VINTER_I,0&ID51122=AS01_STALLV_ENERGI_MV,0&ID14470=AS01_STALLV_EFFEKT_MV,0&ID69486=AS01_VV01_VM31_FLODE_MV,0&ID58085=AS01_VV01_VM31_VOL_MV,0&ID32621=AS01_VS02_EM11_ENERGI_MV,0&ID37725=AS01_VS01_EM15_ENERGI_MV,0&ID13536=AS01_VS01_EM15_EFFEKT_MV,0&ID88384=AS01_VS01_EM15_FLODE_MV,0&ID99093=AS01_VS01_EM15_F_TEMP_MV,0&ID92607=AS01_VS01_EM15_R_TEMP_MV,0&ID7109=AS01_VMP1_ENERGI_MV,0&ID81934=AS01_VMP2_ENERGI_MV,0&ID40790=AS01_VMP1_EFFEKT_MV,0&ID6361=AS01_VMP2_EFFEKT_MV,0&ID64224=AS01_VMP1_EM_KL,0&ID79231=AS01_VMP2_EM_KL,0&ID41922=AS01_VS02_EM11_F_TEMP_MV,0&ID54086=AS01_VS02_EM11_R_TEMP_MV,0&ID84422=AS01_VS01_EM11_KL,0&ID83846=AS01_VS01_EM12_KL,0&ID19328=AS01_VS01_EM13_KL,0&ID9042=AS01_VS01_EM14_KL,0&ID82879=AS01_VS01_EM15_KL,0&ID72020=AS01_VS02_EM11_KL,0&ID44454=AS01_VV01_VM31_KL,0&ID10990=AS01_STALLV_EM_KL,0&"

        r = requests.get(url,cookies=cookies,headers=headers,allow_redirects=False)

        # Decode the weird windows encoding
        decode = urllib.unquote(r.content).decode('windows-1252')

        # Get rid of the dummy xml tags
        regexp = re.search('<data>(.*)</data>', decode)
        data = regexp.group(1)

        # Clean some formatting
        data = data.split('EOP#')

        # Specify and try to find the messages that we want
        general_prefix = "AS01"

        energy_point_type = ['ENERGI_MV','FLODE_MV','EFFEKT_MV','F_TEMP_MV','R_TEMP_MV']
        water_point_type = ['VOL_MV','FLODE_MV']

        requested_datapoint = {
            "KB01_EM11": energy_point_type,
            "VS01_EM11": energy_point_type,
            "VS01_EM12": energy_point_type,
            "VS01_EM13": energy_point_type,
            "VS01_EM14": energy_point_type,
            "VS01_EM15": energy_point_type,
            "VS01_EM16": energy_point_type,
            "VS02_EM11": energy_point_type,
            "VV01_VM31": water_point_type
        }

        # Requested points
        requested_points = []
        for pointname,pointtypes in requested_datapoint.iteritems():
            for types in pointtypes:
                requested_points.append("%s_%s_%s" % (general_prefix,pointname,types))


        # Create index tag from id to datapoint
        tagname_datapoint = {}
        for point in requested_points:
            try:
                regexp = re.search('\d+(?=\=' + point + ')', url) #Find the tag id in the url by using regex lookahead
                tagid = regexp.group()
                tagname_datapoint[tagid] = point
            except:
                # print "Tag not found in data, skipping " + point
                continue;



        # Parse the actual data to get the values
        point_value = []
        for point in data:
            try:
                # print point
                # Find the tagname and match it to the desired data name
                regexp = re.search('tagname#ID(.*?)#', point)
                tagname = regexp.group(1)

                # print tagname
                data_name = tagname_datapoint[tagname]

                # Find value
                regexp = re.search('(?<=dynamic\#3\$)(.*?)\$', point)
                value = regexp.group()[:-1] #get the first group, and strip the last $ that we use to match

                point_value.append([data_name,value])
            except:#If we get an error, just skip this tag
                continue



        # Now that we have all the values, package it as mqtt packets

        packages = {}
        for pair in point_value:
            data_name = pair[0]
            value = pair[1]

            name_pieces = data_name.split('_')
            package_name = "%s_%s" % (name_pieces[1], name_pieces[2])

            package = {}
            if(packages.has_key(package_name)):
                package = packages[package_name]

            point_name = "_".join(name_pieces[3:-1])

            package[point_name] = value
            packages[package_name] = package


        messages = []
        for topic,payload in packages.iteritems():
            message = {'topic': self.stem + topic, 'payload': json.dumps(payload)}
            if self.verbose:
                print message
            messages.append(message)

        # print messages
        if len(messages) > 0:
            publish.multiple(messages, hostname=self.host)
            print('type=info msg="published messages" count=' + str(len(messages)))
        else:
            print('type=info msg="no messages published"')
