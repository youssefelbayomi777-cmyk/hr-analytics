# -*- coding: utf-8 -*-
import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                 Table, TableStyle, Image, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from PIL import Image as PILImage
import arabic_reshaper
from bidi.algorithm import get_display

# ============================================================
# FONT REGISTRATION
# ============================================================
pdfmetrics.registerFont(TTFont('FreeSerif', '/usr/share/fonts/truetype/freefont/FreeSerif.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerifBold', '/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerifItalic', '/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerifBoldItalic', '/usr/share/fonts/truetype/freefont/FreeSerifBoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))

registerFontFamily('FreeSerif', normal='FreeSerif', bold='FreeSerifBold',
                   italic='FreeSerifItalic', boldItalic='FreeSerifBoldItalic')

# ============================================================
# ARABIC TEXT HELPER
# ============================================================
def ar(text):
    """Reshape and reorder Arabic text for PDF rendering."""
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def ar_num(text):
    """Handle mixed Arabic + number text."""
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

# ============================================================
# LOAD DATA
# ============================================================
with open('/home/z/my-project/download/analysis_results.json', 'r') as f:
    results = json.load(f)

CHARTS_DIR = '/home/z/my-project/download/'

# ============================================================
# STYLES
# ============================================================
DARK_BLUE = colors.HexColor('#1F4E79')
LIGHT_BLUE = colors.HexColor('#D6E4F0')
HEADER_BG = colors.HexColor('#1F4E79')
ROW_ODD = colors.HexColor('#F5F5F5')
ROW_EVEN = colors.white
ACCENT = colors.HexColor('#2E86AB')

cover_title_style = ParagraphStyle(
    name='CoverTitle', fontName='FreeSerifBold', fontSize=36,
    leading=48, alignment=TA_CENTER, textColor=DARK_BLUE, spaceAfter=24
)
cover_subtitle_style = ParagraphStyle(
    name='CoverSubtitle', fontName='FreeSerif', fontSize=18,
    leading=26, alignment=TA_CENTER, textColor=colors.HexColor('#555555'), spaceAfter=36
)
cover_info_style = ParagraphStyle(
    name='CoverInfo', fontName='FreeSerif', fontSize=14,
    leading=22, alignment=TA_CENTER, textColor=colors.HexColor('#777777'), spaceAfter=12
)

h1_style = ParagraphStyle(
    name='H1Arabic', fontName='FreeSerifBold', fontSize=20,
    leading=28, alignment=TA_RIGHT, textColor=DARK_BLUE,
    spaceBefore=18, spaceAfter=12
)
h2_style = ParagraphStyle(
    name='H2Arabic', fontName='FreeSerifBold', fontSize=15,
    leading=22, alignment=TA_RIGHT, textColor=colors.HexColor('#2C5F8A'),
    spaceBefore=14, spaceAfter=8
)
h3_style = ParagraphStyle(
    name='H3Arabic', fontName='FreeSerifBold', fontSize=12,
    leading=18, alignment=TA_RIGHT, textColor=colors.HexColor('#34495E'),
    spaceBefore=10, spaceAfter=6
)
body_style = ParagraphStyle(
    name='BodyArabic', fontName='FreeSerif', fontSize=11,
    leading=20, alignment=TA_RIGHT, textColor=colors.black,
    spaceBefore=2, spaceAfter=6
)
body_center_style = ParagraphStyle(
    name='BodyCenter', fontName='FreeSerif', fontSize=11,
    leading=20, alignment=TA_CENTER, textColor=colors.black,
    spaceBefore=2, spaceAfter=6
)
bullet_style = ParagraphStyle(
    name='BulletArabic', fontName='FreeSerif', fontSize=11,
    leading=20, alignment=TA_RIGHT, textColor=colors.black,
    spaceBefore=2, spaceAfter=4, rightIndent=15
)
caption_style = ParagraphStyle(
    name='Caption', fontName='FreeSerif', fontSize=10,
    leading=14, alignment=TA_CENTER, textColor=colors.HexColor('#555555'),
    spaceBefore=4, spaceAfter=8
)
tbl_header_style = ParagraphStyle(
    name='TblHeader', fontName='FreeSerifBold', fontSize=10,
    leading=14, alignment=TA_CENTER, textColor=colors.white
)
tbl_cell_style = ParagraphStyle(
    name='TblCell', fontName='FreeSerif', fontSize=10,
    leading=14, alignment=TA_CENTER, textColor=colors.black
)
tbl_cell_right = ParagraphStyle(
    name='TblCellRight', fontName='FreeSerif', fontSize=10,
    leading=14, alignment=TA_RIGHT, textColor=colors.black
)
kpi_val_style = ParagraphStyle(
    name='KPIVal', fontName='FreeSerifBold', fontSize=22,
    leading=28, alignment=TA_CENTER, textColor=DARK_BLUE
)
kpi_label_style = ParagraphStyle(
    name='KPILabel', fontName='FreeSerif', fontSize=10,
    leading=14, alignment=TA_CENTER, textColor=colors.HexColor('#555555')
)

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def add_image(story, img_path, max_width=460, caption_text=None):
    """Add an image with optional caption."""
    if os.path.exists(img_path):
        pil_img = PILImage.open(img_path)
        orig_w, orig_h = pil_img.size
        scale = min(max_width / orig_w, 1.0)
        img = Image(img_path, width=orig_w * scale, height=orig_h * scale)
        img.hAlign = 'CENTER'
        story.append(img)
        if caption_text:
            story.append(Spacer(1, 4))
            story.append(Paragraph(ar(caption_text), caption_style))

def make_table(headers, rows, col_widths=None):
    """Create a styled table with Arabic headers."""
    data = []
    header_row = [Paragraph(ar(h), tbl_header_style) for h in headers]
    data.append(header_row)
    for row in rows:
        data.append([Paragraph(str(v), tbl_cell_style) for v in row])
    
    if col_widths is None:
        w = 480 / len(headers)
        col_widths = [w] * len(headers)
    
    t = Table(data, colWidths=col_widths)
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        bg = ROW_EVEN if i % 2 == 1 else ROW_ODD
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))
    t.setStyle(TableStyle(style_cmds))
    t.hAlign = 'CENTER'
    return t

# ============================================================
# BUILD PDF
# ============================================================
output_path = '/home/z/my-project/download/HR_Analysis_Report.pdf'
pdf_title = os.path.splitext(os.path.basename(output_path))[0]

doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    title=pdf_title,
    author='Z.ai',
    creator='Z.ai',
    subject='HR Analytics Report - Comprehensive Employee Data Analysis',
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm
)

story = []

# ============================================================
# COVER PAGE
# ============================================================
story.append(Spacer(1, 100))
story.append(Paragraph(ar('تقرير تحليل الموارد البشرية الشامل'), cover_title_style))
story.append(Spacer(1, 24))
story.append(Paragraph(ar('تحليل بيانات الموظفين ومؤشرات الأداء الرئيسية'), cover_subtitle_style))
story.append(Spacer(1, 36))

# Decorative line
line_data = [['']]
line_table = Table(line_data, colWidths=[300])
line_table.setStyle(TableStyle([
    ('LINEABOVE', (0, 0), (-1, 0), 3, ACCENT),
    ('TOPPADDING', (0, 0), (-1, -1), 0),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
]))
line_table.hAlign = 'CENTER'
story.append(line_table)

story.append(Spacer(1, 48))
story.append(Paragraph(ar('إعداد: قسم تحليل البيانات'), cover_info_style))
story.append(Paragraph(ar('التاريخ: أبريل 2026'), cover_info_style))
story.append(Spacer(1, 24))
story.append(Paragraph(ar('عدد الموظفين: 50 | عدد الأقسام: 8'), cover_info_style))
story.append(PageBreak())

# ============================================================
# TABLE OF CONTENTS
# ============================================================
story.append(Paragraph(ar('جدول المحتويات'), h1_style))
story.append(Spacer(1, 18))

toc_items = [
    ar('1. ملخص تنفيذي'),
    ar('2. تنظيف البيانات والتحقق من الجودة'),
    ar('3. التحليل الاستكشافي للبيانات'),
    ar('4. مؤشرات الأداء الرئيسية'),
    ar('5. تحليل الأقسام'),
    ar('6. التحليل التنبؤي للدوران الوظيفي'),
    ar('7. الرؤى الأساسية والتوصيات'),
]
for item in toc_items:
    story.append(Paragraph(item, body_style))
    story.append(Spacer(1, 6))

story.append(PageBreak())

# ============================================================
# SECTION 1: EXECUTIVE SUMMARY
# ============================================================
story.append(Paragraph(ar('1. ملخص تنفيذي'), h1_style))
story.append(Spacer(1, 12))

exec_summary = ar(
    'يقدم هذا التقرير تحليلا شاملا لبيانات الموارد البشرية الخاصة بالمنظمة، '
    'ويغطي 50 موظفا موزعين على 8 أقسام. يهدف التقرير الى تقديم رؤى عميقة حول '
    'معدلات الغياب وساعات العمل الاضافي وتقييمات الاداء ومستوى الرضا الوظيفي '
    'ومعدلات دوران الموظفين. كما يتضمن تحليلا تنبؤيا باستخدام نماذج التعلم الالي '
    'لتحديد العوامل المؤثرة في احتمالية مغادرة الموظفين للمنظمة.'
)
story.append(Paragraph(exec_summary, body_style))
story.append(Spacer(1, 12))

# KPI Summary Table
story.append(Paragraph(ar('ملخص المؤشرات الرئيسية'), h2_style))
story.append(Spacer(1, 8))

kpis = results['kpis']
kpi_data = [
    [ar('القيمة'), ar('المؤشر')],
    [f"{kpis['overall_absence_rate']}%", ar('معدل الغياب الشهري')],
    [f"{kpis['avg_performance']} / 5", ar('متوسط تقييم الاداء')],
    [f"{kpis['avg_satisfaction']} / 10", ar('متوسط درجة الرضا')],
    [f"{kpis['turnover_rate_3y']}%", ar('معدل الدوران الوظيفي - 3 سنوات')],
    [f"{kpis['avg_overtime']} ", ar('متوسط ساعات العمل الاضافي')],
    [f"{kpis['avg_tenure']} ", ar('متوسط سنوات الخدمة')],
]
kpi_table_data = []
for row in kpi_data:
    kpi_table_data.append([Paragraph(row[0], tbl_cell_style), Paragraph(row[1], tbl_cell_style)])

kpi_t = Table(kpi_table_data, colWidths=[200, 280])
kpi_style_cmds = [
    ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]
for i in range(1, len(kpi_table_data)):
    bg = ROW_EVEN if i % 2 == 1 else ROW_ODD
    kpi_style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))
kpi_t.setStyle(TableStyle(kpi_style_cmds))
kpi_t.hAlign = 'CENTER'
story.append(kpi_t)
story.append(Spacer(1, 6))
story.append(Paragraph(ar('جدول 1: ملخص مؤشرات الاداء الرئيسية للموارد البشرية'), caption_style))
story.append(Spacer(1, 12))

# Add KPI summary image
add_image(story, os.path.join(CHARTS_DIR, 'chart7_kpi_summary.png'), max_width=460,
          caption_text='شكل 1: لوحة ملخص مؤشرات الاداء الرئيسية')

# ============================================================
# SECTION 2: DATA CLEANING
# ============================================================
story.append(Spacer(1, 18))
story.append(Paragraph(ar('2. تنظيف البيانات والتحقق من الجودة'), h1_style))
story.append(Spacer(1, 12))

cleaning_text1 = ar(
    'تم اجراء عملية فحص شاملة لجودة البيانات قبل بدء التحليل. تضمنت العملية التحقق '
    'من صحة التنسيقات والقيم المفقودة وتوحيد التسميات. اظهرت النتائج ان مجموعة البيانات '
    'تحتوي على 50 سجلا خاصا بالموظفين عبر 9 اعمدة بيانات، وان جميع التواريخ بصيغة '
    'مقبولة وقابلة للتحويل التلقائي دون اخطاء.'
)
story.append(Paragraph(cleaning_text1, body_style))
story.append(Spacer(1, 8))

cleaning_text2 = ar(
    'لم يتم رصد اي قيم مفقودة في اي من الاعمدة التسعة، مما يشير الى جودة عالية في '
    'عملية جمع البيانات. كما تم التحقق من عدم وجود سجلات مكررة بناء على معرف '
    'الموظف، ووجد ان جميع المعرفات فريدة. تتضمن مجموعة البيانات 8 اقسام موحدة '
    'باسمائها الانجليزية القياسية وهي: خدمة العملاء والهندسة والعمليات والمالية '
    'وتقنية المعلومات والمبيعات والتسويق والموارد البشرية.'
)
story.append(Paragraph(cleaning_text2, body_style))
story.append(Spacer(1, 8))

cleaning_text3 = ar(
    'تمت اضافة عمودين جديدين هما: سنوات الخدمة المحسوبة من تاريخ التعيين، وعلامة '
    'الدوران الوظيفي التي تشير الى ما اذا كان الموظف قد غادر المنظمة مرة واحدة '
    'على الاقل خلال السنوات الثلاث الماضية. اتضح ان 72% من الموظفين لديهم سجل '
    'دوران وظيفي واحد على الاقل.'
)
story.append(Paragraph(cleaning_text3, body_style))
story.append(Spacer(1, 12))

# Data Quality Summary Table
quality_data = [
    [ar('الحالة'), ar('البند')],
    ['50', ar('عدد السجلات')],
    ['9', ar('عدد الاعمدة')],
    ['0', ar('القيم المفقودة')],
    ['0', ar('السجلات المكررة')],
    ['8', ar('عدد الاقسام')],
    [ar('نظيفة وموحدة'), ar('تنسيقات التواريخ')],
    [ar('1.0 - 10.0'), ar('نطاق درجات الرضا')],
    [ar('1.0 - 5.0'), ar('نطاق تقييمات الاداء')],
]
quality_rows = []
for row in quality_data:
    quality_rows.append([Paragraph(row[0], tbl_cell_style), Paragraph(row[1], tbl_cell_style)])
qt = Table(quality_rows, colWidths=[200, 280])
qt_style = [
    ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
]
for i in range(1, len(quality_rows)):
    bg = ROW_EVEN if i % 2 == 1 else ROW_ODD
    qt_style.append(('BACKGROUND', (0, i), (-1, i), bg))
qt.setStyle(TableStyle(qt_style))
qt.hAlign = 'CENTER'
story.append(qt)
story.append(Spacer(1, 6))
story.append(Paragraph(ar('جدول 2: ملخص جودة البيانات'), caption_style))

# ============================================================
# SECTION 3: EDA
# ============================================================
story.append(Spacer(1, 18))
story.append(Paragraph(ar('3. التحليل الاستكشافي للبيانات'), h1_style))
story.append(Spacer(1, 12))

story.append(Paragraph(ar('3.1 الاحصائيات الوصفية'), h2_style))
story.append(Spacer(1, 8))

eda_text1 = ar(
    'يوضح الجدول التالي الاحصائيات الوصفية لجميع المتغيرات العددية في مجموعة البيانات. '
    'يبلغ متوسط معدل الغياب الشهري 3.04% بانحراف معياري 1.14، مما يشير الى تباين '
    'معتدل في معدلات الغياب بين الموظفين. اما متوسط ساعات العمل الاضافي فهو 12.36 '
    'ساعة شهريا بانحراف معياري 4.26 ساعة. ويسجل متوسط تقييم الاداء 3.10 من 5 '
    'بينما يبلغ متوسط الرضا الوظيفي 4.76 من 10.'
)
story.append(Paragraph(eda_text1, body_style))
story.append(Spacer(1, 8))

# Descriptive stats table
stats = results['descriptive_stats']
stat_headers = [ar('الانحراف المعياري'), ar('المتوسط'), ar('الوسيط'), ar('المؤشر')]
stat_rows = []
metric_map = {
    'Monthly_Absence_Rate': 'معدل الغياب الشهري (%)',
    'Overtime_Hours': 'ساعات العمل الاضافي',
    'Performance_Rating': 'تقييم الاداء (1-5)',
    'Satisfaction': 'الرضا الوظيفي (1-10)',
    'Turnover_3Y': 'الدوران الوظيفي (3 سنوات)',
    'Tenure_Years': 'سنوات الخدمة'
}
for key, label in metric_map.items():
    s = stats.get(key, {})
    stat_rows.append([
        f"{s.get('std', 0):.2f}",
        f"{s.get('mean', 0):.2f}",
        f"{s.get('median', 0):.2f}",
        ar(label)
    ])
stat_table = make_table(stat_headers, stat_rows, col_widths=[100, 100, 100, 180])
story.append(stat_table)
story.append(Spacer(1, 6))
story.append(Paragraph(ar('جدول 3: الاحصائيات الوصفية للمتغيرات العددية'), caption_style))
story.append(Spacer(1, 14))

# Distribution charts
story.append(Paragraph(ar('3.2 توزيعات المتغيرات الرئيسية'), h2_style))
story.append(Spacer(1, 8))

eda_text2 = ar(
    'تظهر المخططات التالية توزيعات ثلاثة متغيرات رئيسية: معدل الغياب الشهري وساعات '
    'العمل الاضافي ودرجات الرضا الوظيفي. يتبين من مخطط الغياب ان التوزيع يميل '
    'الى الطبيعية مع تركز حول القيمة 3%. اما ساعات العمل الاضافي فتظهر توزيعا '
    'واسعا نسبيا بين 5 و20 ساعة. في حين يظهر توزيع الرضا تركزا واضحا عند '
    'القيم المتطرفة (1 و10) مما يشير الى استقطاب في مستوى الرضا.'
)
story.append(Paragraph(eda_text2, body_style))
story.append(Spacer(1, 8))

add_image(story, os.path.join(CHARTS_DIR, 'chart1_distributions.png'), max_width=470,
          caption_text='شكل 2: توزيعات الغياب والعمل الاضافي والرضا')
story.append(Spacer(1, 14))

# Correlation
story.append(Paragraph(ar('3.3 تحليل الارتباطات'), h2_style))
story.append(Spacer(1, 8))

corr = results['correlation']
corr_text = ar(
    'يكشف تحليل الارتباط بين المتغيرات عن عدة نتائج مهمة. يوجد ارتباط سلبي طفيف '
    'بين الرضا الوظيفي ومعدل الغياب حيث يبلغ معامل الارتباط -0.253، مما يعني ان '
    'الموظفين الاكثر رضا يميلون الى الغياب اقل. كما يوجد ارتباط سلبي بين الرضا '
    'والدوران الوظيفي بقيمة -0.145. من ناحية اخرى يوجد ارتباط ايجابي بين '
    'الاداء وسنوات الخدمة بقيمة 0.228 مما يشير الى ان الموظفين ذوي الخبرة '
    'الاطول يميلون الى تحقيق اداء افضل.'
)
story.append(Paragraph(corr_text, body_style))
story.append(Spacer(1, 8))

add_image(story, os.path.join(CHARTS_DIR, 'chart2_correlation.png'), max_width=380,
          caption_text='شكل 3: مصفوفة الارتباط بين المتغيرات')

# ============================================================
# SECTION 4: KPIs
# ============================================================
story.append(Spacer(1, 18))
story.append(Paragraph(ar('4. مؤشرات الأداء الرئيسية'), h1_style))
story.append(Spacer(1, 12))

story.append(Paragraph(ar('4.1 معدلات الغياب'), h2_style))
story.append(Spacer(1, 8))

absence_text = ar(
    'يبلغ معدل الغياب الشهري العام للمنظمة 3.04% وهو معدل معتدل. تعتبر تقنية '
    'المعلومات الاعلى في الغياب بمتوسط 3.50% تليها المبيعات بنسبة 3.36% ثم '
    'العمليات بنسبة 3.15%. اما الاقل غيابا فهي قسم التسويق بنسبة 2.40% ثم '
    'المالية بنسبة 2.52% ثم الهندسة بنسبة 2.63%. يشير هذا التباين الى اختلاف '
    'طبيعة العمل والضغوط بين الاقسام المختلفة.'
)
story.append(Paragraph(absence_text, body_style))
story.append(Spacer(1, 8))

# Absence by department table
absence_dept = results['absence_by_dept']
abs_headers = [ar('القسم'), ar('معدل الغياب (%)')]
abs_rows = []
for dept, val in absence_dept.items():
    abs_rows.append([ar(dept), f"{val:.2f}"])
abs_table = make_table(abs_headers, abs_rows, col_widths=[300, 180])
story.append(abs_table)
story.append(Spacer(1, 6))
story.append(Paragraph(ar('جدول 4: معدل الغياب حسب القسم'), caption_style))
story.append(Spacer(1, 14))

story.append(Paragraph(ar('4.2 تقييمات الأداء حسب القسم'), h2_style))
story.append(Spacer(1, 8))

perf_text = ar(
    'يحقق قسم التسويق اعلى متوسط لتقييم الاداء بمقدار 4.67 من 5 يليه المبيعات '
    'بمعدل 3.80 ثم الموارد البشرية بمعدل 3.38. في المقابل يسجل كل من قسمي '
    'الهندسة والمالية ادنى متوسط اداء بمقدار 2.50. يستحق هذا التباين دراسة '
    'مفصلة لفهم الاسباب الكامنة وراء تدني الاداء في هذين القسمين رغم ان '
    'الهندسة تمتلك متوسط ساعات عمل اضافي مرتفع يبلغ 13.67 ساعة.'
)
story.append(Paragraph(perf_text, body_style))
story.append(Spacer(1, 8))

# Performance by department table
perf_dept = results['performance_by_dept']
perf_headers = [ar('القسم'), ar('متوسط الاداء (1-5)')]
perf_rows = []
for dept, val in perf_dept.items():
    perf_rows.append([ar(dept), f"{val:.2f}"])
perf_table = make_table(perf_headers, perf_rows, col_widths=[300, 180])
story.append(perf_table)
story.append(Spacer(1, 6))
story.append(Paragraph(ar('جدول 5: متوسط تقييم الاداء حسب القسم'), caption_style))
story.append(Spacer(1, 14))

story.append(Paragraph(ar('4.3 معدل الدوران الوظيفي'), h2_style))
story.append(Spacer(1, 8))

turnover_text = ar(
    'يبلغ معدل دوران الموظفين خلال السنوات الثلاث الماضية 72% وهو معدل مرتفع '
    'يستدعي اهتماما خاصا. يعني هذا ان 36 من اصل 50 موظفا قد غادروا المنظمة '
    'مرة واحدة على الاقل. يتصدر قسم العمليات قائمة الدوران بمتوسط 1.75 مرة '
    'يليه المبيعات بمعدل 1.60 مرة ثم الهندسة بمعدل 1.50 مرة. يعد ارتفاع '
    'الدوران تكلفة كبيرة على المنظمة من حيث تكاليف التوظيف والتدريب وفقدان '
    'المعرفة التنظيمية.'
)
story.append(Paragraph(turnover_text, body_style))
story.append(Spacer(1, 14))

story.append(Paragraph(ar('4.4 العلاقة بين العمل الإضافي والرضا'), h2_style))
story.append(Spacer(1, 8))

ot_text = ar(
    'يكشف التحليل عن ارتباط ضعيف جدا بين ساعات العمل الاضافي ومستوى الرضا '
    'حيث يبلغ معامل الارتباط 0.052 فقط. هذا يعني ان زيادة ساعات العمل الاضافي '
    'لا تؤثر بشكل مباشر على مستوى رضا الموظفين بشكل كبير. ومع ذلك عند تقسيم '
    'الموظفين الى ثلاث فئات حسب ساعات العمل الاضافي نجد ان الفئة ذات العمل '
    'الاضافي المرتفع (16+ ساعة) تمتلك اعلى متوسط رضا بمقدار 5.43 مقارنة '
    'بالفئة المتوسطة (4.25) والمنخفضة (4.70). قد يعكس ذلك حصول الموظفين '
    'ذوي العمل الاضافي المرتفع على تعويضات مادية اضافية.'
)
story.append(Paragraph(ot_text, body_style))
story.append(Spacer(1, 8))

add_image(story, os.path.join(CHARTS_DIR, 'chart5_ot_vs_sat.png'), max_width=420,
          caption_text='شكل 4: العلاقة بين ساعات العمل الاضافي والرضا الوظيفي')

# ============================================================
# SECTION 5: DEPARTMENT ANALYSIS
# ============================================================
story.append(Spacer(1, 18))
story.append(Paragraph(ar('5. تحليل الأقسام'), h1_style))
story.append(Spacer(1, 12))

dept_text1 = ar(
    'يوفر هذا القسم تحليلا مفصلا لاداء الاقسام الثمانية في المنظمة من حيث '
    'معدلات الغياب والاداء والرضا والدوران الوظيفي وسنوات الخدمة. يتبين من '
    'التحليل ان هناك تباينا واضحا بين الاقسام في جميع المؤشرات مما يتطلب '
    'استراتيجيات مخصصة لكل قسم لتحسين الاداء العام.'
)
story.append(Paragraph(dept_text1, body_style))
story.append(Spacer(1, 8))

# Department comprehensive table
dept_stats = results['department_stats']
dept_headers = [ar('الخدمة'), ar('الغياب'), ar('الرضا'), ar('الاداء'), ar('الدوران'), ar('العدد'), ar('القسم')]
dept_rows = []
for dept in sorted(dept_stats.keys()):
    d = dept_stats[dept]
    dept_rows.append([
        f"{d['Avg_Tenure']:.1f}",
        f"{d['Avg_Turnover']:.1f}",
        f"{d['Avg_Satisfaction']:.1f}",
        f"{d['Avg_Performance']:.1f}",
        f"{d['Avg_Absence']:.1f}",
        str(d['Count']),
        ar(dept)
    ])
dept_table = make_table(dept_headers, dept_rows, col_widths=[60, 60, 60, 60, 60, 50, 130])
story.append(dept_table)
story.append(Spacer(1, 6))
story.append(Paragraph(ar('جدول 6: مقارنة شاملة لمؤشرات الاقسام'), caption_style))
story.append(Spacer(1, 12))

add_image(story, os.path.join(CHARTS_DIR, 'chart3_departments.png'), max_width=470,
          caption_text='شكل 5: تحليل الاداء حسب القسم - الغياب والاداء والرضا والدوران')
story.append(Spacer(1, 8))

add_image(story, os.path.join(CHARTS_DIR, 'chart8_boxplots.png'), max_width=470,
          caption_text='شكل 6: المخططات الصندوقية لتوزيع المؤشرات حسب القسم')

# ============================================================
# SECTION 6: PREDICTIVE ANALYSIS
# ============================================================
story.append(Spacer(1, 18))
story.append(Paragraph(ar('6. التحليل التنبؤي للدوران الوظيفي'), h1_style))
story.append(Spacer(1, 12))

pred_text1 = ar(
    'تم بناء نموذجين للتنبؤ باحتمالية دوران الموظفين باستخدام خوارزميات التعلم '
    'الالي. النموذج الاول هو الانحدار اللوجستي والثاني هو شجرة القرار. تم استخدام '
    'خمسة متغيرات تنبؤية هي: معدل الغياب وساعات العمل الاضافي وتقييم الاداء '
    'ومستوى الرضا وسنوات الخدمة.'
)
story.append(Paragraph(pred_text1, body_style))
story.append(Spacer(1, 8))

pred = results['predictive']
model_headers = [ar('الدقة'), ar('النموذج')]
model_rows = [
    [f"{pred['logistic_regression_accuracy']:.1%}", ar('الانحدار اللوجستي')],
    [f"{pred['decision_tree_accuracy']:.1%}", ar('شجرة القرار')],
]
model_table = make_table(model_headers, model_rows, col_widths=[200, 280])
story.append(model_table)
story.append(Spacer(1, 6))
story.append(Paragraph(ar('جدول 7: دقة النماذج التنبؤية'), caption_style))
story.append(Spacer(1, 12))

story.append(Paragraph(ar('6.1 اهمية المتغيرات التنبؤية'), h2_style))
story.append(Spacer(1, 8))

feat_text = ar(
    'يكشف تحليل اهمية المتغيرات في نموذج شجرة القرار ان سنوات الخدمة هي العامل '
    'الاكثر تاثيرا في الدوران الوظيفي بنسبة اهمية 34.45%، يليه معدل الغياب '
    'بنسبة 28.48%. هذا يعني ان الموظفين الجدد والذين لديهم معدلات غياب مرتفعة '
    'هم الاكثر عرضة لمغادرة المنظمة. تاتي تقييمات الاداء في المرتبة الثالثة '
    'بنسبة 14.02% مما يؤكد اهمية متابعة وتحسين اداء الموظفين.'
)
story.append(Paragraph(feat_text, body_style))
story.append(Spacer(1, 8))

# Feature importance table
fi = pred['feature_importance']
fi_headers = [ar('الاهمية'), ar('المتغير')]
fi_map = {
    'Tenure_Years': 'سنوات الخدمة',
    'Monthly_Absence_Rate': 'معدل الغياب',
    'Performance_Rating': 'تقييم الاداء',
    'Overtime_Hours': 'ساعات العمل الاضافي',
    'Satisfaction': 'الرضا الوظيفي'
}
fi_rows = []
for feat, imp in sorted(fi.items(), key=lambda x: -x[1]):
    fi_rows.append([f"{imp:.2%}", ar(fi_map.get(feat, feat))])
fi_table = make_table(fi_headers, fi_rows, col_widths=[200, 280])
story.append(fi_table)
story.append(Spacer(1, 6))
story.append(Paragraph(ar('جدول 8: اهمية المتغيرات في نموذج شجرة القرار'), caption_style))
story.append(Spacer(1, 12))

# LR Coefficients
story.append(Paragraph(ar('6.2 معاملات الانحدار اللوجستي'), h2_style))
story.append(Spacer(1, 8))

lr_text = ar(
    'يوضح تحليل معاملات الانحدار اللوجستي اتجاه تاثير كل متغير. يظهر ان سنوات '
    'الخدمة (0.512) وساعات العمل الاضافي (0.328) وتقييم الاداء (0.459) لها '
    'تاثير ايجابي على احتمالية الدوران. بينما معدل الغياب (-0.555) والرضا '
    '(-0.265) لهما تاثير سلبي. قد يبدو هذا متناقضا لكنه يعكس ان الموظفين '
    'الذين قضوا فترة اطول في المنظمة هم من يميلون الى الانتقال الى فرص اخرى.'
)
story.append(Paragraph(lr_text, body_style))
story.append(Spacer(1, 8))

lr = pred['lr_coefficients']
lr_headers = [ar('المعامل'), ar('التاثير'), ar('المتغير')]
lr_rows = []
for feat, coef in lr.items():
    direction = ar('سلبي') if coef < 0 else ar('ايجابي')
    lr_rows.append([f"{coef:.4f}", direction, ar(fi_map.get(feat, feat))])
lr_table = make_table(lr_headers, lr_rows, col_widths=[120, 120, 240])
story.append(lr_table)
story.append(Spacer(1, 6))
story.append(Paragraph(ar('جدول 9: معاملات نموذج الانحدار اللوجستي'), caption_style))
story.append(Spacer(1, 12))

add_image(story, os.path.join(CHARTS_DIR, 'chart6_feature_importance.png'), max_width=470,
          caption_text='شكل 7: اهمية المتغيرات في النماذج التنبؤية')

# ============================================================
# SECTION 7: INSIGHTS & RECOMMENDATIONS
# ============================================================
story.append(Spacer(1, 18))
story.append(Paragraph(ar('7. الرؤى الأساسية والتوصيات'), h1_style))
story.append(Spacer(1, 12))

story.append(Paragraph(ar('7.1 الرؤى الخمس الأساسية'), h2_style))
story.append(Spacer(1, 8))

insights = [
    ('القسم الاكثر تعرضا للدوران',
     'يعاني قسم العمليات من اعلى معدل دوران وظيفي بمتوسط 1.75 مرة خلال 3 سنوات '
     'مما يشكل مخاطرة حقيقية على استمرارية العمليات. كما يمتلك هذا القسم ثاني '
     'اعلى معدل غياب بنسبة 3.15% وثاني اقل تقييم اداء بمقدار 2.75 من 5. يتطلب '
     'هذا القسم تدخلا عاجلا لفهم اسباب الاستياء وتحسين بيئة العمل.'),
    ('الرضا الوظيفي المنخفض في قسم الهندسة',
     'رغم ان قسم الهندسة يحظى بمتوسط ساعات عمل اضافي مرتفع يبلغ 13.67 ساعة شهريا '
     'الا ان متوسط الرضا الوظيفي فيه هو 4.67 من 10 فقط. هذا التناقض يشير الى ان '
     'التعويضات المالية وحدها لا تكفي لضمان رضا الموظفين ويجب العمل على تحسين '
     'عوامل اخرى مثل التوازن بين العمل والحياة والتطوير المهني.'),
    ('الاستقطاب في درجات الرضا',
     'يظهر توزيع درجات الرضا تركيزا واضحا عند القيم المتطرفة (1 و10) مع انحراف '
     'معياري مرتفع يبلغ 3.16 من 10. يعكس هذا وجود فجوة كبيرة بين الموظفين الراضين '
     'جدا والذين يعانون من عدم الرضا مما يتطلب استراتيجيات مختلفة لكل فئة.'),
    ('تاثير سنوات الخدمة على الدوران',
     'اثبت التحليل التنبؤي ان سنوات الخدمة هي العامل الاكثر تاثيرا على الدوران '
     'الوظيفي بنسبة اهمية 34.45%. الموظفون الذين تقل خبرتهم عن 6 سنوات هم الاكثر '
     'عرضة للمغادرة. كما ان الموظفين ذوي الخبرة الطويلة (اكثر من 8 سنوات) اقل '
     'عرضة للدوران مما يؤكد اهمية برامج الاحتفاظ بالمواهب الجديدة.'),
    ('ضعف الارتباط بين العمل الاضافي والرضا',
     'يكشف معامل الارتباط المنخفض (0.052) بين ساعات العمل الاضافي والرضا ان زيادة '
     'ساعات العمل لا تعني بالضرورة انخفاض الرضا بشكل كبير. الملاحظ ان فئة العمل '
     'الاضافي المرتفع تمتلك اعلى رضا مما قد يعكس فعالية سياسات التعويض عن العمل الاضافي.'),
]

for i, (title, text) in enumerate(insights, 1):
    story.append(Paragraph(ar(f'{i}. {title}'), h3_style))
    story.append(Paragraph(ar(text), body_style))
    story.append(Spacer(1, 8))

story.append(Spacer(1, 12))
story.append(Paragraph(ar('7.2 التوصيات العملية'), h2_style))
story.append(Spacer(1, 8))

recs = [
    ('تحسين بيئة العمل في قسم العمليات',
     'نوصي باجراء مقابلات خروج مفصلة للموظفين المغادرين من قسم العمليات وتحليل '
     'النتائج لتحديد الاسباب الجذرية. يجب ايضا مراجعة الحمل العملية وتوزيع المهام '
     'وتوفير موارد اضافية ان لزم الامر. ننصح بتنفيذ برنامج تحفيز شهري لتحسين '
     'معنويات فريق العمل وتقليل معدل الدوران.'),
    ('تعزيز الرضا في قسم الهندسة',
     'يجب اطلاق برامج تطوير مهني متخصصة لمهندسي المنظمة تشمل التدريب المتقدم '
     'والمؤتمرات وشهادات الاحتراف. كما نوصي بتوفير مرونة اكبر في ساعات العمل '
     'ومراجعة نظام التقييم الحالي لضمان العدالة. يمكن ايضا انشاء مسارات ترقية '
     'واضحة لتعزيز شعور الموظفين بالنمو المهني.'),
    ('برامج احتفاظ بالمواهب الجديدة',
     'بما ان الموظفين الجدد هم الاكثر عرضة للدوران نقترح تصميم برنامج توجيه '
     'مهني يربط الموظفين الجدد بمرشدين ذوي خبرة. يجب ايضا توفير خطة تطوير '
     'فردية لكل موظف جديد مع متابعة دورية خلال اول سنتين من الخدمة.'),
    ('معالجة الاستقطاب في الرضا',
     'نوصي بتقسيم الموظفين الى فئات حسب مستوى الرضا وتصميم استراتيجيات مخصصة. '
     'للفئة غير الراضية يجب اجراء مقابلات فردية لفهم التحديات. للفئة الراضية يجب '
     'تعزيز العوامل الايجابية وتحويلهم الى سفراء للمنظمة.'),
    ('تحسين متوسط تقييمات الاداء',
     'بما ان متوسط تقييم الاداء العام هو 3.10 من 5 فقط نقترح مراجعة معايير التقييم '
     'واضافة اهداف واضحة وقابلة للقياس. يجب ايضا توفير تغذية راجعة مستمرة بدلا من '
     'التقييم السنوي فقط وتدريب المديرين على مهارات التقييم العادل والبناء.'),
]

for i, (title, text) in enumerate(recs, 1):
    story.append(Paragraph(ar(f'{i}. {title}'), h3_style))
    story.append(Paragraph(ar(text), body_style))
    story.append(Spacer(1, 8))

# Satisfaction vs Performance chart
story.append(Spacer(1, 12))
add_image(story, os.path.join(CHARTS_DIR, 'chart4_sat_vs_perf.png'), max_width=420,
          caption_text='شكل 8: العلاقة بين الرضا والاداء ملونة حسب الدوران')

# ============================================================
# BUILD
# ============================================================
doc.build(story)
print(f"PDF saved: {output_path}")

