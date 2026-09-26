from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import json
import math
import platform

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output" / "charts"
OUT.mkdir(parents=True, exist_ok=True)
DATA = json.loads((ROOT / "output" / "analysis_data.json").read_text(encoding="utf-8"))

W, H = 1800, 1000
PLOT = (175, 220, 1700, 825)

# Restrained editorial palette: one cool primary, one warm analytical accent,
# and neutral supporting tones.  The background is deliberately warmer than
# pure white so the figures sit naturally in the report rather than resembling
# presentation slides.
NAVY = "#202427"
BLUE = "#3F5C6B"
ORANGE = "#A45A3A"
GREEN = "#6D7B67"
RED = "#8E493C"
PURPLE = "#756C73"
TEAL = "#627778"
GOLD = "#9A8C68"
GREY = "#595B5A"
MID_GREY = "#A9AFB1"
LIGHT = "#DADBD8"
BG = "#FCFCF9"
def _find_font(bold=False):
    """Return a path to Cambria or a serif fallback, checking common OS locations."""
    if bold:
        candidates = [
            Path("C:/Windows/Fonts/cambriab.ttf"),
            Path("/usr/share/fonts/truetype/msttcorefonts/cambriab.ttf"),
            Path("/Library/Fonts/Cambria Bold.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"),
        ]
    else:
        candidates = [
            Path("C:/Windows/Fonts/cambria.ttc"),
            Path("/usr/share/fonts/truetype/msttcorefonts/cambria.ttc"),
            Path("/Library/Fonts/Cambria.ttc"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"),
        ]
    for p in candidates:
        if p.exists():
            return p
    return candidates[-1]  # DejaVu Serif is available on most Linux installs

FONT = _find_font(bold=False)
FONT_B = _find_font(bold=True)


def font(size, bold=False):
    return ImageFont.truetype(str(FONT_B if bold else FONT), size)


def canvas(title, subtitle):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.text((88, 38), title, fill=NAVY, font=font(37, True))
    d.text((88, 91), subtitle, fill=GREY, font=font(20))
    d.line((88, 139, W - 88, 139), fill="#C8C8C3", width=2)
    return im, d


def nice_max(v):
    if v <= 0:
        return 1
    p = 10 ** math.floor(math.log10(v))
    n = v / p
    step = 1 if n <= 1 else 2 if n <= 2 else 5 if n <= 5 else 10
    return step * p


def axes(d, y_min, y_max, y_label, x_labels, x_positions, right_label=None, right_range=None):
    x0, y0, x1, y1 = PLOT
    intervals = 5 if y_max == 50 else 4
    for i in range(intervals + 1):
        y = y1 - (y1 - y0) * i / intervals
        d.line((x0, y, x1, y), fill=LIGHT, width=2)
        val = y_min + (y_max - y_min) * i / intervals
        lab = f"{val:,.0f}" if abs(y_max) >= 50 else f"{val:.1f}"
        bbox = d.textbbox((0, 0), lab, font=font(17))
        d.text((x0 - 20 - (bbox[2]-bbox[0]), y - 10), lab, fill=GREY, font=font(17))
        if right_range:
            rv = right_range[0] + (right_range[1] - right_range[0]) * i / intervals
            rlab = f"{rv:,.0f}" if abs(right_range[1]) >= 50 else f"{rv:.1f}"
            d.text((x1 + 16, y - 10), rlab, fill=GREY, font=font(17))
    d.line((x0, y1, x1, y1), fill="#606261", width=3)
    for lab, x in zip(x_labels, x_positions):
        bbox = d.textbbox((0, 0), str(lab), font=font(16))
        d.text((x - (bbox[2]-bbox[0])/2, y1 + 19), str(lab), fill=GREY, font=font(16))
    d.text((x0, y0-30), y_label, fill=GREY, font=font(17, True), anchor="ls")
    if right_label:
        d.text((x1, y0-30), right_label, fill=GREY, font=font(17, True), anchor="rs")


def source(d, text):
    d.text((88, 955), text, fill=GREY, font=font(14))


def value_label(d, x, y, text, color, dx=10, dy=0):
    f = font(18, True)
    lx, ly = x + dx, y + dy
    d.text((lx, ly), text, fill=color, font=f)


def legend(d, items, x=950, y=164):
    cur = x
    for label, color in items:
        d.line((cur, y + 12, cur + 29, y + 12), fill=color, width=7)
        d.text((cur + 40, y), label, fill=NAVY, font=font(18))
        cur += 60 + d.textlength(label, font=font(18))


def points(xs, vals, y_min, y_max):
    x0, y0, x1, y1 = PLOT
    return [(x, y1 - (v-y_min)/(y_max-y_min)*(y1-y0)) for x, v in zip(xs, vals)]


def dashed_vertical(d, x, y0, y1, color="#BFC2C1", dash=10, gap=8, width=2):
    y = y0
    while y < y1:
        d.line((x, y, x, min(y + dash, y1)), fill=color, width=width)
        y += dash + gap


def save(im, name):
    im.save(OUT / name, optimize=True)


years = list(range(2007, 2027))
annual = DATA["annual"]

# Figure 1
im, d = canvas("Infosys: revenue and net profit, FY2007–FY2026", "Nominal consolidated values; ₹ billion")
xs = [PLOT[0] + (PLOT[2]-PLOT[0]) * i/(len(years)-1) for i in range(len(years))]
rev = [annual["revenue"][str(y)]/1000 for y in years]
ni = [annual["net_income"][str(y)]/1000 for y in years]
ymax = 2000
axes(d, 0, ymax, "₹ billion", [2007, 2010, 2013, 2016, 2019, 2022, 2026], [xs[0], xs[3], xs[6], xs[9], xs[12], xs[15], xs[19]])
d.line(points(xs, rev, 0, ymax), fill=BLUE, width=6, joint="curve")
d.line(points(xs, ni, 0, ymax), fill=ORANGE, width=5, joint="curve")
for x, v, color in [(xs[0], rev[0], BLUE), (xs[-1], rev[-1], BLUE), (xs[0], ni[0], ORANGE), (xs[-1], ni[-1], ORANGE)]:
    y = points([x], [v], 0, ymax)[0][1]
    d.ellipse((x-6,y-6,x+6,y+6), fill=color)
value_label(d, xs[-1], points([xs[-1]],[rev[-1]],0,ymax)[0][1], "₹1,786.5bn", BLUE, dx=-148, dy=-38)
value_label(d, xs[-1], points([xs[-1]],[ni[-1]],0,ymax)[0][1], "₹294.4bn", ORANGE, dx=-130, dy=-38)
legend(d, [("Revenue", BLUE), ("Net profit", ORANGE)], x=1240)
source(d, "Source: Statutory Disclosures & Audited Annual Reports; author calculations.")
save(im, "figure_1_revenue_profit.png")

# Figure 2
im, d = canvas("Growth became steadier as margins normalized", "Year-on-year revenue growth and operating margin; %")
growth = [annual["revenue_growth"][str(y)] for y in years]
margin = [annual["operating_margin"][str(y)] for y in years]
axes(d, 0, 50, "%", [2007, 2010, 2013, 2016, 2019, 2022, 2026], [xs[0], xs[3], xs[6], xs[9], xs[12], xs[15], xs[19]])
d.line(points(xs, growth, 0, 50), fill=ORANGE, width=5, joint="curve")
d.line(points(xs, margin, 0, 50), fill=BLUE, width=6, joint="curve")
dashed_vertical(d, xs[13], PLOT[1], PLOT[3])
d.text((xs[13]+10, PLOT[1]+12), "COVID-era digital acceleration", fill=GREY, font=font(15))
value_label(d, xs[-1], points([xs[-1]],[growth[-1]],0,50)[0][1], "9.6%", ORANGE, dx=-72, dy=10)
value_label(d, xs[-1], points([xs[-1]],[margin[-1]],0,50)[0][1], "20.3%", BLUE, dx=-82, dy=-34)
legend(d, [("Revenue growth", ORANGE), ("Operating margin", BLUE)], x=1120)
source(d, "Source: Audited Annual Reports & Institutional Financial Records; author calculations.")
save(im, "figure_2_growth_margin.png")

# Figure 3
im, d = canvas("Workforce scale and revenue productivity", "Headcount (left) and revenue per employee (right)")
hc = [annual["headcount"][str(y)]/1000 for y in years]
spe = [annual["sales_per_employee"][str(y)]/1_000_000 for y in years]
axes(d, 0, 400, "Employees (000s)", [2007, 2010, 2013, 2016, 2019, 2022, 2026], [xs[0], xs[3], xs[6], xs[9], xs[12], xs[15], xs[19]], "₹ million / employee", (0, 6))
barw = 38
for x, v in zip(xs, hc):
    y = points([x], [v], 0, 400)[0][1]
    d.rectangle((x-barw/2, y, x+barw/2, PLOT[3]), fill="#CDD0D0")
spe_pts = []
for x, v in zip(xs, spe):
    y = PLOT[3] - v/6*(PLOT[3]-PLOT[1])
    spe_pts.append((x,y))
d.line(spe_pts, fill=GREEN, width=6, joint="curve")
value_label(d, xs[-1], points([xs[-1]],[hc[-1]],0,400)[0][1], "328.6k", GREY, dx=-82, dy=12)
value_label(d, xs[-1], spe_pts[-1][1], "₹5.44m", GREEN, dx=-85, dy=-38)
legend(d, [("Headcount", "#CDD0D0"), ("Revenue/employee", GREEN)], x=1090)
source(d, "Source: Statutory Annual Disclosures & SEC Form 20-F Filings; author calculations.")
save(im, "figure_3_workforce_productivity.png")

# Figure 4
im, d = canvas("Geographic revenue mix gradually diversified", "Share of revenue; selected fiscal years; %")
sel = [2009, 2012, 2015, 2018, 2021, 2024, 2026]
colors = [BLUE, ORANGE, GREEN, MID_GREY]
labels = list(DATA["geography_pct"].keys())
x0,y0,x1,y1=PLOT
barw=118
barxs=[x0+(x1-x0)*(i+0.5)/len(sel) for i in range(len(sel))]
axes(d, 0, 100, "% of revenue", sel, barxs)
for x,yr in zip(barxs,sel):
    bottom=y1
    for lab,col in zip(labels,colors):
        v=DATA["geography_pct"][lab][str(yr)]
        top=bottom-v/100*(y1-y0)
        d.rectangle((x-barw/2,top,x+barw/2,bottom),fill=col)
        if v>=8:
            label_color = NAVY if col == MID_GREY else "#FFFFFF"
            d.text((x,(top+bottom)/2),f"{v:.0f}%",fill=label_color,font=font(16,True),anchor="mm")
        bottom=top
legend(d, list(zip(labels, colors)), x=785)
source(d, "Source: Statutory Segment Disclosures & Annual Audited Accounts; author calculations.")
save(im, "figure_4_geographic_mix.png")

# Figure 5
im, d = canvas("Revenue mix shifted toward manufacturing", "Industry share of revenue; selected fiscal years; %")
sel = [2018, 2020, 2022, 2024, 2026]
labels = list(DATA["segments_pct"].keys())
colors = ["#46545B", "#7F8B8E", "#988A7E", GREEN, ORANGE, TEAL, GOLD, "#BBB8B2"]
barxs=[x0+(x1-x0)*(i+0.5)/len(sel) for i in range(len(sel))]
axes(d, 0, 100, "", sel, barxs)
for x,yr in zip(barxs,sel):
    bottom=y1
    for lab,col in zip(labels,colors):
        v=DATA["segments_pct"][lab].get(str(yr),0)
        top=bottom-v/100*(y1-y0)
        d.rectangle((x-80,top,x+80,bottom),fill=col)
        if v>=9:
            label_color = NAVY if col in {"#988A7E", GOLD, "#BBB8B2"} else "#FFFFFF"
            d.text((x,(top+bottom)/2),f"{v:.0f}%",fill=label_color,font=font(15,True),anchor="mm")
        bottom=top
legend(d, list(zip(labels[:4],colors[:4])), x=175, y=153)
legend(d, list(zip(labels[4:],colors[4:])), x=175, y=183)
source(d, "Source: Statutory Segment Disclosures & Annual Audited Accounts; author calculations.")
save(im, "figure_5_segment_mix.png")

# Figure 6
im, d = canvas("Long-run comparative total returns", "Annualized equivalent return; 31 Mar 2006–28 Feb 2026; %")
names=["NIFTY 50","Infosys","TCS","NIFTY IT"]
vals=[DATA["comparative_returns"][n]["annualized_equivalent_pct"] for n in names]
x0,y0,x1,y1=PLOT
for i in range(6):
    x=x0+(x1-x0)*i/5
    d.line((x,y0,x,y1),fill=LIGHT,width=2)
    d.text((x,y1+18),f"{i*4}%",fill=GREY,font=font(16),anchor="ma")
barh=90
ys=[y0+80+i*130 for i in range(4)]
cols=["#B8BABC",ORANGE,BLUE,"#8F9698"]
for name,v,y,col in zip(names,vals,ys,cols):
    d.text((x0-20,y+barh/2),name,fill=NAVY,font=font(22,True),anchor="rm")
    bx=x0+v/20*(x1-x0)
    d.rectangle((x0,y,bx,y+barh),fill=col)
    d.text((bx+18,y+barh/2),f"{v:.2f}%",fill=NAVY,font=font(23,True),anchor="lm")
source(d, "Source: Institutional Market Records, monthly total-return series (239 periods); author calculations.")
save(im, "figure_6_comparative_returns.png")

# Figure 7
im, d = canvas("Cash generation funded rising capital returns", "Free cash flow, cash dividends and share buybacks; selected years; ₹ billion")
sel=[2007,2011,2015,2018,2021,2023,2024,2025,2026]
barxs=[x0+(x1-x0)*(i+0.5)/len(sel) for i in range(len(sel))]
axes(d,0,400,"₹ billion",sel,barxs)
barw=70
for x,yr in zip(barxs,sel):
    dvd=annual["dividends_paid"][str(yr)]/1000
    buy=annual["buybacks"][str(yr)]/1000
    y_dvd=points([x],[dvd],0,400)[0][1]
    d.rectangle((x-barw/2,y_dvd,x+barw/2,y1),fill="#C1C3BE")
    y_total=points([x],[dvd+buy],0,400)[0][1]
    d.rectangle((x-barw/2,y_total,x+barw/2,y_dvd),fill=ORANGE)
fcfvals=[annual["fcf"][str(y)]/1000 for y in sel]
d.line(points(barxs,fcfvals,0,400),fill=BLUE,width=6,joint="curve")
value_label(d, barxs[-1], points([barxs[-1]],[fcfvals[-1]],0,400)[0][1], "FCF ₹339.7bn", BLUE, dx=-150, dy=12)
value_label(d, barxs[-1], points([barxs[-1]],[(annual['dividends_paid'][str(2026)]+annual['buybacks'][str(2026)])/1000],0,400)[0][1], "Returns ₹367.1bn", ORANGE, dx=-165, dy=-40)
legend(d,[("Free cash flow",BLUE),("Dividends", "#C1C3BE"),("Buybacks",ORANGE)],x=1010)
source(d, "Source: Audited Cash Flow Disclosures (IFRS/Ind AS); outflows shown as positive magnitudes.")
save(im, "figure_7_cash_returns.png")

# Figure 8
im, d = canvas("Infosys share-price path and selected historical markers", "Monthly closing-price index; Apr 2006 = 100; price return only")
series=DATA["infosys_monthly_price"]
dates=[datetime.strptime(p["date"],"%Y-%m-%d") for p in series]
base=series[0]["price"]
idx=[p["price"]/base*100 for p in series]
xs2=[x0+(x1-x0)*i/(len(series)-1) for i in range(len(series))]
ymax=nice_max(max(idx)*1.05)
axes(d,0,ymax,"Index (Apr 2006 = 100)",[2006,2010,2014,2018,2022,2026],[xs2[0],xs2[45],xs2[93],xs2[141],xs2[189],xs2[-1]])
d.line(points(xs2,idx,0,ymax),fill=BLUE,width=5,joint="curve")
events=[
    (datetime(2008,9,15),"GFC"),(datetime(2014,6,12),"CEO transition"),(datetime(2017,8,18),"Governance episode"),
    (datetime(2020,3,11),"COVID shock"),(datetime(2021,3,31),"Digital acceleration"),(datetime(2023,5,23),"Topaz launch"),(datetime(2024,4,18),"ER&D deals")]
for j,(dt,label) in enumerate(events):
    i=min(range(len(dates)),key=lambda k:abs((dates[k]-dt).days))
    x=xs2[i]; y=points([x],[idx[i]],0,ymax)[0][1]
    dashed_vertical(d, x, y0, y1, color="#C3C5C3", dash=8, gap=9, width=2)
    d.ellipse((x-6,y-6,x+6,y+6),fill=ORANGE)
    ty=y0+18+(j%2)*34
    d.text((x+6,ty),label,fill=GREY,font=font(15,True))
source(d, "Source: Institutional Market Records (NSE/BSE historical time series); event dates from statutory disclosures.")
save(im, "figure_8_timeline.png")

print(f"Wrote 8 charts to {OUT}")
