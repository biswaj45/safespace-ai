from pathlib import Path
p=Path('toxicity_test_results_20251031_133524.csv')
s=p.read_text(encoding='utf-8')
lines=[l for l in s.splitlines() if l.strip()]
api_fail_count=sum(1 for L in lines if 'API call failed' in L)
# Count lines where groq_is_toxic field (10th column, 0-based index 9) is empty
empty_groq_field=0
for L in lines[1:]:
    cols=L.split(',')
    if len(cols)>=10:
        if cols[9].strip()=='' or cols[9].strip().upper()=='NONE':
            empty_groq_field+=1
print('api_fail_count=',api_fail_count)
print('empty_groq_field=',empty_groq_field)
print('total_messages=',len(lines)-1)
if api_fail_count>0:
    print('\nSample lines with API call failed:')
    for L in lines:
        if 'API call failed' in L:
            print(L)
            break
