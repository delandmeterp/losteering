# -*- coding: utf-8 -*-

import losteering_process as lp
import sporteering_login as login
from upload_gdrive import upload_file
from write_xlsx import write_xlsx


df = lp.fetch_datafile(login.username, login.password)

basename = 'LOSTeering Winter 2021_results'
csv_file = open(basename + '.csv', 'w') 

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
write_xlsx(basename)


upload_file(basename + '.xlsx', basename + '.xlsx')