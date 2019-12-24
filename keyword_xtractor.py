import pandas as pd
from pandas import ExcelWriter
import re
file_name= "../files/test_lh2_equip_cat_c_ds6_sp.txt"
phrase=['DECLARE','SET','CALL','MERGE','UPDATE','INSERT','DELETE','SELECT','strtok_split_to_table','substr',
        'cast','max','Union','coalesce','Interval','row_number ( ) over(','ZEROIFNULL(','INDEX']
map = {'DECLARE' : 'Declaration'
,'SET' : 'Set'
,'CALL' : 'Dynamic SQL'
,'MERGE' : 'SQL'
,'UPDATE': 'SQL'
,'UPDATE SET': 'SQL'
,'INSERT VALUES':'SQL'
,'INSERT': 'SQL'
,'DELETE': 'SQL'
,'SELECT': 'SQL'
,'strtok_split_to_table': 'FUNCTION'
,'substr': 'FUNCTION'
,'cast': 'FUNCTION'
,'max': 'FUNCTION'
,'Union': 'SQL'
,'coalesce': 'FUNCTION'
,'Interval': 'FUNCTION'
,'row_number ( ) over(': 'ANALYTICAL FUNCTION'
,'ZEROIFNULL(': 'FUNCTION'
,'INDEX' : 'FUNCTION'
,'lock table' : 'LOCK TABLE'
}

resp = []
phr = []
obj_name = []
op_name = file_name.split('.')[0]
xl_writer = ExcelWriter(op_name + '_output.xlsx')
with open(file_name,encoding='utf-8') as f:
    for i, line in enumerate(f, 0):
        for p,v in map.items():
            if p.lower().strip() in line.lower().strip():
                if not line.startswith('--') or line.startswith('--'):
                    phr.append(p)
                    resp.append([i,p,v])
                elif 'create view' or 'create procedure' or 'replace procedure'in line.lower():
                    obj = line.split('procedure')[1].replace('as','').strip()
                    obj_name.append(obj)

count = {}
for items in phrase:
    count[items]= [phr.count(items)]
op_df = pd.DataFrame(resp)
op_df.columns = ['line_no','keyword','mapping']
op_df['obj_name']= file_name.split('.')[0]
op_df[(op_df['keyword']=='UPDATE') | (op_df['keyword']=='UPDATE SET')]['line_no'].drop_duplicates(keep = 'first',inplace = True)
# count_df = pd.DataFrame(count)
# count_df.columns = ['DECLARE', 'SET', 'CALL', 'MERGE', 'UPDATE', 'INSERT', 'DELETE','SELECT']
print(op_df)

# count_df.to_excel(xl_writer,sheet_name='count',index=False)
op_df.to_excel(xl_writer,sheet_name='keywords',index=False)
xl_writer.save()
