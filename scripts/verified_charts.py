from pathlib import Path
import json
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

ROOT = Path(__file__).resolve().parent.parent
D = json.loads((ROOT/'output/analysis_data.json').read_text())
A = D['annual']; OUT = ROOT/'output/charts'
plt.rcParams.update({'font.family':'serif','font.serif':['Cambria','DejaVu Serif'], 'font.size':10, 'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.edgecolor':'#777777','axes.labelcolor':'#333333','xtick.color':'#444444','ytick.color':'#444444','axes.axisbelow':True,'savefig.dpi':300})
BLUE='#3F5C6B'; RUST='#A45A3A'; GREEN='#6D7B67'; GRAY='#B9BFC0'
chart_text=[]
def base(title, unit):
    fig, ax=plt.subplots(figsize=(9,4.6),layout='constrained')
    ax.set_title(title,loc='left',fontweight='bold',fontsize=13,pad=16)
    ax.set_ylabel(unit); ax.grid(axis='y',color='#E2E4E3',linewidth=.6)
    ax.tick_params(length=0); chart_text.extend([title,unit]); return fig,ax
def save(fig,name):
    fig.supxlabel('Source: Statutory filings, audited financial disclosures, and institutional market records; author calculations.',fontsize=7,color='#555555')
    fig.savefig(OUT/name,facecolor='white')
    fig.savefig(OUT/name.replace('.png','.pdf'),facecolor='white')
    plt.close(fig)
def values(key,ys):return [A[key][str(y)] for y in ys]
ys=list(range(2007,2027)); ticks=[2007,2010,2013,2016,2019,2022,2026]
f,ax=base('Revenue and net profit, FY2007–FY2026','INR billion')
for k,label,c in [('revenue','Revenue',BLUE),('net_income','Net profit',RUST)]:
    v=[x/1000 for x in values(k,ys)];ax.plot(ys,v,label=label,color=c,lw=2);ax.annotate(f'{v[-1]:,.1f}',(2026,v[-1]),xytext=(-8,9),textcoords='offset points',ha='right',color=c,fontweight='bold')
ax.set(ylim=(0,2000),xticks=ticks,yticks=[0,500,1000,1500,2000]);ax.legend(frameon=False,loc='upper left');save(f,'figure_1_revenue_profit.png')
f,ax=base('Revenue growth and operating margin','Percent')
for k,label,c in [('revenue_growth','Revenue growth',RUST),('operating_margin','Operating margin',BLUE)]:
    v=values(k,ys);ax.plot(ys,v,label=label,color=c,lw=1.8);ax.annotate(f'{v[-1]:.1f}%',(2026,v[-1]),xytext=(-8,8),textcoords='offset points',ha='right',color=c)
ax.set(ylim=(0,50),xticks=ticks);ax.legend(frameon=False,loc='upper right');save(f,'figure_2_growth_margin.png')
f,ax=base('Workforce and revenue per employee','Employees (thousands)')
ax.bar(ys,[v/1000 for v in values('headcount',ys)],color=GRAY,width=.65,label='Employees');ax.set(ylim=(0,400),xticks=ticks)
right=ax.twinx();right.plot(ys,[v/1e6 for v in values('sales_per_employee',ys)],color=GREEN,lw=2,label='Revenue/employee');right.set(ylim=(0,6),ylabel='INR million per employee');right.tick_params(length=0);right.annotate('5.44',(2026,5.4368),xytext=(-10,8),textcoords='offset points',ha='right',color=GREEN)
ax.legend(frameon=False,loc='upper left');right.legend(frameon=False,loc='upper center');save(f,'figure_3_workforce_productivity.png')
for key,sel,name,title,colors in [
 ('geography_pct',[2009,2012,2015,2018,2021,2024,2026],'figure_4_geographic_mix.png','Geographic revenue mix',[BLUE,RUST,GREEN,GRAY]),
 ('segments_pct',[2018,2020,2022,2024,2026],'figure_5_segment_mix.png','Industry revenue mix',['#46545B','#7F8B8E','#988A7E',GREEN,RUST,'#627778','#9A8C68','#BBB8B2'])]:
    f,ax=base(title,'Revenue share (%)');bottom=[0]*len(sel)
    for (label,series),c in zip(D[key].items(),colors):
        vals=[series[str(y)] for y in sel];ax.bar(range(len(sel)),vals,bottom=bottom,width=.62,color=c,label=label)
        for i,(v,b) in enumerate(zip(vals,bottom)):
            if v>=8:ax.text(i,b+v/2,f'{v:.0f}%',ha='center',va='center',fontsize=8,color='white' if c in [BLUE,RUST,GREEN,'#46545B','#627778'] else '#222222')
        bottom=[b+v for b,v in zip(bottom,vals)]
    ax.set(xticks=range(len(sel)),xticklabels=sel,ylim=(0,100),yticks=[0,25,50,75,100]);ax.set_title(title,loc='left',fontweight='bold',fontsize=13,y=1.23,pad=4);ax.legend(frameon=False,ncol=4,fontsize=8,loc='upper center',bbox_to_anchor=(.5,1.17));save(f,name)
f,ax=base('Comparative annualized total returns: dividend treatment qualifies index comparison','')
names=['TCS','Infosys','NIFTY 50','NIFTY IT'];vs=[D['comparative_returns'][n]['annualized_equivalent_pct'] for n in names]
ax.grid(False);ax.grid(axis='x',color='#E2E4E3',lw=.6);ax.barh(names,vs,color=[BLUE,RUST,GRAY,'#929B9D'],height=.55);ax.invert_yaxis();ax.set(xlim=(0,18),xlabel='Displayed annualized equivalent (%)')
for i,v in enumerate(vs):ax.text(v+.15,i,f'{v:.2f}%',va='center',fontsize=10)
save(f,'figure_6_comparative_returns.png')
f,ax=base('Free cash flow, dividends and net repurchases','INR billion')
sel=[2007,2011,2015,2018,2021,2023,2024,2025,2026];dv=[v/1000 for v in values('dividends_paid',sel)];buy=[v/1000 for v in values('buybacks',sel)]
ax.bar(sel,dv,color=GRAY,width=.65,label='Dividends');ax.bar(sel,buy,bottom=dv,color=RUST,width=.65,label='Net repurchases');ax.plot(ys,[v/1000 for v in values('fcf',ys)],color=BLUE,lw=2,label='FCF')
ax.set(ylim=(0,430),xticks=sel,yticks=[0,100,200,300,400]);ax.tick_params(axis='x',labelsize=8);ax.legend(frameon=False,ncol=3,loc='upper left',fontsize=9);save(f,'figure_7_cash_returns.png')
f,ax=base('Infosys monthly price and selected historical markers','Index: 31 May 2006 = 100')
s=D['infosys_monthly_price'];dates=[datetime.fromisoformat(p['date']) for p in s];v=[100*p['price']/s[0]['price'] for p in s];ax.plot(dates,v,color=BLUE,lw=1.6)
events=[('2008-09-15','GFC'),('2014-06-12','CEO appointment'),('2017-08-18','CEO resignation'),('2020-03-11','Pandemic'),('2023-05-23','Topaz'),('2024-04-18','in-tech deal')]
for j,(date,label) in enumerate(events):
    dt=datetime.fromisoformat(date);ax.axvline(dt,color='#BCC1C0',lw=.7,ls='--');ax.text(dt,1450-(j%2)*140,label,fontsize=7,ha='left',va='top')
ax.set(ylim=(0,1500));save(f,'figure_8_timeline.png')
print('Saved eight 300-dpi figures and vector PDF copies.')
