# HR Analytics Dashboard | لوحة تحليلات الموارد البشرية

<div align="center">

![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4-38B2AC?logo=tailwindcss)
![shadcn/ui](https://img.shields.io/badge/shadcn/ui-latest-black)
![Python](https://img.shields.io/badge/Python-3.12-yellow?logo=python)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-orange?logo=scikit-learn)
[![Vercel](https://img.shields.io/badge/Vercel-deployed-success?logo=vercel)](https://hr-analytics-roan.vercel.app)
![GitHub](https://img.shields.io/badge/GitHub-hosted-success?logo=github)

**لوحة تحكم تفاعلية لتحليل بيانات الموارد البشرية مع تحليل تنبؤي باستخدام التعلم الآلي**

[English](#english) | [العربية](#arabic)

</div>

---

## 🇸🇦 العربية

### 📋 نبذة عن المشروع

مشروع تحليل شامل لبيانات الموارد البشرية يغطي 50 موظفاً عبر 8 أقسام. يتضمن تنظيف البيانات، تحليل استكشافي، مؤشرات أداء رئيسية، تحليل تنبؤي للدوران الوظيفي، وتصورات بيانية تفاعلية.

### ✨ المميزات

- ** تنظيف البيانات**: التحقق من صحة التنسيقات، معالجة القيم المفقودة، توحيد التسميات
- **تحليل استكشافي (EDA)**: إحصائيات وصفية، مصفوفة الارتباط، توزيعات المتغيرات
- **مؤشرات الأداء (KPIs)**: الغياب، الأداء، الرضا، الدوران الوظيفي، الأوفرايم
- **تحليل تنبؤي**: Logistic Regression + Decision Tree مع Feature Importance
- **لوحة تحكم تفاعلية**: 4 تبويبات (مقاييس عامة، أقسام، رضا vs أداء، تنبؤي)
- **تقرير PDF شامل**: مع 9 جداول و8 أشكال بيانية
- **تصميم RTL**: دعم كامل للغة العربية

### 🛠️ التقنيات المستخدمة

| التقنية | الاستخدام |
|---------|-----------|
| Next.js 16 + TypeScript | واجهة الويب التفاعلية |
| Tailwind CSS 4 + shadcn/ui | التصميم والتنسيق |
| Recharts | المخططات البيانية التفاعلية |
| Python + Pandas | تحليل البيانات |
| scikit-learn | النماذج التنبؤية |
| Matplotlib + Seaborn | التصورات البيانية |
| ReportLab | إنشاء تقرير PDF |
| openpyxl | تحديث ملف Excel |

### 📂 هيكل المشروع

```
hr-analytics-dashboard/
├── src/
│   ├── app/
│   │   ├── layout.tsx          # التخطيط الرئيسي (RTL)
│   │   ├── page.tsx            # لوحة التحكم الرئيسية
│   │   └── globals.css         # الأنماط العامة
│   ├── components/ui/          # مكونات shadcn/ui
│   ├── hooks/                  # React Hooks
│   └── lib/                    # أدوات مساعدة
├── public/
│   └── charts/                 # المخططات البيانية (8 PNG)
├── python-analysis/            # سكريبتات التحليل
│   ├── analysis.py             # التحليل الرئيسي
│   ├── create_excel.py         # إنشاء Excel
│   └── generate_pdf.py         # إنشاء PDF
├── download/                   # الملفات الناتجة
│   ├── HR_Analysis_Report.pdf
│   ├── HR_Analysis_Report.xlsx
│   └── analysis_results.json
└── package.json
```

### 📊 مؤشرات الأداء الرئيسية

| المؤشر | القيمة |
|--------|--------|
| معدل الغياب الشهري | 3.04% |
| متوسط تقييم الأداء | 3.10 / 5 |
| متوسط الرضا الوظيفي | 4.76 / 10 |
| معدل الدوران (3 سنوات) | 72% |
| متوسط الأوفرايم | 12.36 ساعة |
| دقة Logistic Regression | 66.7% |
| دقة Decision Tree | 60% |

### 🚀 التشغيل المحلي

#### المتطلبات
- Node.js 18+
- Python 3.12+
- Bun أو npm

#### تشغيل لوحة التحكم

```bash
# تثبيت التبعيات
npm install

# تشغيل خادم التطوير
npm run dev
```

ثم افتح [http://localhost:3000](http://localhost:3000)

#### تشغيل التحليل

```bash
# تثبيت تبعيات Python
pip install pandas numpy matplotlib seaborn scikit-learn openpyxl arabic-reshaper python-bidi reportlab

# تشغيل التحليل الكامل
python python-analysis/analysis.py
python python-analysis/create_excel.py
python python-analysis/generate_pdf.py
```

---

## 🇬🇧 English

### 📋 About

A comprehensive HR data analytics project covering 50 employees across 8 departments. Includes data cleaning, exploratory data analysis, KPI tracking, predictive turnover analysis using machine learning, and interactive visualizations.

### ✨ Features

- **Data Cleaning**: Format validation, missing value treatment, name standardization
- **Exploratory Data Analysis (EDA)**: Descriptive statistics, correlation matrix, distributions
- **KPI Dashboard**: Absence, performance, satisfaction, turnover, overtime metrics
- **Predictive Analysis**: Logistic Regression + Decision Tree with Feature Importance
- **Interactive Dashboard**: 4 tabs (Overview, Departments, Satisfaction vs Performance, Predictive)
- **Comprehensive PDF Report**: 9 tables and 8 charts
- **RTL Design**: Full Arabic language support

### 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Next.js 16 + TypeScript | Interactive Web UI |
| Tailwind CSS 4 + shadcn/ui | Styling & Components |
| Recharts | Interactive Charts |
| Python + Pandas | Data Analysis |
| scikit-learn | Predictive Models |
| Matplotlib + Seaborn | Data Visualization |
| ReportLab | PDF Report Generation |
| openpyxl | Excel Processing |

### 🚀 Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Open http://localhost:3000
```

### 📊 Key Findings

1. **Operations** has the highest turnover rate (1.75x in 3 years)
2. **IT** has the highest absence rate (3.50%)
3. **Marketing** leads in performance (4.67/5) and satisfaction (6.67/10)
4. **Tenure** is the strongest predictor of turnover (34.45% importance)
5. Overall turnover rate of **72%** over 3 years requires urgent attention

### 📄 License

This project is for educational and portfolio purposes.

---

<div align="center">
Made with ❤️ by <a href="https://github.com/youssefelbayomi777-cmyk">Youssef Elbayomi</a>
</div>
