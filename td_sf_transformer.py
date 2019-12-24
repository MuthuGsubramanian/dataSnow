from dataSnow.coversion_config import *
from playground.files.change_log import *
import os
import datetime



with open('../files/macro/Teradata Actual Macro.txt', 'r') as inp:
    op = inp.readlines()
    mac = ''.join(op)
block = ''.join(mac.split(');')).split(';')


def create_macro(k,v):
        pd = list(filter(lambda x: k in x, block))
        macro_name = pd[0].split('(',1)[0].split('  ',2)[-1].split('\n')[0]
        converted = v.format(macro_name.upper())
        return converted


def merge_into(k,v):
    merge_block = block[1].split('(',1)[1]
    d = ''.join(block).split("  d")[-1]
    update = 'var_sql_logical_delete_capture = ' +d.split(('set'))[0].split('from')[0]
    set = 'set\n' + d.split(('set'))[1]
    from_b = 'from' + d.split(('set'))[0].split('from')[1]
    converted = 'AS'+'\n' +" $$"+ ' ' +'try {' + v.format(merge_block)+';' +'\n\n'+ sf_exe_b + '\n\n' + update + set + from_b + sf_exe_e

    return converted

def new_keys():
    keyw = []
    inp_keys = []
    resp_keys = []
    for i in block:
        keyw.append(i.split(' ', 1)[0] + ' macro')
    for kys in list(conf_map.keys()):
        inp_keys.append(" ".join(kys.split()))
    for h in keyw:
        if h not in inp_keys:
            resp_keys.append(list(filter(lambda x: h in x, block)))
    with open('td_rs_new_keys.txt', 'w') as f:
        for item in resp_keys:
            f.write("%s\n" % item)
    return resp_keys

def query_processor():
    query_resp = []
    for k, v in conf_map.items():
        if k == 'create  macro':
            c_macro = create_macro(k, v)
            query_resp.append(c_macro)
        elif k == 'merge into':
            m_macro = merge_into(k,v)
            query_resp.append(m_macro)
    change_date = str(datetime.datetime.today().date())
    change_id = str(os.getlogin())
    op = change_header + '\n' + change_title + '\n' + change_content.format(date=change_date,
                                                                            id = change_id,
                                                                            version = 'initial',
                                                                            desc = 'test files') + '\n' + change_tail + '\n\n'
    query_resp.insert(0,op)
    with open('td_rs_resp.txt', 'a') as f:
        for item in query_resp:
            f.write("%s\n" % item)
    new_keys()
        # else:

if __name__ == '__main__':
    s = query_processor()
    print(s)


# ''.join(op[op.index('using \n'):op.index('when matched then \n')]).replace('\n','').replace('\t','')