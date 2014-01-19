#!/usr/bin/python


import sys
import re
import pprint
import json

if __name__ == '__main__':


    fields = ['id', 'name', 'pan_number', 'password', 'date_of_birth_or_incarnation', 'contact_number', 'bank_name', 'bank_branch' ,'account_number', 'ifsc_code', 'micr', 'account_type', 'email', 'address', 'city', 'pincode', 'status', 'employer', 'self_occupied']
    _file = sys.argv[1]
    records = []
    for line in open(_file):
        values = line.split(",")
        values = re.findall('[^"]*?,|".*?",', line)
        
        field_values = dict([(k, v.strip(", \"")) for k,v in zip(fields, values)])
        field_values['user_id'] = field_values['pan_number']
        field_values['fathers_name'] = ''
        if field_values['date_of_birth_or_incarnation'] != '':
            d, m, y = field_values['date_of_birth_or_incarnation'].split('/')
            date = "%s-%s-%s" % (y, m, d)
            field_values['date_of_birth_or_incarnation'] = date
        else:
            field_values['date_of_birth_or_incarnation'] = '1900-01-01'
        if field_values['self_occupied'] == '':
            field_values['self_occupied'] = False
        record = {"model": "report.person", "pk": int(field_values['id'])}

        #field_values.pop("id")
        record['fields'] = field_values

        records.append(record)
        
    #pprint.pprint(records)

    print json.dumps(records)

