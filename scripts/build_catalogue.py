#!/usr/bin/env python3
"""Build data/catalogue.js from the brand-store research in data/research-*/.

Facts (official names, sizes/shades, SKUs, barcodes, brand list prices) are read
from the research files; the Russian descriptions and usage text below are our own
wording. Store prices in UZS are still demo values: the default variant keeps the
site's price and other variants follow the brand's own price ratio.

Run:  python3 scripts/build_catalogue.py
"""
import json, os, re
from datetime import date

ROOT = os.path.join(os.path.dirname(__file__), '..')
DATA = os.path.join(ROOT, 'data')
CHECKED = date.today().isoformat()

def research(path):
    with open(os.path.join(DATA, path)) as f:
        return json.load(f)

def store_product(path, handle):
    for p in research(path)['products']:
        if p['handle'] == handle:
            return p
    raise KeyError(f'{path}: {handle}')

def romand(title):
    for p in research('research-26-39/romand-all.json')['products']:
        if p['title'] == title:
            return p
    raise KeyError(title)

# id -> spec. "variants": [(match in brand variant title, our label)], first one is the default.
# "base": UZS price of the default variant (demo). "url": full source URL where known.
SPECS = {
 0: dict(src='research-0-11/0.json', url='https://www.cosrx.com/products/advanced-snail-96-mucin-power-essence',
         base=219000, old=259000, variants=[('100mL','100 мл'),('50ml','50 мл'),('30mL','30 мл')],
         description='Эссенция с 96% фильтрата муцина улитки. Увлажняет, поддерживает защитный барьер и выравнивает текстуру кожи. Подходит всем типам кожи, в том числе чувствительной и после высыпаний.',
         keyIngredients=['Фильтрат муцина улитки 96%']),
 1: dict(src='research-0-11/1.json', base=129000, variants=[('150ml','150 мл'),(r'^1\.69','50 мл')],
         description='Мягкий гель для умывания со слабокислым pH. Очищает, не пересушивая, и подходит для ежедневного использования утром и вечером.'),
 3: dict(src='research-0-11/3.json', name='Glow Serum: Propolis + Niacinamide', base=209000,
         variants=[('30ml','30 мл'),('60ml','60 мл')],
         description='Сыворотка с прополисом и ниацинамидом: увлажняет, успокаивает и делает поры и текстуру кожи визуально более ровными.',
         keyIngredients=['Экстракт прополиса','Ниацинамид']),
 4: dict(src='research-0-11/4.json', name='Heartleaf 77 Soothing Toner', base=249000, old=289000,
         variants=[('250ml','250 мл'),('500ml','500 мл')],
         description='Успокаивающий тонер с экстрактом хауттюйнии (heartleaf). Снимает ощущение раздражения и увлажняет.',
         keyIngredients=['Экстракт хауттюйнии сердцевидной 77%']),
 5: dict(src='research-0-11/5.json', base=269000, variants=[('Default','200 мл')],
         description='Гидрофильное масло для первого этапа очищения: растворяет макияж, SPF и излишки себума.'),
 6: dict(src='research-0-11/6.json', base=229000, variants=[('200ml','200 мл'),('100ml','100 мл'),('500ml','500 мл')],
         description='Увлажняющий тонер с минералами морской воды острова Токто. Мягко отшелушивает ороговевшие клетки и выравнивает текстуру. Без отдушки.',
         keyIngredients=['Морская вода (глубоководная)','Минералы: магний, кальций, цинк'],
         howTo='После умывания смочите ватный диск и мягко протрите лицо по направлению массажных линий.'),
 8: dict(src='research-0-11/8.json', name='Lip Sleeping Mask', base=239000, variantGalleryOnly=True,
         variants=[('Berry','Berry (оригинал)'),('Lemon Sorbet','Lemon Sorbet'),('Strawberry Shortcake','Strawberry Shortcake'),
                   ('Pink Lemonade','Pink Lemonade'),('Matcha Bubble Tea','Matcha Bubble Tea'),('Acai Mango Smoothie','Acai Mango Smoothie')],
         description='Ночная несмываемая маска для губ. Смягчает и интенсивно увлажняет, к утру губы гладкие.',
         keyIngredients=['Комплекс ягод','Масло мурумуру','Масло ши'],
         howTo='Вечером нанесите плотный слой на губы и оставьте на ночь. Утром остатки можно снять салфеткой.'),
 9: dict(src='research-0-11/9.json', name='Water Bank Blue Hyaluronic Cream', base=389000, skip_images=['Infographic','Matin_Kim'],
         variants=[('^50mL','50 мл'),('Mini','Мини 20 мл'),('Refill','Рефил (сменный блок)')],
         description='Увлажняющий крем, укрепляющий защитный барьер кожи; эффект увлажнения подтверждён клиническим исследованием бренда.'),
 10: dict(src='research-0-11/10.json', url='https://www.skin1004.com/products/skin1004-madagascar-centella-ampoule',
          name='Madagascar Centella Ampoule', base=189000, old=219000,
          variants=[('55ml','55 мл'),('30ml','30 мл'),('100ml','100 мл')],
          description='Ампула с экстрактом центеллы азиатской из Мадагаскара. Успокаивает покраснения и увлажняет; подходит всем типам кожи, особенно сухой и чувствительной.',
          keyIngredients=['Экстракт центеллы азиатской']),
 11: dict(src='research-0-11/11.json', name='Hyalu-Cica Water-Fit Sun Serum SPF50+ PA++++', base=199000,
          variants=[('^50ml','50 мл'),('15ml','15 мл'),('100ml','100 мл')],
          description='Лёгкий солнцезащитный крем-сыворотка с химическими фильтрами: быстро впитывается, увлажняет и не оставляет жирного блеска.',
          keyIngredients=['Экстракт центеллы азиатской','Гиалуроновая кислота','Экстракт листьев зелёного чая']),
 12: dict(src='research-12-25/12.json', url='https://torriden.us/products/dive-in-serum', name='DIVE-IN Low Molecular Hyaluronic Acid Serum',
          base=219000, variants=[('Single','50 мл')],
          description='Увлажняющая сыворотка с низкомолекулярными гиалуроновыми кислотами разного размера. Подходит даже для чувствительной кожи.',
          keyIngredients=['Гиалуроновая кислота (5 типов)'],
          howTo='Нанесите небольшое количество на лицо и мягко вбейте похлопывающими движениями до впитывания.'),
 13: dict(src='research-12-25/13.json', url='https://torriden.us/products/dive-in-soothing-cream', name='DIVE-IN Soothing Cream',
          base=249000, variants=[('Jar','100 мл, банка'),('Tube','Туба')],
          description='Лёгкий гель-крем с гиалуроновой кислотой: охлаждает, увлажняет и успокаивает покраснения от жары и раздражения.',
          keyIngredients=['Гиалуроновая кислота (5 типов)'],
          howTo='Нанесите небольшое количество на лицо и вбейте похлопывающими движениями. Для более лёгкой текстуры можно смешать с тонером.'),
 14: dict(src='research-12-25/14.json', base=179000, variants=[('50ml','50 мл')],
          description='Солнцезащитный гель на водной основе с восемью видами гиалуроновой кислоты. Свежий финиш без липкости.',
          keyIngredients=['Гиалуроновая кислота (8 видов)','Ниацинамид','Центелла азиатская'],
          howTo='Последний шаг утреннего ухода: нанесите достаточное количество на лицо и вбейте до впитывания.'),
 15: dict(url='https://en.somebymi.com/product/aha-bha-pha-30-days-miracle-toner-150ml/73/', base=189000,
          images=['https://en.somebymi.com/web/product/big/202412/595ada9757e13df90f36fac8e02e81ed.jpg'], manual_variants=[('150 мл',None,None)],
          description='Отшелушивающий тонер с кислотами AHA, BHA и PHA для кожи, склонной к жирности и несовершенствам.',
          keyIngredients=['AHA','BHA','PHA'],
          howTo='После умывания обильно смочите ватный диск и протрите лицо по направлению роста волосков, затем слегка похлопайте.'),
 16: dict(src='research-12-25/16.json', name='AGE-R Booster Pro', cat='device', art='device', palette=0, base=2890000,
          variants=[('Pink','Розовый'),('Black','Чёрный')],
          description='Домашний бьюти-прибор «6 в 1» для ухода за кожей лица: режимы для сияния, пор и упругости. В комплекте инструкция и USB-кабель.',
          howTo='Пользуйтесь по инструкции из комплекта; режимы и интенсивность настраиваются в приложении AGE-R.'),
 17: dict(src='research-12-25/17.json', name='Zero Pore Pad 2.0', base=269000, variants=[('SINGLE','70 шт')],
          description='Пэды с двумя текстурами, пропитанные BHA (салициловой кислотой) и AHA. Отшелушивают и помогают очищать поры.',
          keyIngredients=['Салициловая кислота (BHA)','AHA'],
          howTo='После умывания протрите лицо рельефной стороной от центра к краям, затем гладкой стороной. Остатки вбейте похлопыванием.'),
 21: dict(src='research-12-25/21.json', name='First Care Activating Serum VI', base=1290000,
          variants=[('60','60 мл'),('90','90 мл')],
          description='Антивозрастная сыворотка-бустер: смягчает вид мелких морщин и укрепляет кожу. Для нормальной, сухой, комбинированной и жирной кожи.',
          keyIngredients=['Экстракт женьшеня','Экстракты корейских трав','Производное витамина C']),
 23: dict(src='research-12-25/23.json', name='The N.M.F Ampoule Mask × 10', base=139000, old=169000, variants=[('10 Pack','10 шт')],
          description='Тканевая маска с натуральным увлажняющим фактором (N.M.F): снимает ощущение стянутости и оставляет кожу мягкой и сияющей.',
          keyIngredients=['Комплекс N.M.F','Церамиды','Сквалан']),
 25: dict(src='research-12-25/25.json', name='No.5+ Glutathione Vitamin Concentrated Sheet Mask × 5', base=119000, variants=[('Default','5 шт')],
          description='Тканевые маски с витаминами и глутатионом для более ровного и сияющего тона.'),
 27: dict(romand='JUICY LASTING TINT', base=129000,
          variants=[('PEELING ANGDOO','Peeling Angdoo'),('JUJUBE','Jujube'),('APPLE BROWN','Apple Brown'),
                    ('PINK PUMPKIN','Pink Pumpkin'),('CHERRY BOMB','Cherry Bomb'),('CORNI SODA','Corni Soda')],
          description='Глянцевый тинт для губ с сочным, стойким цветом.'),
 28: dict(src='research-26-39/romand-dewy.json', name='Dewy·ful Water Tint', base=129000,
          variants=[('IN CORAL','In Coral'),('SALTY PEACH','Salty Peach'),('IF ROSE','If Rose'),('CHILI UP','Chili Up'),('THULIAN','Thulian'),('CHERRY WAY','Cherry Way')],
          description='Лёгкий водянистый тинт с влажным сияющим финишем. Есть оттенки для тёплого и холодного подтона.',
          howTo='Нанесите тинт на внутреннюю часть губ, растушуйте к краям и подождите несколько секунд.'),
 29: dict(romand='BETTER THAN CHEEK', base=139000,
          variants=[('ODI MILK','Odi Milk'),('NUTTY NUDE','Nutty Nude'),('PEACH CHIP','Peach Chip'),('VINE NUDE','Vine Nude'),('BLUEBERRY CHIP','Blueberry Chip'),('MANGO CHIP','Mango Chip')],
          description='Компактные румяна с мягким естественным цветом.'),
 31: dict(src='research-26-39/clio-mascara.json', base=169000,
          variants=[('01 Long Curling / None','01 Long Curling'),('02 Volume Curling / None','02 Volume Curling'),('04 Extreme Volume / None','04 Extreme Volume')],
          description='Водостойкая тушь: длина, подкручивание и чёткое разделение ресниц на весь день.'),
 34: dict(src='research-26-39/haruharu.json', brand='Haruharu Wonder', name='Black Rice Hyaluronic Toner', base=269000,
          variants=[('150ml','150 мл'),('30ml','30 мл'),('300ml','300 мл')],
          description='Лёгкий увлажняющий тонер с ферментированным экстрактом корейского чёрного риса. Веганская формула.',
          keyIngredients=['Ферментированный экстракт чёрного риса','Бетаин','Бета-глюкан'],
          howTo='После умывания смочите ватный диск, распределите тонер по лицу и вбейте до полного впитывания.'),
 39: dict(src='research-26-39/innisfree-cream.json', name='Green Tea Seed Hyaluronic Cream', base=259000,
          variants=[('50ML','50 мл'),('30ML','30 мл'),('80ML','80 мл')],
          description='Ежедневный увлажняющий крем с зелёным чаем и гиалуроновой кислотой: укрепляет барьер сухой и тусклой кожи.',
          keyIngredients=['Экстракт семян зелёного чая','Гиалуроновая кислота']),

 # ---- replacements: the original products' brand stores could not be reached; same category, real products ----
 2: dict(store=('research-extra/beautyofjoseon.com-1.json','relief-sun-rice-probiotics'), name='Relief Sun: Rice + Niacinamide SPF50+ PA++++',
         base=189000, variants=[('1-Pack','50 мл'),('2-Pack','2 × 50 мл')],
         description='Кремовый, но лёгкий солнцезащитный крем с экстрактом риса: увлажняет без липкости и оставляет сияющий финиш.',
         keyIngredients=['Экстракт риса','Ниацинамид']),
 7: dict(store=('research-extra/beautyofjoseon.com-1.json','relief-sun-aqua-fresh'), brand='Beauty of Joseon', name='Relief Sun Aqua-Fresh: Rice + B5 SPF50+ PA++++',
         base=189000, variants=[('1-Pack','50 мл'),('2-Pack','2 × 50 мл')], skin=['oily','combo'],
         description='Самая лёгкая версия Relief Sun — флюид с рисовой водой. Хорошо подходит для жирной и комбинированной кожи.',
         keyIngredients=['Рисовая вода','Пантенол (B5)']),
 18: dict(store=('research-extra/torriden.us-1.json','dive-in-toner'), brand='Torriden', name='DIVE-IN Low Molecular Hyaluronic Acid Toner',
          base=229000, variants=[('Default','1 шт')], art='toner', palette=3, skin=['dry','combo','sens'],
          description='Мягкий тонер с низким pH: убирает излишки себума после умывания и восполняет увлажнение без липкости.',
          keyIngredients=['Гиалуроновая кислота']),
 19: dict(store=('research-extra/anua.us-1.json','niacinamide-10-txa-4-serum-copy-1'), brand='Anua', name='Niacinamide 10 + TXA 4 Dark Spot Serum',
          base=239000, variants=[('Default','1 шт')], art='dropper', palette=4, skin=['oily','combo','sens'],
          description='Сыворотка против пятен постакне и неровного тона с 10% ниацинамида и 4% транексамовой кислоты; церамиды и гиалуроновая кислота смягчают формулу.',
          keyIngredients=['Ниацинамид 10%','Транексамовая кислота 4%','Церамиды','Гиалуроновая кислота']),
 20: dict(store=('research-extra/www.cosrx.com-1.json','pure-fit-cica-cream-intensive'), brand='COSRX', name='Pure Fit Cica Cream Intense',
          base=319000, variants=[('Default','50 мл')], art='jar', palette=1,
          description='Плотный крем с комплексом из 7 видов экстракта центеллы: успокаивает чувствительную кожу и глубоко увлажняет.',
          keyIngredients=['Комплекс Cica-7 (центелла азиатская)']),
 22: dict(store=('research-extra/www.cosrx.com-1.json','one-step-original-clear-skin-calming-pad'), brand='COSRX', name='One Step Original Clear Skin Calming Pad',
          base=259000, variants=[('Default','1 банка · 280 мл эссенции')], cat='toner', art='jar', palette=1,
          description='Крупные пэды, пропитанные эссенцией с водой зелёного чая (82%) и центеллой: успокаивают покраснения и выравнивают текстуру.',
          keyIngredients=['Вода зелёного чая 82%','Центелла азиатская']),
 24: dict(store=('research-extra/www.cosrx.com-1.json','the-hyaluronic-acid-3-serum_new'), brand='COSRX', name='The Hyaluronic Acid 3 Serum',
          base=249000, variants=[('Default','1 шт')], art='dropper', palette=3,
          description='Увлажняющая сыворотка с 3% гиалуроновой кислоты — простой базовый шаг для любого типа кожи.',
          keyIngredients=['Гиалуроновая кислота 3%']),
 26: dict(store=('research-extra/anua.us-1.json','3-ceramide-panthenol-moisture-barrier-cream'), brand='Anua', name='3 Ceramide Panthenol Moisture Barrier Cream',
          base=219000, variants=[('Default','1 шт')], art='jar', palette=9,
          description='Мягкий увлажняющий крем для чувствительной кожи: помогает удерживать влагу и уменьшает покраснения от сухости.',
          keyIngredients=['Церамиды (3 вида)','Пантенол']),
 30: dict(store=('research-extra/us.sulwhasoo.com-1.json','perfecting-cushion-ad'), brand='Sulwhasoo', name='Perfecting Cushion SPF 46',
          base=749000, variants=[('17N1','17N1 Vanilla'),('21N1','21N1 Beige'),('23N1','23N1 Sand'),('25N1','25N1 Amber'),('31W1','31W1 Almond'),('33C1','33C1 Walnut')],
          description='Лёгкий кушон с SPF 46 и полуматовым финишем: выравнивает тон и маскирует несовершенства. В комплекте запасной спонж.',
          keyIngredients=['Экстракт корейских трав']),
 32: dict(romand='HAN ALL BROW CARA', brand='rom&nd', name='Han All Brow Cara', base=125000,
          variants=[('Grace Taupe','Grace Taupe'),('Mild Woody','Mild Woody'),('Modern Beige','Modern Beige'),('Merry Blondy','Merry Blondy'),('Brow Fixer','Brow Fixer (прозрачный)')],
          description='Тушь для бровей: подкрашивает и фиксирует волоски без комочков, держится весь день.',
          howTo='Снимите излишки о горлышко флакона и расчешите брови щёточкой, придавая нужную форму.'),
 33: dict(romand='BLUR FUDGE TINT', brand='rom&nd', name='Blur Fudge Tint', base=139000,
          variants=[('POMELOCO','Pomeloco'),('ROSIENTAL','Rosiental'),('MUSKY','Musky'),('RADWOOD','Radwood'),('BIBI CANDY','Bibi Candy'),('MAUVISH','Mauvish')],
          description='Матовый тинт с текстурой «помадки»: заполняет складочки губ и даёт мягкий размытый финиш. Цвет можно наслаивать.'),
 35: dict(store=('research-extra/beautyofjoseon.com-1.json','ground-rice-and-honey-glow-mask'), brand='Beauty of Joseon', name='Ground Rice and Honey Glow Mask',
          base=149000, variants=[('150','150 мл')],
          description='Смываемая маска с корейским рисом и мёдом: мягко отшелушивает, увлажняет и придаёт сияние.',
          keyIngredients=['Экстракт риса','Мёд']),
 36: dict(store=('research-extra/www.cosrx.com-1.json','cosrx-peptide-132-ultra-perfect-hair-bonding-treatment-번들'), brand='COSRX', name='Peptide-132 Hair Bonding Treatment',
          base=189000, variants=[('120mL / Single','120 мл'),('240mL / Single','240 мл')],
          description='Восстанавливающая маска для повреждённых волос с пептидом PEPTIDE-132: укрепляет, разглаживает и добавляет блеск.',
          keyIngredients=['PEPTIDE-132']),
 37: dict(store=('research-extra/www.cosrx.com-1.json','cosrx-peptide-132-ultra-perfect-hair-bonding-oil-serum-번들'), brand='COSRX', name='Peptide-132 Hair Bonding Oil Serum',
          base=189000, variants=[('Single','28 мл')],
          description='Лёгкое масло-сыворотка для волос: запечатывает кончики, защищает от повреждений и даёт блеск без утяжеления.',
          keyIngredients=['PEPTIDE-132']),
 38: dict(store=('research-extra/haruharuwonder.com-1.json','haruharuwonder-black-bamboo-nourishing-calming-hand-nail-cream-50ml'), brand='Haruharu Wonder',
          name='Black Bamboo Nourishing Calming Hand & Nail Cream', base=149000, variants=[('50ml','50 мл')],
          description='Питательный крем для рук и ногтей с бамбуком, маслом мурумуру и пантенолом. Впитывается без жирной плёнки.',
          keyIngredients=['Экстракт бамбука','Масло мурумуру','Пантенол']),
 # ---- added so the hair/body tiles show real products ----
 40: dict(store=('research-extra/www.cosrx.com-1.json','cosrx-peptide-132-ultra-perfect-hair-bonding-shampoo-번들'), brand='COSRX', name='Peptide-132 Hair Bonding Shampoo',
          base=189000, variants=[('200mL / Single','200 мл'),('400mL / Single','400 мл')], cat='hair', art='pump', palette=9,
          skin=['dry','oily','combo','sens'], stock=False, hot=False,
          description='Шампунь с PEPTIDE-132: укрепляет повреждённые волосы и мягко очищает кожу головы.',
          keyIngredients=['PEPTIDE-132']),
 41: dict(store=('research-extra/www.cosrx.com-1.json','cosrx-skin-barrier-moisturizing-body-cream'), brand='COSRX', name='Skin Barrier Moisturizing Body Cream',
          base=249000, variants=[('Default','450 мл')], cat='body', art='jar', palette=9,
          skin=['dry','sens'], stock=False, hot=False,
          description='Крем для тела и лица с пятью видами церамидов: долго увлажняет и укрепляет барьер сухой и чувствительной кожи.',
          keyIngredients=['Церамиды (5 видов)']),
}

def img_url(x):
    if isinstance(x, dict): x = x.get('src')
    if not x: return None
    return 'https:' + x if x.startswith('//') else x

def build(pid, s):
    if 'store' in s:
        path, handle = s['store']
        raw = store_product(path, handle); vendor = raw.get('vendor'); src_path = '/products/' + handle
        if path.startswith('research-extra/'):
            s.setdefault('url', 'https://' + path.split('/')[1].rsplit('-1.json', 1)[0] + src_path)
    elif 'romand' in s:
        raw = romand(s['romand']); src_path = '/products/' + raw['handle']; vendor = 'rom&nd'
    elif 'src' in s:
        raw = research(s['src']); src_path = raw.get('url'); vendor = raw.get('vendor')
    else:
        raw = None; src_path = None; vendor = None
    variants = []
    if raw:
        rv = raw['variants']
        def find(m):
            hits = [v for v in rv if re.search(m, v['title'], re.I)]
            if not hits: raise SystemExit(f'id {pid}: no variant matching {m!r} in {[v["title"] for v in rv]}')
            return hits[0]
        found = [(find(m), label) for m, label in s['variants']]
        cents = lambda v: float(v['price']) * (100 if isinstance(v['price'], str) else 1)
        base_cents = cents(found[0][0])
        skip = s.get('skip_images', [])
        for i, (v, label) in enumerate(found):
            price = s['base'] if i == 0 else round(s['base'] * cents(v) / base_cents, -3)
            variants.append({k: x for k, x in dict(label=label, price=int(price), sku=v.get('sku'), barcode=v.get('barcode'),
                                                   image=(lambda u: None if not u or any(k in u for k in skip) else u)(img_url(v.get('featured_image')))).items() if x})
    else:
        variants = [dict(label=l, price=s['base']) for l, _, _ in s['manual_variants']]
    if s.get('old'): variants[0]['old'] = s['old']
    images = []
    if raw:
        # default variant's packshot first, then the brand's gallery (skip_images drops infographics/banners)
        for u in [variants[0].get('image')] + [img_url(x) for x in raw.get('images') or []]:
            if u and u not in images and not any(k in u for k in s.get('skip_images', [])):
                images.append(u)
    out = dict(id=pid, variants=variants, description=s['description'], verified=True,
               source={k: v for k, v in dict(url=s.get('url'), store=vendor, path=src_path, checked=CHECKED).items() if v})
    for k in ('name', 'brand', 'cat', 'art', 'palette', 'skin', 'stock', 'hot', 'keyIngredients', 'howTo', 'variantGalleryOnly'):
        if k in s: out[k] = s[k]
    images += [u for u in s.get('images', []) if u not in images]  # e.g. og:image from a saved page
    if images: out['images'] = images[:6]
    return out

entries = [build(pid, s) for pid, s in sorted(SPECS.items())]
photo_dir = os.path.join(ROOT, 'images', 'products')
photos = sorted(f[:-4] for f in os.listdir(photo_dir) if f.lower().endswith('.jpg'))
js = ('// Generated by scripts/build_catalogue.py — edit the script, not this file.\n'
      '// Verified against official brand stores; UZS prices are still demo values.\n'
      '// Brand-store product photos are linked from the brands\' own servers (not copied) for this\n'
      '// private prototype. Before the site goes public, set this to false and use photos your\n'
      '// distributor approves (images/products/).\n'
      'window.HARI_BRAND_IMAGES = true;\n'
      'window.HARI_CATALOGUE = ' + json.dumps(entries, ensure_ascii=False, indent=1) + ';\n'
      '// Real product photos present in images/products/ (re-run this script after adding photos).\n'
      'window.HARI_PHOTOS = ' + json.dumps(photos) + ';\n')
with open(os.path.join(DATA, 'catalogue.js'), 'w') as f:
    f.write(js)
print(f'wrote data/catalogue.js: {len(entries)} verified products, {len(photos)} product photos')
