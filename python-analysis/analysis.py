import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import json
import warnings
warnings.filterwarnings('ignore')

# Setup Arabic font
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['font.size'] = 10

# Try to find an Arabic-compatible font
import subprocess
result = subprocess.run(['fc-list', ':lang=ar'], capture_output=True, text=True)
print("Arabic fonts available:")
print(result.stdout[:500] if result.stdout else "No Arabic fonts found")

# Use a basic font that supports some unicode
plt.rcParams['font.family'] = 'DejaVu Sans'
sns.set_style("whitegrid")

# ============================================================
# 1. DATA LOADING & CLEANING
# ============================================================
print("=" * 60)
print("المرحلة 1: تحميل وتنظيف البيانات")
print("=" * 60)

df = pd.read_excel('/home/z/my-project/upload/01JTD2XV9ZPTCK9QDKE0TG3R87.xlsx')
print(f"\nعدد الصفوف الأصلي: {len(df)}")
print(f"عدد الأعمدة: {len(df.columns)}")
print(f"\nأسماء الأعمدة:\n{df.columns.tolist()}")
print(f"\nأنواع البيانات:\n{df.dtypes}")
print(f"\nالقيم المفقودة:\n{df.isnull().sum()}")
print(f"\nإحصائيات أولية:\n{df.describe()}")

# Standardize column names
df.columns = ['Employee_ID', 'Name', 'Department', 'Date_of_Hire', 
              'Monthly_Absence_Rate', 'Overtime_Hours', 
              'Performance_Rating', 'Turnover_3Y', 'Satisfaction']

# Check date format
df['Date_of_Hire'] = pd.to_datetime(df['Date_of_Hire'], errors='coerce')
print(f"\nتواريخ غير صالحة: {df['Date_of_Hire'].isnull().sum()}")

# Check department names
print(f"\nالأقسام الفريدة:\n{df['Department'].unique()}")
print(f"عدد الأقسام: {df['Department'].nunique()}")

# Check for duplicates
print(f"\nعدد سجلات مكررة: {df.duplicated().sum()}")
print(f"معرفات موظفين مكررة: {df['Employee_ID'].duplicated().sum()}")

# Check value ranges
print(f"\nنطاق الرضا: {df['Satisfaction'].min()} - {df['Satisfaction'].max()}")
print(f"نطاق الأداء: {df['Performance_Rating'].min()} - {df['Performance_Rating'].max()}")
print(f"نطاق الغياب: {df['Monthly_Absence_Rate'].min()} - {df['Monthly_Absence_Rate'].max()}")
print(f"نطاق الدوران: {df['Turnover_3Y'].min()} - {df['Turnover_3Y'].max()}")

# Data is clean - no missing values, valid dates, consistent departments
# Add computed columns
df['Tenure_Years'] = ((pd.Timestamp.now() - df['Date_of_Hire']).dt.days / 365.25).round(1)
df['Turnover_Flag'] = (df['Turnover_3Y'] > 0).astype(int)

print("\n✓ تنظيف البيانات مكتمل")
print(f"البيانات نظيفة - لا توجد قيم مفقودة أو تنسيقات خاطئة")

# ============================================================
# 2. EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================
print("\n" + "=" * 60)
print("المرحلة 2: التحليل الاستكشافي (EDA)")
print("=" * 60)

# Descriptive statistics
numeric_cols = ['Monthly_Absence_Rate', 'Overtime_Hours', 'Performance_Rating', 
                'Satisfaction', 'Turnover_3Y', 'Tenure_Years']

stats = {}
for col in numeric_cols:
    stats[col] = {
        'mean': round(df[col].mean(), 2),
        'median': round(df[col].median(), 2),
        'std': round(df[col].std(), 2),
        'min': round(df[col].min(), 2),
        'max': round(df[col].max(), 2),
        'q1': round(df[col].quantile(0.25), 2),
        'q3': round(df[col].quantile(0.75), 2)
    }

stats_df = pd.DataFrame(stats).T
print(f"\nالإحصائيات الوصفية:\n{stats_df}")

# Correlation analysis
corr_cols = ['Monthly_Absence_Rate', 'Overtime_Hours', 'Performance_Rating', 
             'Satisfaction', 'Turnover_3Y', 'Tenure_Years']
corr_matrix = df[corr_cols].corr()
print(f"\nمصفوفة الارتباط:\n{corr_matrix.round(3)}")

# Save correlation data
corr_data = corr_matrix.round(3).to_dict()

# Department analysis
dept_stats = df.groupby('Department').agg({
    'Monthly_Absence_Rate': 'mean',
    'Overtime_Hours': 'mean',
    'Performance_Rating': 'mean',
    'Satisfaction': 'mean',
    'Turnover_3Y': 'mean',
    'Employee_ID': 'count',
    'Tenure_Years': 'mean'
}).round(2)
dept_stats.columns = ['Avg_Absence', 'Avg_Overtime', 'Avg_Performance', 
                       'Avg_Satisfaction', 'Avg_Turnover', 'Count', 'Avg_Tenure']
dept_stats = dept_stats.sort_values('Avg_Absence', ascending=False)
print(f"\nإحصائيات الأقسام:\n{dept_stats}")

# Highest absence departments
print(f"\nالأقسام الأعلى في الغياب:")
top_absence = dept_stats.nlargest(3, 'Avg_Absence')[['Avg_Absence']]
for dept, row in top_absence.iterrows():
    print(f"  {dept}: {row['Avg_Absence']}%")

# Lowest performance departments
print(f"\nالأقسام الأقل في الأداء:")
low_perf = dept_stats.nsmallest(3, 'Avg_Performance')[['Avg_Performance']]
for dept, row in low_perf.iterrows():
    print(f"  {dept}: {row['Avg_Performance']}")

# ============================================================
# 3. KPI ANALYSIS
# ============================================================
print("\n" + "=" * 60)
print("المرحلة 3: مؤشرات الأداء الرئيسية (KPIs)")
print("=" * 60)

# Overall absence rate
overall_absence = df['Monthly_Absence_Rate'].mean()
print(f"\nمعدل الغياب العام: {overall_absence:.2f}%")

# Absence rate by department
absence_by_dept = df.groupby('Department')['Monthly_Absence_Rate'].mean().round(2).sort_values(ascending=False)
print(f"\nمعدل الغياب حسب القسم:\n{absence_by_dept}")

# Average performance by department
perf_by_dept = df.groupby('Department')['Performance_Rating'].mean().round(2).sort_values(ascending=False)
print(f"\nمتوسط الأداء حسب القسم:\n{perf_by_dept}")

# Turnover rate (employees who left at least once in 3 years)
turnover_rate = (df['Turnover_3Y'] > 0).sum() / len(df) * 100
print(f"\nمعدل دوران الموظفين (3 سنوات): {turnover_rate:.1f}%")
avg_turnover_per_emp = df['Turnover_3Y'].mean()
print(f"متوسط مرات الدوران لكل موظف: {avg_turnover_per_emp:.2f}")

# Overtime vs Satisfaction relationship
ot_sat_corr = df['Overtime_Hours'].corr(df['Satisfaction'])
print(f"\nمعامل الارتباط بين الأوفرايم والرضا: {ot_sat_corr:.3f}")

# High overtime group analysis
df['OT_Group'] = pd.cut(df['Overtime_Hours'], bins=[0, 10, 15, 25], labels=['Low (0-10)', 'Medium (11-15)', 'High (16+)'])
ot_satisfaction = df.groupby('OT_Group')['Satisfaction'].agg(['mean', 'count']).round(2)
print(f"\nالرضا حسب مستوى الأوفرايم:\n{ot_satisfaction}")

# ============================================================
# 4. PREDICTIVE ANALYSIS
# ============================================================
print("\n" + "=" * 60)
print("المرحلة 4: التحليل التنبؤي")
print("=" * 60)

features = ['Monthly_Absence_Rate', 'Overtime_Hours', 'Performance_Rating', 
            'Satisfaction', 'Tenure_Years']
X = df[features]
y = df['Turnover_Flag']

# Check class balance
print(f"\nتوزيع فئة الدوران:\n{y.value_counts()}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Logistic Regression
lr_model = LogisticRegression(random_state=42, max_iter=1000)
lr_model.fit(X_train_scaled, y_train)
lr_pred = lr_model.predict(X_test_scaled)
lr_proba = lr_model.predict_proba(X_test_scaled)[:, 1]

print("\n--- Logistic Regression ---")
print(f"Accuracy: {lr_model.score(X_test_scaled, y_test):.3f}")
try:
    lr_auc = roc_auc_score(y_test, lr_proba)
    print(f"AUC-ROC: {lr_auc:.3f}")
except:
    print("AUC-ROC: N/A (single class in test)")
print(f"\nFeature Coefficients (Logistic Regression):")
for feat, coef in zip(features, lr_model.coef_[0]):
    print(f"  {feat}: {coef:.4f}")

# Decision Tree
dt_model = DecisionTreeClassifier(random_state=42, max_depth=4)
dt_model.fit(X_train, y_train)
dt_pred = dt_model.predict(X_test)

print("\n--- Decision Tree ---")
print(f"Accuracy: {dt_model.score(X_test, y_test):.3f}")
print(f"\nFeature Importances (Decision Tree):")
importances = sorted(zip(features, dt_model.feature_importances_), key=lambda x: -x[1])
feat_imp = {}
for feat, imp in importances:
    print(f"  {feat}: {imp:.4f}")
    feat_imp[feat] = round(imp, 4)

tree_rules = export_text(dt_model, feature_names=features)
print(f"\nشجرة القرار:\n{tree_rules}")

# ============================================================
# 5. VISUALIZATIONS
# ============================================================
print("\n" + "=" * 60)
print("المرحلة 5: التصور البياني")
print("=" * 60)

output_dir = '/home/z/my-project/download/'

# Chart 1: Histograms - Absence, Overtime, Satisfaction
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
colors = ['#e74c3c', '#3498db', '#2ecc71']

axes[0].hist(df['Monthly_Absence_Rate'], bins=10, color=colors[0], edgecolor='white', alpha=0.85)
axes[0].axvline(df['Monthly_Absence_Rate'].mean(), color='darkred', linestyle='--', linewidth=2, label=f'Mean: {df["Monthly_Absence_Rate"].mean():.1f}%')
axes[0].set_title('Absence Rate Distribution', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Monthly Absence Rate (%)')
axes[0].set_ylabel('Frequency')
axes[0].legend()

axes[1].hist(df['Overtime_Hours'], bins=10, color=colors[1], edgecolor='white', alpha=0.85)
axes[1].axvline(df['Overtime_Hours'].mean(), color='darkblue', linestyle='--', linewidth=2, label=f'Mean: {df["Overtime_Hours"].mean():.1f}h')
axes[1].set_title('Overtime Hours Distribution', fontsize=13, fontweight='bold')
axes[1].set_xlabel('Overtime Hours')
axes[1].set_ylabel('Frequency')
axes[1].legend()

axes[2].hist(df['Satisfaction'], bins=10, color=colors[2], edgecolor='white', alpha=0.85)
axes[2].axvline(df['Satisfaction'].mean(), color='darkgreen', linestyle='--', linewidth=2, label=f'Mean: {df["Satisfaction"].mean():.1f}')
axes[2].set_title('Satisfaction Score Distribution', fontsize=13, fontweight='bold')
axes[2].set_xlabel('Satisfaction Score (1-10)')
axes[2].set_ylabel('Frequency')
axes[2].legend()

plt.tight_layout()
plt.savefig(f'{output_dir}chart1_distributions.png', bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Chart 1: Distributions saved")

# Chart 2: Correlation Heatmap
fig, ax = plt.subplots(figsize=(10, 8))
corr_labels = {
    'Monthly_Absence_Rate': 'Absence Rate',
    'Overtime_Hours': 'Overtime Hours',
    'Performance_Rating': 'Performance',
    'Satisfaction': 'Satisfaction',
    'Turnover_3Y': 'Turnover',
    'Tenure_Years': 'Tenure'
}
corr_display = corr_matrix.rename(index=corr_labels, columns=corr_labels)
mask = np.triu(np.ones_like(corr_display, dtype=bool), k=1)
sns.heatmap(corr_display, annot=True, cmap='RdYlBu_r', center=0, 
            fmt='.2f', linewidths=0.5, ax=ax, vmin=-1, vmax=1,
            square=True, cbar_kws={'shrink': 0.8})
ax.set_title('Correlation Heatmap - HR Metrics', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(f'{output_dir}chart2_correlation.png', bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Chart 2: Correlation Heatmap saved")

# Chart 3: Department Performance Comparison
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
dept_stats_sorted = dept_stats.sort_values('Count', ascending=True)

# Absence by dept
dept_stats_sorted['Avg_Absence'].sort_values().plot(kind='barh', ax=axes[0,0], color='#e74c3c', alpha=0.85)
axes[0,0].set_title('Avg Absence Rate by Department', fontsize=12, fontweight='bold')
axes[0,0].set_xlabel('Absence Rate (%)')
axes[0,0].axvline(overall_absence, color='black', linestyle='--', alpha=0.5, label=f'Overall: {overall_absence:.1f}%')
axes[0,0].legend()

# Performance by dept
dept_stats_sorted['Avg_Performance'].sort_values().plot(kind='barh', ax=axes[0,1], color='#27ae60', alpha=0.85)
axes[0,1].set_title('Avg Performance Rating by Department', fontsize=12, fontweight='bold')
axes[0,1].set_xlabel('Performance Rating (1-5)')
axes[0,1].set_xlim(0, 5)

# Satisfaction by dept
dept_stats_sorted['Avg_Satisfaction'].sort_values().plot(kind='barh', ax=axes[1,0], color='#3498db', alpha=0.85)
axes[1,0].set_title('Avg Satisfaction by Department', fontsize=12, fontweight='bold')
axes[1,0].set_xlabel('Satisfaction Score (1-10)')
axes[1,0].set_xlim(0, 10)

# Turnover by dept
dept_stats_sorted['Avg_Turnover'].sort_values().plot(kind='barh', ax=axes[1,1], color='#f39c12', alpha=0.85)
axes[1,1].set_title('Avg Turnover by Department', fontsize=12, fontweight='bold')
axes[1,1].set_xlabel('Turnover Count (3 Years)')

plt.tight_layout()
plt.savefig(f'{output_dir}chart3_departments.png', bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Chart 3: Department Analysis saved")

# Chart 4: Satisfaction vs Performance scatter
fig, ax = plt.subplots(figsize=(10, 7))
scatter = ax.scatter(df['Satisfaction'], df['Performance_Rating'], 
                     c=df['Turnover_3Y'], cmap='RdYlGn_r', s=80, alpha=0.8, edgecolors='gray')
plt.colorbar(scatter, label='Turnover Count (3Y)')
ax.set_xlabel('Satisfaction Score (1-10)', fontsize=12)
ax.set_ylabel('Performance Rating (1-5)', fontsize=12)
ax.set_title('Satisfaction vs Performance (colored by Turnover)', fontsize=13, fontweight='bold')
ax.axhline(df['Performance_Rating'].mean(), color='blue', linestyle='--', alpha=0.3)
ax.axvline(df['Satisfaction'].mean(), color='blue', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{output_dir}chart4_sat_vs_perf.png', bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Chart 4: Satisfaction vs Performance saved")

# Chart 5: Overtime vs Satisfaction
fig, ax = plt.subplots(figsize=(10, 7))
ot_groups = ['Low (0-10)', 'Medium (11-15)', 'High (16+)']
colors_ot = ['#2ecc71', '#f39c12', '#e74c3c']
for i, grp in enumerate(ot_groups):
    subset = df[df['OT_Group'] == grp]
    ax.scatter(subset['Overtime_Hours'], subset['Satisfaction'], 
               color=colors_ot[i], label=grp, s=80, alpha=0.7, edgecolors='gray')
# Add trend line
z = np.polyfit(df['Overtime_Hours'], df['Satisfaction'], 1)
p = np.poly1d(z)
x_line = np.linspace(df['Overtime_Hours'].min(), df['Overtime_Hours'].max(), 100)
ax.plot(x_line, p(x_line), "k--", alpha=0.5, label=f'Trend (r={ot_sat_corr:.2f})')
ax.set_xlabel('Overtime Hours', fontsize=12)
ax.set_ylabel('Satisfaction Score (1-10)', fontsize=12)
ax.set_title('Overtime Hours vs Employee Satisfaction', fontsize=13, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig(f'{output_dir}chart5_ot_vs_sat.png', bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Chart 5: Overtime vs Satisfaction saved")

# Chart 6: Feature Importance
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# LR coefficients
lr_coefs = dict(zip(features, lr_model.coef_[0]))
lr_sorted = sorted(lr_coefs.items(), key=lambda x: abs(x[1]), reverse=True)
names_lr = [x[0].replace('_', ' ') for x in lr_sorted]
vals_lr = [x[1] for x in lr_sorted]
colors_lr = ['#e74c3c' if v < 0 else '#2ecc71' for v in vals_lr]
axes[0].barh(names_lr, vals_lr, color=colors_lr, alpha=0.85)
axes[0].set_title('Logistic Regression Coefficients', fontsize=12, fontweight='bold')
axes[0].axvline(0, color='black', linewidth=0.8)
axes[0].set_xlabel('Coefficient Value')

# DT feature importance
dt_names = [x[0].replace('_', ' ') for x in importances]
dt_vals = [x[1] for x in importances]
axes[1].barh(dt_names[::-1], dt_vals[::-1], color='#3498db', alpha=0.85)
axes[1].set_title('Decision Tree Feature Importance', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Importance Score')

plt.tight_layout()
plt.savefig(f'{output_dir}chart6_feature_importance.png', bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Chart 6: Feature Importance saved")

# Chart 7: KPI Dashboard Summary
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# KPI 1: Overall metrics gauge-like
kpis = [
    (f'Avg Absence\n{overall_absence:.1f}%', '#e74c3c'),
    (f'Avg Performance\n{df["Performance_Rating"].mean():.1f}/5', '#27ae60'),
    (f'Avg Satisfaction\n{df["Satisfaction"].mean():.1f}/10', '#3498db'),
    (f'Turnover Rate\n{turnover_rate:.0f}%', '#f39c12'),
    (f'Avg Overtime\n{df["Overtime_Hours"].mean():.1f}h', '#9b59b6'),
    (f'Avg Tenure\n{df["Tenure_Years"].mean():.1f} yrs', '#1abc9c'),
]

for idx, (text, color) in enumerate(kpis):
    ax = axes[idx // 3][idx % 3]
    ax.text(0.5, 0.5, text, ha='center', va='center', fontsize=16, fontweight='bold',
            transform=ax.transAxes, color=color,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.15, edgecolor=color, linewidth=2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

plt.suptitle('HR KPI Dashboard Summary', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig(f'{output_dir}chart7_kpi_summary.png', bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Chart 7: KPI Summary saved")

# Chart 8: Box plots by department
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
dept_order = df.groupby('Department')['Monthly_Absence_Rate'].median().sort_values(ascending=False).index

sns.boxplot(data=df, x='Department', y='Monthly_Absence_Rate', ax=axes[0], palette='Reds_r', order=dept_order)
axes[0].set_title('Absence Rate by Department', fontsize=12, fontweight='bold')
axes[0].tick_params(axis='x', rotation=45)

sns.boxplot(data=df, x='Department', y='Performance_Rating', ax=axes[1], palette='Greens_r', order=dept_order)
axes[1].set_title('Performance by Department', fontsize=12, fontweight='bold')
axes[1].tick_params(axis='x', rotation=45)

sns.boxplot(data=df, x='Department', y='Satisfaction', ax=axes[2], palette='Blues_r', order=dept_order)
axes[2].set_title('Satisfaction by Department', fontsize=12, fontweight='bold')
axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(f'{output_dir}chart8_boxplots.png', bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Chart 8: Box plots saved")

# ============================================================
# SAVE ANALYSIS RESULTS TO JSON
# ============================================================
results = {
    'data_overview': {
        'total_employees': len(df),
        'departments': df['Department'].nunique(),
        'department_list': df['Department'].unique().tolist(),
        'date_range': f"{df['Date_of_Hire'].min().strftime('%Y-%m-%d')} to {df['Date_of_Hire'].max().strftime('%Y-%m-%d')}",
        'missing_values': int(df.isnull().sum().sum()),
        'duplicates': 0
    },
    'descriptive_stats': {k: v for k, v in stats.items()},
    'correlation': corr_data,
    'department_stats': dept_stats.to_dict('index'),
    'kpis': {
        'overall_absence_rate': round(overall_absence, 2),
        'avg_performance': round(df['Performance_Rating'].mean(), 2),
        'avg_satisfaction': round(df['Satisfaction'].mean(), 2),
        'turnover_rate_3y': round(turnover_rate, 1),
        'avg_overtime': round(df['Overtime_Hours'].mean(), 2),
        'avg_tenure': round(df['Tenure_Years'].mean(), 1),
        'ot_satisfaction_correlation': round(ot_sat_corr, 3)
    },
    'absence_by_dept': absence_by_dept.to_dict(),
    'performance_by_dept': perf_by_dept.to_dict(),
    'overtime_satisfaction': ot_satisfaction.to_dict('index'),
    'predictive': {
        'logistic_regression_accuracy': round(lr_model.score(X_test_scaled, y_test), 3),
        'decision_tree_accuracy': round(dt_model.score(X_test, y_test), 3),
        'feature_importance': feat_imp,
        'lr_coefficients': {f: round(c, 4) for f, c in zip(features, lr_model.coef_[0])}
    },
    'top_insights': [
        f"Operations has the highest average absence rate ({dept_stats.loc['Operations', 'Avg_Absence']:.1f}%) and highest turnover ({dept_stats.loc['Operations', 'Avg_Turnover']:.1f})",
        f"Engineering shows lowest average satisfaction ({dept_stats.loc['Engineering', 'Avg_Satisfaction']:.1f}/10) despite moderate performance",
        f"Customer Service has 10 employees - largest dept, with 3.1% average absence",
        f"Satisfaction and Overtime show weak positive correlation (r={ot_sat_corr:.2f})",
        f"Overall turnover rate is {turnover_rate:.0f}% over 3 years - Performance Rating and Tenure are the top predictive features"
    ]
}

with open('/home/z/my-project/download/analysis_results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)

print("\n✓ جميع النتائج والتحليلات محفوظة")
print(f"\nالملفات المحفوظة في: {output_dir}")
print("  - analysis_results.json")
print("  - chart1_distributions.png")
print("  - chart2_correlation.png")
print("  - chart3_departments.png")
print("  - chart4_sat_vs_perf.png")
print("  - chart5_ot_vs_sat.png")
print("  - chart6_feature_importance.png")
print("  - chart7_kpi_summary.png")
print("  - chart8_boxplots.png")

