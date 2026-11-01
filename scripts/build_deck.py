"""Recompute embedded presentation data. Runtime deck needs no dependencies."""
from pathlib import Path
from collections import Counter
import json, hashlib, math, re
import numpy as np
from openpyxl import load_workbook
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.contingency_tables import StratifiedTable
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'amazon_synthetic_1500_orders.xlsx'
w=load_workbook(p,read_only=True,data_only=True)
a=list(w['Orders'].values); raw=[dict(zip(a[0],r)) for r in a[1:] if r[0]]
assert len(raw)==1500
rows=[dict(id=r['Order_ID'],date=r['Order_Date'].strftime('%Y-%m-%d'),category=r['Category'],method=r['Payment_Method'],value=float(r['Order_Value_INR']),quantity=int(r['Quantity']),status=r['Order_Status'],cancel=int(r['Cancelled_Flag']),returned=int(r['Return_Flag']),city=r['City']) for r in raw]
assert all(r['cancel']==(r['status']=='Cancelled') and r['returned']==(r['status']=='Returned') for r in rows)
x=np.array([r['value'] for r in rows]); c=np.array([r['method']=='COD' for r in rows]); y=np.array([r['cancel'] for r in rows]);q=np.array([r['quantity'] for r in rows])
def group(data):
 v=np.array([r['value'] for r in data]); outcomes=Counter(r['status'] for r in data)
 total=float(v.sum()); delivered=sum(r['value'] for r in data if r['status']=='Delivered'); settled=[r for r in data if r['status']!='In Transit'];sv=sum(r['value'] for r in settled)
 return dict(n=len(data),cancel=sum(r['cancel'] for r in data),returned=sum(r['returned'] for r in data),rate=sum(r['cancel'] for r in data)/len(data),returnRate=sum(r['returned'] for r in data)/sum(not r['cancel'] for r in data),mean=float(v.mean()),median=float(np.median(v)),sd=float(v.std(ddof=1)),variance=float(v.var(ddof=1)),iqr=float(np.percentile(v,75)-np.percentile(v,25)),cv=float(v.std(ddof=1)/v.mean()),total=total,delivered=delivered,settledValue=sv,settledN=len(settled),settledMean=sv/len(settled),keepPlaced=delivered/total,keepSettled=delivered/sv,outcomes=dict(outcomes))
cod=group([r for r in rows if r['method']=='COD']);pre=group([r for r in rows if r['method']!='COD']);allg=group(rows)
methods=[]
for name in ['COD','UPI','Credit Card','Debit Card','Net Banking','Wallet']:
 g=group([r for r in rows if r['method']==name]);methods.append(dict(name=name,**g))
mt=np.array([[g['cancel'],g['n']-g['cancel']] for g in methods[1:]])
merge=stats.chi2_contingency(mt,correction=False)
hist=np.histogram(x,bins=[*range(0,5001,500),np.inf])[0].tolist()
welch=stats.ttest_ind(x[c],x[~c],equal_var=False,alternative='greater'); se=math.sqrt(cod['variance']/cod['n']+pre['variance']/pre['n']);df=(cod['variance']/cod['n']+pre['variance']/pre['n'])**2/((cod['variance']/cod['n'])**2/(cod['n']-1)+(pre['variance']/pre['n'])**2/(pre['n']-1))
pool=float(y.mean());z=(cod['rate']-pre['rate'])/math.sqrt(pool*(1-pool)*(1/cod['n']+1/pre['n']));gap=cod['rate']-pre['rate'];segap=math.sqrt(cod['rate']*(1-cod['rate'])/cod['n']+pre['rate']*(1-pre['rate'])/pre['n'])
statuses=['Delivered','Cancelled','Returned','In Transit']; table=np.array([[cod['outcomes'].get(s,0) for s in statuses],[pre['outcomes'].get(s,0) for s in statuses]])
chi=stats.chi2_contingency(table,correction=False)
cats=[];tables=[]
for cat in sorted(set(r['category'] for r in rows)):
 gc=group([r for r in rows if r['category']==cat and r['method']=='COD']); gp=group([r for r in rows if r['category']==cat and r['method']!='COD']);cats.append(dict(name=cat,cod=gc,pre=gp,excess=gc['n']*(gc['rate']-gp['rate'])))
 tables.append(np.array([[gc['cancel'],gc['n']-gc['cancel']],[gp['cancel'],gp['n']-gp['cancel']]]))
mh=StratifiedTable(np.stack(tables,axis=2));catnames=sorted(set(r['category'] for r in rows));design=np.column_stack([np.ones(len(rows)),c.astype(float),x/1000,q]+[np.array([r['category']==cat for r in rows],dtype=float) for cat in catnames[1:]])
fit=sm.Logit(y,design).fit(disp=0); ci=fit.conf_int()[1]; crude=cod['cancel']*(pre['n']-pre['cancel'])/((cod['n']-cod['cancel'])*pre['cancel']);or_se=math.sqrt(1/cod['cancel']+1/(cod['n']-cod['cancel'])+1/pre['cancel']+1/(pre['n']-pre['cancel']))
th=cod['mean']+cod['sd']; hi=[r for r in rows if r['method']=='COD' and r['value']>th];lo=[r for r in rows if r['method']=='COD' and r['value']<=th]
coords={'Bengaluru':[12.97,77.59],'Delhi':[28.61,77.21],'Ahmedabad':[23.02,72.57],'Pune':[18.52,73.86],'Kolkata':[22.57,88.36],'Chennai':[13.08,80.27],'Jaipur':[26.91,75.79],'Kochi':[9.93,76.27],'Hyderabad':[17.39,78.49],'Lucknow':[26.85,80.95],'Coimbatore':[11.02,76.96],'Mumbai':[19.08,72.88]}
D=dict(source=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),rows=rows,all=allg,cod=cod,pre=pre,methods=methods,hist=hist,cities=[dict(name=k,n=v,lat=coords[k][0],lon=coords[k][1]) for k,v in Counter(r['city'] for r in rows).most_common()],categories=sorted(cats,key=lambda r:-r['excess']),mergeP=float(merge.pvalue),skew=3*(allg['mean']-allg['median'])/allg['sd'],corr=np.corrcoef([c.astype(float),y,x]).tolist(),threshold=th,highRate=sum(r['cancel'] for r in hi)/len(hi),lowRate=sum(r['cancel'] for r in lo)/len(lo),highN=len(hi),highC=sum(r['cancel'] for r in hi),oneT=(allg['mean']-1500)/(allg['sd']/math.sqrt(len(rows))),oneP=float(stats.ttest_1samp(x,1500).pvalue),welchT=float(welch.statistic),welchP=float(welch.pvalue),welchDF=df,welchSE=se,welchCritical=float(stats.t.ppf(.95,df)),z=z,zP=float(stats.norm.sf(z)),gapCI=[gap-1.96*segap,gap+1.96*segap],chi=float(chi.statistic),chiP=float(chi.pvalue),chiDF=int(chi.dof),expected=chi.expected_freq.tolist(),table=table.tolist(),statuses=statuses,crudeOR=crude,crudeCI=[math.exp(math.log(crude)-1.96*or_se),math.exp(math.log(crude)+1.96*or_se)],mhOR=float(mh.oddsratio_pooled),mhCI=list(mh.oddsratio_pooled_confint()),logOR=float(np.exp(fit.params[1])),logCI=np.exp(ci).tolist(),logCoef=float(fit.params[1]),homogeneityP=float(mh.test_equal_odds().pvalue),binCOD=float(stats.binom.sf(14,100,cod['rate'])),binPre=float(stats.binom.sf(14,100,pre['rate'])))
D['cramers']=math.sqrt(D['chi']/len(rows)); D['breakEven']=(pre['keepSettled']-cod['keepSettled'])*cod['settledMean'];D['breakEvenPlaced']=(pre['keepPlaced']-cod['keepPlaced'])*cod['mean']
jsontext=json.dumps(D,separators=(',',':'),ensure_ascii=False)
out=ROOT/'index.html'
if out.exists():
 text=out.read_text();text=re.sub(r'/\* DATA_START \*/.*?/\* DATA_END \*/',lambda _: '/* DATA_START */\nconst D='+jsontext+';\n/* DATA_END */',text,flags=re.S);out.write_text(text);(ROOT/'Cash or click_ The story (1).html').write_text(text)
(ROOT/'scripts'/'analysis.json').write_text(json.dumps({k:v for k,v in D.items() if k!='rows'},indent=2))
print(json.dumps({k:D[k] for k in ['mergeP','welchT','welchP','z','chi','mhOR','logOR','threshold','highRate','lowRate','breakEven','breakEvenPlaced']},indent=2))
