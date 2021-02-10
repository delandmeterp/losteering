# -*- coding: utf-8 -*-

import losteering_process as lp
import sporteering_login as login
from upload_gdrive import upload_file


df = lp.fetch_datafile(login.username, login.password)

csv_filename = 'LOSTeering Winter 2021.csv'
csv_file = open(csv_filename, 'w') 

csv_file.write('LOSTeering Winter 2021\n')


event_name = "LOSTeering 2021 - Hiver - Court"
event_controls = list(range(101, 109))
lp.classify(df, event_name, event_controls, csv_file)


event_name = 'LOSTeering 2021 - Hiver - Moyen'
event_controls = [105, 109, 107, 111, 112, 113, 114, 115, 116, 102, 103, 117, 118]
lp.classify(df, event_name, event_controls, csv_file)

event_name = 'LOSTeering 2021 - Hiver - Long'
event_controls = [117, 118, 119, 120, 121, 122, 131, 123, 124, 125, 126, 127, 111, 113, 128, 129, 110, 106, 130]
lp.classify(df, event_name, event_controls, csv_file)

event_name = "LOSTeering 2021 - Hiver - Chasse aux postes Long"
event_controls = [104, 105, 106, 107, 108, 109, 110, 111, 113] + list(range(117, 132))
lp.classify(df, event_name, event_controls, csv_file, chasse=True)


event_name = "LOSTeering 2021 - Hiver - Chasse aux postes Centre"
event_controls = [101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 128, 129, 130]
lp.classify(df, event_name, event_controls, csv_file, chasse=True)

csv_file.close()


upload_file(csv_filename, csv_filename)