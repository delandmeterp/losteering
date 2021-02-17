# -*- coding: utf-8 -*-

import openpyxl
from datetime import datetime


def write_xlsx(basename):
    
    book = openpyxl.load_workbook('empty.xlsx')
    sheet = book.active
    
    
    now = datetime.now()
    now_str = now.strftime("%d/%m/%Y %H:%M:%S")
    
    sheet['C2'] = now_str
    
    starts = [6, 10, 14, 21, 28]
    
    csv = open(basename + '.csv', 'r')
    lines = csv.readlines()
    
    icls = -1
    shift = 0
    for line in lines[1:]:
        if len(line) == 1: #empty line
            continue
        if line[:10] == 'Classement':
            icls +=1
        else:
            l = line.split(',')
            row = starts[icls] + shift
            sheet.insert_rows(row)
            for col, s in enumerate(l):
               sclean = s if col < len(l)-1 else s[:-1]
               sheet.cell(row=row, column=col+2).value = sclean
            
            shift += 1
    
    
    book.save(basename + '.xlsx')