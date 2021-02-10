# -*- coding: utf-8 -*-

import losteering_process as lp
import sporteering_login as login
from upload_gdrive import upload_file


df = lp.fetch_datafile(login.username, login.password)

csv_filename = 'LOSTeering Ete 2020.csv'
csv_file = open(csv_filename, 'w') 

csv_file.write('LOSTeering ETE 2020\n')

event_name = 'LOSTeering 2020 - Eté - Découverte des parcs de Lauzelle (Moyen)'
event_controls = [109, 110, 102, 103, 112, 113, 115, 116, 117, 118, 119, 107, 108]
lp.classify(df, event_name, event_controls, csv_file)

event_name = 'LOSTeering 2020 - Eté - Découverte des parcs des Bruyères (Long)'
event_controls = [120, 121, 122, 123, 124, 125, 126, 127, 134, 128, 129, 130, 131, 132, 133, 111]
lp.classify(df, event_name, event_controls, csv_file)

event_name = "LOSTeering 2020 - Eté - D'un musée à l'autre (Court)"
event_controls = [108, 107, 106, 104, 102, 101, 120, 111]
lp.classify(df, event_name, event_controls, csv_file)


event_name = "LOSTeering 2020 - Eté - Chasse aux postes Lauzelle"
event_controls = [101, 109, 111, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134]
lp.classify(df, event_name, event_controls, csv_file, chasse=True)


event_name = "LOSTeering 2020 - Eté - Chasse aux postes Bruyères"
event_controls = [101, 109, 111, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134]
lp.classify(df, event_name, event_controls, csv_file, chasse=True)

csv_file.close()


#upload_file(csv_filename, csv_filename)