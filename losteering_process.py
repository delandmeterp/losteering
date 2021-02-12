# -*- coding: utf-8 -*-

import robobrowser
import numpy as np
import pandas as pd
import sporteering_login as login

def fetch_datafile(username, password):
    browser = robobrowser.RoboBrowser(parser='html.parser')
    browser.open('http://admin.sporteering.com/')
    login_form = browser.get_form(action='/Home/Login')
    login_form['username'] = username
    login_form['password'] = password
    browser.submit_form(login_form)

    form = browser.get_form(action='/Event/Create')

    p = form.submit_fields.getlist('submit')[1]
    browser.submit_form(form, submit=p)

    text_encoded = browser.response.content # bytes utf-8
    data = text_encoded.decode().split('\r\n')
    
    headers = data[0].split(',')
    ncols = len(headers)
        
    data_s = [[]] * (len(data)-2)
    for i in range(1, len(data)-1):
        line = data[i].split(',')
        for ii, item in enumerate(line):
            if item[0] == '"':
                line[ii] = line[ii] + line[ii+1]
                line.pop(ii+1)
        data_s[i-1] = line
        assert len(line) == ncols
    
    ndata = len(data_s)
    
    d = {}
    for i, h in enumerate(headers):
        d[h] = [data_s[idata][i] for idata in range(ndata)]
    
    return pd.DataFrame(data=d)

def test_seq(dfu, event_controls, seq_controls, u, times_OK, times_KO, ncontrols, logs, tstart, tend):
    correct = True
    ucontrol = np.array([int(uc) for uc in seq_controls])
    order = -1
    ncontrols[u] = 0
    for ic, ec in enumerate(event_controls):
        found = np.where(ucontrol==ec)[0]
        if len(found) == 0:
            correct = False
            logs[u] = ("%de balise (%d) non trouvée" % (ic+1, ec))
            break
        found = found[0]
        if found <= order:
            correct = False
            logs[u] = ("%de balise (%d) trouvée dans le mauvaise ordre" % (ic+1, ec))
            break
        order = found
        ncontrols[u] = ic + 1
        
    
    
    t_format = "%d/%m/%Y %H:%M:%S"
    t0 = pd.to_datetime(tstart, format=t_format)
    t1 = pd.to_datetime(tend, format=t_format)
    dt = (t1-t0).total_seconds()
    
    if correct:
        times_OK[u] = dt
        logs[u] = 'OK'
    else:
        times_KO[u] = dt
    return times_OK, times_KO, ncontrols, logs

def test_chasse(dfu, event_controls, seq_controls, u, times_OK, times_KO, ncontrols, logs, tstart, tend):
    seq_controls = np.unique([int(c) for c in seq_controls])
    n = 0
    for s in seq_controls:
        if s in event_controls:
            n +=1

    logs[u] = '%d balises trouvées' % n
    ncontrols[u] = n
    
    t_format = "%d/%m/%Y %H:%M:%S"
    t0 = pd.to_datetime(tstart, format=t_format)
    t1 = pd.to_datetime(tend, format=t_format)
    dt = (t1-t0).total_seconds()
    times_OK[u] = (dt, -1e9*n + dt)


    return times_OK, times_KO, ncontrols, logs

def classify(df, event_name, event_controls, csv_file, chasse=False):
    csv_file.write('Classement %s\n' % event_name)
    print('Classement %s' % event_name)
    dfe = df[df['Event Name'] == event_name]
    users = dfe.User.unique()
    
    times_OK = {}
    times_KO = {}
    ncontrols = {}
    logs = {}
    dates = {}
    
    for u in users:
        dfu = dfe[dfe.User == u]
        ucontrols = np.array(dfu.Control)
        utimes = np.array(dfu.Time)
    
        uu = u.split('(')[0]
        try:
            starts = np.where(ucontrols == 'Start')[0]
            ends = np.where(ucontrols == 'Fin')[0]
            
            assert min(len(starts), len(ends)) > 0
                        
            for i in range(len(starts)):
                if len(ends) > i:
                    seq_controls = ucontrols[starts[i]+1 : ends[i]]
                    if i == 0:
                        uu_seq = uu
                    else:
                        uu_seq = uu + ('(%d)' % i)
                    if not chasse:
                        times_OK, times_KO, ncontrols, logs = test_seq(dfu, event_controls, seq_controls, uu_seq,
                            times_OK, times_KO, ncontrols, logs, utimes[starts[i]], utimes[ends[i]])
                    else:
                        time_OK, time_KO, ncontrols, logs = test_chasse(dfu, event_controls, seq_controls, uu_seq,
                            times_OK, times_KO, ncontrols, logs, utimes[starts[i]], utimes[ends[i]])
                    dates[uu_seq] = utimes[starts[i]][:10]
        except:
            #logs[uu] = "Start/Stop non scannés"
            #times_KO[uu] = 999999
            #dates[uu]
            pass        
            
    if not chasse:
        stimes_OK = list(times_OK.items())
        stimes_OK.sort(key=lambda item: item[1])
        stimes_KO = list(times_KO.items())
        stimes_KO.sort(key=lambda item: item[1])
        stimes = stimes_OK + stimes_KO
    else:
        stimes = list(times_OK.items())
        stimes.sort(key=lambda item: item[1][0])
    for st in stimes:
        t = int(st[1]) if not chasse else int(st[1][0])
        h = t // 3600
        m = (t - h * 3600) // 60
        s =  t % 60
        if t == 999999  :
            h = 99
            m = 99
            s = 99
        print('%s (%s), %d: %02d:%02d:%02d, %s' % (st[0], dates[st[0]], ncontrols[st[0]], h, m, s, logs[st[0]]))
        csv_file.write('%s, %s, %d, %02d:%02d:%02d, %s\n' % (st[0], dates[st[0]], ncontrols[st[0]],  h, m, s, logs[st[0]]))
 
    csv_file.write('\n\n')
    
def print_events(df):
    print(df['Event Name'].unique())