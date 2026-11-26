"""Generate the loop diagram and the faction map as static SVGs in four languages."""
import os
import sys

OUT = sys.argv[1]

FONTS = {
    "zh-CN": "'Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif",
    "ja": "'Noto Sans JP','Hiragino Sans','Yu Gothic',sans-serif",
    "en": "'Inter','Helvetica Neue',Arial,sans-serif",
    "fr": "'Inter','Helvetica Neue',Arial,sans-serif",
}

LOOP = {
    "zh-CN": dict(title="AI 切断的是“企业雇佣塔基”这一环", a="塔基出卖时间", b="获得工资收入", c="形成有效需求",
                  d="企业生产并雇佣", ai="AI：生产改由算力完成", wage="工资", spend="消费", orders="订单",
                  cut="不再需要人"),
    "en": dict(title="AI breaks one link: firms hiring the base", a="The base sells its time", b="Wage income",
               c="Effective demand", d="Firms produce and hire", ai="AI: compute does the work",
               wage="wages", spend="spending", orders="orders", cut="people no longer needed"),
    "fr": dict(title="L'IA rompt un maillon : l'embauche de la base", a="La base vend son temps",
               b="Revenu salarial", c="Demande effective", d="Production et embauche",
               ai="IA : le calcul remplace", wage="salaires", spend="consommation", orders="commandes",
               cut="plus besoin d'humains"),
    "ja": dict(title="AI が断ち切るのは「企業が基層を雇う」という環", a="基層が時間を売る", b="賃金収入",
               c="有効需要", d="企業が生産し雇用する", ai="AI：生産を計算資源が担う", wage="賃金",
               spend="消費", orders="受注", cut="人が不要になる"),
}

FACTIONS = {
    "zh-CN": dict(
        title="美国政治阵营：AI 发展速度 × 收益分配方式",
        x_left="主张放缓、限制", x_right="主张加速",
        y_top="收益公共化（再分配、公共持股）", y_bottom="收益留在市场",
        wh="白宫与科技右翼", wh2="特朗普、Sacks",
        pop="民粹右翼", pop2="Bannon、Hawley",
        prog="民主党进步派", prog2="Sanders：主权财富基金",
        main="民主党主流与州政府", main2="Hochul、加州、各州检察长",
        corp="部分 AI 企业与资本家", corp2="OpenAI 公共财富基金、马斯克",
        note="位置为定性归类，不是测量结果。资料截至 2026 年 11 月。"),
    "en": dict(
        title="US political camps: pace of AI × who gets the gains",
        x_left="Slow down, restrict", x_right="Accelerate",
        y_top="Gains made public (redistribution, public stakes)", y_bottom="Gains stay with the market",
        wh="White House and tech right", wh2="Trump, Sacks",
        pop="Populist right", pop2="Bannon, Hawley",
        prog="Progressive Democrats", prog2="Sanders: sovereign wealth fund",
        main="Mainstream Democrats, states", main2="Hochul, California, state AGs",
        corp="Some AI firms and investors", corp2="OpenAI public wealth fund, Musk",
        note="Positions are a qualitative classification, not a measurement. As of November 2026."),
    "fr": dict(
        title="Camps politiques américains : rythme de l'IA × partage des gains",
        x_left="Ralentir, encadrer", x_right="Accélérer",
        y_top="Gains socialisés (redistribution, part publique)", y_bottom="Gains laissés au marché",
        wh="Maison-Blanche et droite tech", wh2="Trump, Sacks",
        pop="Droite populiste", pop2="Bannon, Hawley",
        prog="Démocrates progressistes", prog2="Sanders : fonds souverain",
        main="Démocrates centristes, États", main2="Hochul, Californie, procureurs",
        corp="Certaines firmes d'IA", corp2="Fonds public d'OpenAI, Musk",
        note="Positions qualitatives, non mesurées. Données à novembre 2026."),
    "ja": dict(
        title="米国の政治陣営：AI の速度 × 利益の分配",
        x_left="減速・規制", x_right="加速",
        y_top="利益の公共化（再分配・公的持株）", y_bottom="利益は市場に残す",
        wh="ホワイトハウスとテック右派", wh2="トランプ、サックス",
        pop="ポピュリスト右派", pop2="バノン、ホーリー",
        prog="民主党進歩派", prog2="サンダース：政府系ファンド",
        main="民主党主流派と州政府", main2="ホークル、カリフォルニア州、州司法長官",
        corp="一部の AI 企業・投資家", corp2="OpenAI 公共富基金、マスク",
        note="位置は定性的な分類であり、測定値ではない。2026 年 11 月時点。"),
}

INK = "#1f2328"
QUIET = "#57606a"
EDGE = "#8c959f"
ACCENT = "#2f6fdb"
BAD = "#cf222e"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def loop_svg(lang):
    t = LOOP[lang]
    f = FONTS[lang]
    W, H = 250, 52
    cl, cr, ra, rb, mid = 160, 600, 110, 250, 380

    def box(cx, cy, label):
        return (f'<rect x="{cx - W / 2}" y="{cy - H / 2}" width="{W}" height="{H}" rx="8" fill="#ffffff" '
                f'stroke="{EDGE}" stroke-width="1.25"/>'
                f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" font-size="14" fill="{INK}">{esc(label)}</text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 310" font-family="{f}">
<rect width="760" height="310" fill="#ffffff"/>
<defs>
<marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{EDGE}"/></marker>
<marker id="b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{ACCENT}"/></marker>
</defs>
<text x="24" y="36" font-size="17" font-weight="600" fill="{INK}">{esc(t["title"])}</text>
<g fill="none" stroke="{EDGE}" stroke-width="1.5">
<path d="M{cl + W / 2} {ra}H{cr - W / 2}" marker-end="url(#a)"/>
<path d="M{cr} {ra + H / 2}V{rb - H / 2}" marker-end="url(#a)"/>
<path d="M{cr - W / 2} {rb}H{cl + W / 2}" marker-end="url(#a)"/>
<path d="M{cl} {rb - H / 2}V{ra + H / 2}" marker-end="url(#a)"/>
</g>
{box(cl, ra, t["a"])}
{box(cr, ra, t["b"])}
{box(cr, rb, t["c"])}
{box(cl, rb, t["d"])}
<g stroke="{BAD}" stroke-width="2.5"><line x1="{cl - 11}" y1="169" x2="{cl + 11}" y2="191"/><line x1="{cl + 11}" y1="169" x2="{cl - 11}" y2="191"/></g>
<rect x="330" y="154" width="230" height="52" rx="8" fill="{ACCENT}" fill-opacity="0.12" stroke="{ACCENT}" stroke-width="2"/>
<text x="445" y="185" text-anchor="middle" font-size="14" font-weight="600" fill="{INK}">{esc(t["ai"])}</text>
<path d="M330 180H{cl + 18}" fill="none" stroke="{ACCENT}" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#b)"/>
<text x="{mid}" y="{ra - 10}" text-anchor="middle" font-size="12" fill="{QUIET}">{esc(t["wage"])}</text>
<text x="{cr + 12}" y="185" font-size="12" fill="{QUIET}">{esc(t["spend"])}</text>
<text x="{mid}" y="{rb - 10}" text-anchor="middle" font-size="12" fill="{QUIET}">{esc(t["orders"])}</text>
<text x="{cl + 18}" y="168" font-size="12" fill="{QUIET}">{esc(t["cut"])}</text>
</svg>
'''


def factions_svg(lang):
    t = FACTIONS[lang]
    f = FONTS[lang]
    x0, x1, y0, y1 = 70, 700, 90, 480
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2

    def dot(x, y, name, sub, color, anchor="start"):
        dx = 12 if anchor == "start" else -12
        return (f'<circle cx="{x}" cy="{y}" r="8" fill="{color}" fill-opacity="0.85"/>'
                f'<text x="{x + dx}" y="{y - 2}" text-anchor="{anchor}" font-size="14" font-weight="600" fill="{INK}">{esc(name)}</text>'
                f'<text x="{x + dx}" y="{y + 16}" text-anchor="{anchor}" font-size="12" fill="{QUIET}">{esc(sub)}</text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 560" font-family="{f}">
<rect width="760" height="560" fill="#ffffff"/>
<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{EDGE}"/></marker></defs>
<text x="24" y="36" font-size="17" font-weight="600" fill="{INK}">{esc(t["title"])}</text>
<g stroke="{EDGE}" stroke-width="1.25" fill="none">
<path d="M{x0} {cy}H{x1}" marker-end="url(#a)" marker-start="url(#a)"/>
<path d="M{cx} {y1}V{y0}" marker-end="url(#a)" marker-start="url(#a)"/>
</g>
<text x="{x0}" y="{cy - 10}" font-size="12" fill="{QUIET}">{esc(t["x_left"])}</text>
<text x="{x1}" y="{cy - 10}" text-anchor="end" font-size="12" fill="{QUIET}">{esc(t["x_right"])}</text>
<text x="{cx + 10}" y="{y0 + 6}" font-size="12" fill="{QUIET}">{esc(t["y_top"])}</text>
<text x="{cx + 10}" y="{y1}" font-size="12" fill="{QUIET}">{esc(t["y_bottom"])}</text>
{dot(640, 420, t["wh"], t["wh2"], "#d1242f", "end")}
{dot(250, 400, t["pop"], t["pop2"], "#bc4c00", "end")}
{dot(130, 140, t["prog"], t["prog2"], ACCENT, "start")}
{dot(260, 330, t["main"], t["main2"], "#1a7f37", "end")}
{dot(640, 170, t["corp"], t["corp2"], "#8250df", "end")}
<text x="24" y="535" font-size="12" fill="{QUIET}">{esc(t["note"])}</text>
</svg>
'''


for lang in LOOP:
    with open(os.path.join(OUT, f"loop-{lang}.svg"), "w", encoding="utf-8") as fh:
        fh.write(loop_svg(lang))
    with open(os.path.join(OUT, f"factions-{lang}.svg"), "w", encoding="utf-8") as fh:
        fh.write(factions_svg(lang))
print("done")

PATHS = {
    "zh-CN": dict(title="割裂之后的三条路径", start="选票仍在，劳动权丧失",
                  a="A. 再分配契约", a2="主权基金、分红、基本收入", b="B. 两极化与强人政治", b2="再分配受阻，民粹竞相激进",
                  c="C. 空心选举", c2="形式保留，决策移出选民射程", ab="立法失败", bc="以恢复秩序为名",
                  note="三条路径并不互斥，可能依次出现。"),
    "en": dict(title="Three paths after the split", start="Votes remain, labor power is gone",
               a="A. Redistributive pact", a2="Wealth fund, dividends, UBI", b="B. Polarization, strongmen",
               b2="Redistribution blocked", c="C. Hollow elections",
               c2="Form kept, power elsewhere", ab="legislation fails", bc="in the name of order",
               note="The paths are not exclusive and may follow one another."),
    "fr": dict(title="Trois voies après la rupture", start="Le vote demeure, le travail ne pèse plus",
               a="A. Pacte redistributif", a2="Fonds, dividendes, revenu", b="B. Polarisation, homme fort",
               b2="Redistribution bloquée", c="C. Élections creuses",
               c2="Forme intacte, pouvoir ailleurs", ab="échec législatif", bc="au nom de l'ordre",
               note="Les voies ne s'excluent pas et peuvent se succéder."),
    "ja": dict(title="分断の後の三つの道", start="票は残り、労働の力は失われる",
               a="A. 再分配の合意", a2="政府系ファンド・配当・基本所得", b="B. 分極化と強権政治",
               b2="再分配が阻まれ、過激化", c="C. 空洞化した選挙",
               c2="形式は残り、決定は手の外へ", ab="立法の失敗", bc="秩序回復を名目に",
               note="三つの道は排他的ではなく、順に現れうる。"),
}


def paths_svg(lang):
    t = PATHS[lang]
    f = FONTS[lang]
    W, H = 206, 72
    xs = {"a": 128, "b": 380, "c": 632}
    y0, y1 = 100, 270

    def box(cx, cy, name, sub, color):
        return (f'<rect x="{cx - W / 2}" y="{cy - H / 2}" width="{W}" height="{H}" rx="8" fill="{color}" fill-opacity="0.08" stroke="{color}" stroke-width="1.5"/>'
                f'<text x="{cx}" y="{cy - 6}" text-anchor="middle" font-size="14" font-weight="600" fill="{INK}">{esc(name)}</text>'
                f'<text x="{cx}" y="{cy + 16}" text-anchor="middle" font-size="11.5" fill="{QUIET}">{esc(sub)}</text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 360" font-family="{f}">
<rect width="760" height="360" fill="#ffffff"/>
<defs>
<marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{EDGE}"/></marker>
<marker id="r" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{BAD}"/></marker>
</defs>
<text x="24" y="36" font-size="17" font-weight="600" fill="{INK}">{esc(t["title"])}</text>
<rect x="230" y="{y0 - 24}" width="300" height="48" rx="8" fill="{ACCENT}" fill-opacity="0.12" stroke="{ACCENT}" stroke-width="2"/>
<text x="380" y="{y0 + 5}" text-anchor="middle" font-size="14" font-weight="600" fill="{INK}">{esc(t["start"])}</text>
<g fill="none" stroke="{EDGE}" stroke-width="1.5">
<path d="M300 {y0 + 24}V150H{xs["a"]}V{y1 - H / 2}" marker-end="url(#a)"/>
<path d="M380 {y0 + 24}V{y1 - H / 2}" marker-end="url(#a)"/>
<path d="M460 {y0 + 24}V150H{xs["c"]}V{y1 - H / 2}" marker-end="url(#a)"/>
</g>
{box(xs["a"], y1, t["a"], t["a2"], "#1a7f37")}
{box(xs["b"], y1, t["b"], t["b2"], BAD)}
{box(xs["c"], y1, t["c"], t["c2"], "#57606a")}
<g fill="none" stroke="{BAD}" stroke-width="1.5" stroke-dasharray="5 4">
<path d="M{xs["a"] + W / 2} {y1 + 20}H{xs["b"] - W / 2}" marker-end="url(#r)"/>
<path d="M{xs["b"] + W / 2} {y1 + 20}H{xs["c"] - W / 2}" marker-end="url(#r)"/>
</g>
<text x="{(xs["a"] + xs["b"]) / 2}" y="{y1 + 52}" text-anchor="middle" font-size="11.5" fill="{BAD}">{esc(t["ab"])}</text>
<text x="{(xs["b"] + xs["c"]) / 2}" y="{y1 + 52}" text-anchor="middle" font-size="11.5" fill="{BAD}">{esc(t["bc"])}</text>
<text x="24" y="345" font-size="12" fill="{QUIET}">{esc(t["note"])}</text>
</svg>
'''


for lang in PATHS:
    with open(os.path.join(OUT, f"paths-{lang}.svg"), "w", encoding="utf-8") as fh:
        fh.write(paths_svg(lang))
print("paths done")
