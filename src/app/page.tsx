'use client';

import React from 'react';
import Image from 'next/image';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import {
  TrendingDown,
  Star,
  Smile,
  UserX,
  Clock,
  CalendarClock,
  BarChart3,
  Building2,
  ScatterChart as ScatterIcon,
  Brain,
  ArrowUpRight,
  ArrowDownRight,
  Minus,
  AlertTriangle,
  CheckCircle2,
} from 'lucide-react';

// ─── Data ───────────────────────────────────────────────────────────────────

const kpis = {
  overall_absence_rate: 3.04,
  avg_performance: 3.1,
  avg_satisfaction: 4.76,
  turnover_rate_3y: 72.0,
  avg_overtime: 12.36,
  avg_tenure: 6.33,
  ot_satisfaction_correlation: 0.052,
};

const departmentStats: Record<string, {
  Avg_Absence: number;
  Avg_Overtime: number;
  Avg_Performance: number;
  Avg_Satisfaction: number;
  Avg_Turnover: number;
  Count: number;
  Avg_Tenure: number;
}> = {
  IT: { Avg_Absence: 3.5, Avg_Overtime: 12.12, Avg_Performance: 3.12, Avg_Satisfaction: 3.38, Avg_Turnover: 0.62, Count: 8, Avg_Tenure: 5.65 },
  Sales: { Avg_Absence: 3.36, Avg_Overtime: 11.2, Avg_Performance: 3.8, Avg_Satisfaction: 6.6, Avg_Turnover: 2.0, Count: 5, Avg_Tenure: 5.64 },
  Operations: { Avg_Absence: 3.15, Avg_Overtime: 13.62, Avg_Performance: 2.75, Avg_Satisfaction: 3.88, Avg_Turnover: 1.88, Count: 8, Avg_Tenure: 8.01 },
  'Customer Service': { Avg_Absence: 3.08, Avg_Overtime: 13.38, Avg_Performance: 2.88, Avg_Satisfaction: 5.25, Avg_Turnover: 1.38, Count: 8, Avg_Tenure: 6.52 },
  HR: { Avg_Absence: 3.01, Avg_Overtime: 12.0, Avg_Performance: 3.38, Avg_Satisfaction: 3.75, Avg_Turnover: 1.0, Count: 8, Avg_Tenure: 5.84 },
  Engineering: { Avg_Absence: 2.63, Avg_Overtime: 13.67, Avg_Performance: 2.5, Avg_Satisfaction: 6.17, Avg_Turnover: 2.5, Count: 6, Avg_Tenure: 6.38 },
  Finance: { Avg_Absence: 2.52, Avg_Overtime: 11.75, Avg_Performance: 2.5, Avg_Satisfaction: 5.5, Avg_Turnover: 1.25, Count: 4, Avg_Tenure: 4.03 },
  Marketing: { Avg_Absence: 2.4, Avg_Overtime: 8.0, Avg_Performance: 4.67, Avg_Satisfaction: 5.33, Avg_Turnover: 1.0, Count: 3, Avg_Tenure: 8.5 },
};

const deptNameMap: Record<string, string> = {
  'Customer Service': 'خدمة العملاء',
  Engineering: 'الهندسة',
  Finance: 'المالية',
  HR: 'الموارد البشرية',
  IT: 'تقنية المعلومات',
  Marketing: 'التسويق',
  Operations: 'العمليات',
  Sales: 'المبيعات',
};

const predictive = {
  logistic_regression_accuracy: 0.667,
  decision_tree_accuracy: 0.6,
  feature_importance: {
    Tenure_Years: 0.3445,
    Monthly_Absence_Rate: 0.2848,
    Performance_Rating: 0.1402,
    Overtime_Hours: 0.1183,
    Satisfaction: 0.1122,
  },
  lr_coefficients: {
    Monthly_Absence_Rate: -0.555,
    Overtime_Hours: 0.3282,
    Performance_Rating: 0.4585,
    Satisfaction: -0.2647,
    Tenure_Years: 0.5117,
  },
};

const overtimeSatisfaction = [
  { name: 'منخفض (0-10 ساعة)', value: 4.7, count: 20 },
  { name: 'متوسط (11-15 ساعة)', value: 4.25, count: 16 },
  { name: 'مرتفع (16+ ساعة)', value: 5.43, count: 14 },
];

const absenceBarData = Object.entries(departmentStats).map(([dept, stats]) => ({
  name: deptNameMap[dept] || dept,
  value: stats.Avg_Absence,
  fullName: dept,
}));

const performanceBarData = Object.entries(departmentStats).map(([dept, stats]) => ({
  name: deptNameMap[dept] || dept,
  value: stats.Avg_Performance,
  fullName: dept,
}));

const featureImportanceData = Object.entries(predictive.feature_importance).map(([feature, importance]) => ({
  name: feature,
  importance: parseFloat((importance * 100).toFixed(1)),
}));

const featureNameMap: Record<string, string> = {
  Tenure_Years: 'سنوات الخدمة',
  Monthly_Absence_Rate: 'معدل الغياب الشهري',
  Performance_Rating: 'تقييم الأداء',
  Overtime_Hours: 'ساعات العمل الإضافي',
  Satisfaction: 'الرضا الوظيفي',
};

// ─── Color helpers ──────────────────────────────────────────────────────────

function getPerformanceColor(val: number): string {
  if (val >= 4) return 'bg-emerald-500';
  if (val >= 3) return 'bg-amber-500';
  return 'bg-red-500';
}

function getAbsenceColor(val: number): string {
  if (val <= 2.6) return 'bg-emerald-500';
  if (val <= 3.1) return 'bg-amber-500';
  return 'bg-red-500';
}

function getTurnoverBadgeVariant(val: number): 'default' | 'secondary' | 'destructive' | 'outline' {
  if (val <= 1.0) return 'default';
  if (val <= 1.5) return 'secondary';
  return 'destructive';
}

const barColors = ['#059669', '#0d9488', '#0891b2', '#2563eb', '#7c3aed', '#c026d3', '#e11d48', '#ea580c'];

// ─── KPI Cards ──────────────────────────────────────────────────────────────

function KPICards() {
  const cards = [
    {
      title: 'معدل الغياب العام',
      value: `${kpis.overall_absence_rate}%`,
      description: 'نسبة الغياب الشهرية',
      icon: TrendingDown,
      gradient: 'from-emerald-500 to-teal-600',
      trend: 'low' as const,
    },
    {
      title: 'متوسط الأداء',
      value: `${kpis.avg_performance}/5`,
      description: 'تقييم الأداء العام',
      icon: Star,
      gradient: 'from-amber-500 to-orange-600',
      trend: 'mid' as const,
    },
    {
      title: 'متوسط الرضا',
      value: `${kpis.avg_satisfaction}/10`,
      description: 'مستوى الرضا الوظيفي',
      icon: Smile,
      gradient: 'from-cyan-500 to-blue-600',
      trend: 'low' as const,
    },
    {
      title: 'معدل دوران العمالة',
      value: `${kpis.turnover_rate_3y}%`,
      description: 'خلال 3 سنوات',
      icon: UserX,
      gradient: 'from-rose-500 to-red-600',
      trend: 'high' as const,
    },
    {
      title: 'متوسط العمل الإضافي',
      value: `${kpis.avg_overtime} ساعة`,
      description: 'شهرياً',
      icon: Clock,
      gradient: 'from-violet-500 to-purple-600',
      trend: 'mid' as const,
    },
    {
      title: 'متوسط سنوات الخدمة',
      value: `${kpis.avg_tenure} سنة`,
      description: 'متوسط مدة البقاء',
      icon: CalendarClock,
      gradient: 'from-teal-500 to-emerald-600',
      trend: 'low' as const,
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {cards.map((card) => {
        const IconComp = card.icon;
        return (
          <Card key={card.title} className="overflow-hidden border-0 shadow-lg">
            <CardContent className="p-0">
              <div className={`bg-gradient-to-br ${card.gradient} p-5 text-white`}>
                <div className="flex items-start justify-between">
                  <div className="space-y-2">
                    <p className="text-white/80 text-sm font-medium">{card.title}</p>
                    <p className="text-3xl font-bold tracking-tight">{card.value}</p>
                    <p className="text-white/70 text-xs">{card.description}</p>
                  </div>
                  <div className="rounded-xl bg-white/20 p-3 backdrop-blur-sm">
                    <IconComp className="h-6 w-6 text-white" />
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}

// ─── Tab 1: Overall Metrics ────────────────────────────────────────────────

function OverallMetricsTab() {
  return (
    <div className="space-y-6">
      <KPICards />

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <BarChart3 className="h-5 w-5 text-emerald-600" />
            ملخص المؤشرات الرئيسية
          </CardTitle>
          <CardDescription>نظرة شاملة على جميع مؤشرات الأداء الرئيسية للموارد البشرية</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="relative w-full rounded-lg overflow-hidden bg-muted/30 p-4">
            <Image
              src="/charts/chart7_kpi_summary.png"
              alt="ملخص المؤشرات الرئيسية"
              width={1200}
              height={600}
              className="w-full h-auto"
            />
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <AlertTriangle className="h-5 w-5 text-amber-500" />
            أبرز النتائج والتحليلات
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {[
              'قسم العمليات يُسجّل أعلى معدل غياب (3.15%) وأعلى دوران وظيفي (1.88)',
              'قسم الهندسة يُظهر أقل رضا وظيفي (6.17/10) رغم الأداء المعتدل',
              'خدمة العملاء أكبر قسم بـ 8 موظفين ومعدل غياب 3.08%',
              'الارتباط بين الرضا وساعات العمل الإضافي ضعيف (r=0.05)',
              'معدل الدوران الوظيفي العام 72% خلال 3 سنوات - تقييم الأداء وسنوات الخدمة أهم عوامل التنبؤ',
            ].map((insight, i) => (
              <div key={i} className="flex items-start gap-3 p-3 rounded-lg bg-muted/50">
                <div className="mt-1 rounded-full bg-emerald-100 p-1">
                  <CheckCircle2 className="h-4 w-4 text-emerald-600" />
                </div>
                <p className="text-sm leading-relaxed text-muted-foreground">{insight}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

// ─── Tab 2: Department Analysis ────────────────────────────────────────────

function DepartmentAnalysisTab() {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Building2 className="h-5 w-5 text-teal-600" />
            جدول إحصائيات الأقسام
          </CardTitle>
          <CardDescription>مقارنة تفصيلية بين أداء ومؤشرات كل قسم</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto rounded-lg border">
            <Table>
              <TableHeader>
                <TableRow className="bg-muted/50">
                  <TableHead className="text-right font-bold">القسم</TableHead>
                  <TableHead className="text-center font-bold">العدد</TableHead>
                  <TableHead className="text-center font-bold">الغياب %</TableHead>
                  <TableHead className="text-center font-bold">الأداء</TableHead>
                  <TableHead className="text-center font-bold">الرضا</TableHead>
                  <TableHead className="text-center font-bold">العمل الإضافي</TableHead>
                  <TableHead className="text-center font-bold">الدوران</TableHead>
                  <TableHead className="text-center font-bold">سنوات الخدمة</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {Object.entries(departmentStats)
                  .sort((a, b) => b[1].Avg_Performance - a[1].Avg_Performance)
                  .map(([dept, stats]) => (
                    <TableRow key={dept} className="hover:bg-emerald-50/50 transition-colors">
                      <TableCell className="font-semibold text-right">
                        <div className="flex items-center gap-2">
                          <div className={`h-2.5 w-2.5 rounded-full ${getPerformanceColor(stats.Avg_Performance)}`} />
                          {deptNameMap[dept] || dept}
                        </div>
                      </TableCell>
                      <TableCell className="text-center">{stats.Count}</TableCell>
                      <TableCell className="text-center">
                        <Badge variant="outline" className="font-mono">
                          {stats.Avg_Absence.toFixed(2)}%
                        </Badge>
                      </TableCell>
                      <TableCell className="text-center">
                        <Badge variant={stats.Avg_Performance >= 3.5 ? 'default' : stats.Avg_Performance >= 3 ? 'secondary' : 'destructive'} className="font-mono">
                          {stats.Avg_Performance.toFixed(2)}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-center">
                        <span className="font-mono text-sm">{stats.Avg_Satisfaction.toFixed(2)}</span>
                      </TableCell>
                      <TableCell className="text-center">
                        <span className="font-mono text-sm">{stats.Avg_Overtime.toFixed(1)}h</span>
                      </TableCell>
                      <TableCell className="text-center">
                        <Badge variant={getTurnoverBadgeVariant(stats.Avg_Turnover)} className="font-mono">
                          {stats.Avg_Turnover.toFixed(2)}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-center">
                        <span className="font-mono text-sm">{stats.Avg_Tenure.toFixed(1)}</span>
                      </TableCell>
                    </TableRow>
                  ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">معدل الغياب حسب القسم</CardTitle>
            <CardDescription>مقارنة معدلات الغياب الشهرية بين الأقسام</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={absenceBarData} layout="vertical" margin={{ top: 5, right: 30, left: 80, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
                  <XAxis type="number" domain={[0, 4]} tick={{ fontSize: 12 }} />
                  <YAxis type="category" dataKey="name" width={80} tick={{ fontSize: 11 }} />
                  <Tooltip
                    contentStyle={{
                      borderRadius: '8px',
                      border: '1px solid #e5e7eb',
                      boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)',
                      textAlign: 'right',
                      direction: 'rtl',
                    }}
                    formatter={(value: number) => [`${value.toFixed(2)}%`, 'معدل الغياب']}
                  />
                  <Bar dataKey="value" radius={[0, 4, 4, 0]} maxBarSize={30}>
                    {absenceBarData.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={entry.value <= 2.6 ? '#059669' : entry.value <= 3.1 ? '#d97706' : '#dc2626'}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">تقييم الأداء حسب القسم</CardTitle>
            <CardDescription>متوسط تقييم الأداء لكل قسم (من 5)</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={performanceBarData} layout="vertical" margin={{ top: 5, right: 30, left: 80, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
                  <XAxis type="number" domain={[0, 5]} tick={{ fontSize: 12 }} />
                  <YAxis type="category" dataKey="name" width={80} tick={{ fontSize: 11 }} />
                  <Tooltip
                    contentStyle={{
                      borderRadius: '8px',
                      border: '1px solid #e5e7eb',
                      boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)',
                      textAlign: 'right',
                      direction: 'rtl',
                    }}
                    formatter={(value: number) => [`${value.toFixed(2)}/5`, 'الأداء']}
                  />
                  <Bar dataKey="value" radius={[0, 4, 4, 0]} maxBarSize={30}>
                    {performanceBarData.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={entry.value >= 4 ? '#059669' : entry.value >= 3 ? '#d97706' : '#dc2626'}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">تحليل الغياب حسب القسم</CardTitle>
            <CardDescription>توزيع معدلات الغياب وأثرها</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="relative w-full rounded-lg overflow-hidden bg-muted/30 p-3">
              <Image
                src="/charts/chart3_departments.png"
                alt="تحليل الغياب حسب القسم"
                width={800}
                height={500}
                className="w-full h-auto"
              />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">توزيع الأداء حسب القسم</CardTitle>
            <CardDescription>مخططات الصندوق لتقييمات الأداء</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="relative w-full rounded-lg overflow-hidden bg-muted/30 p-3">
              <Image
                src="/charts/chart8_boxplots.png"
                alt="مخططات الصندوق للأداء"
                width={800}
                height={500}
                className="w-full h-auto"
              />
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

// ─── Tab 3: Satisfaction vs Performance ─────────────────────────────────────

function SatisfactionVsPerformanceTab() {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <ScatterIcon className="h-5 w-5 text-cyan-600" />
            العلاقة بين الرضا والأداء
          </CardTitle>
          <CardDescription>تحليل الارتباط بين مستوى الرضا الوظيفي وتقييم الأداء</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="relative w-full rounded-lg overflow-hidden bg-muted/30 p-4">
            <Image
              src="/charts/chart4_sat_vs_perf.png"
              alt="الرضا مقابل الأداء"
              width={1200}
              height={700}
              className="w-full h-auto"
            />
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Clock className="h-5 w-5 text-violet-600" />
            العلاقة بين العمل الإضافي والرضا
          </CardTitle>
          <CardDescription>
            ارتباط ضعيف (r = {kpis.ot_satisfaction_correlation}) بين ساعات العمل الإضافي ومستوى الرضا
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="relative w-full rounded-lg overflow-hidden bg-muted/30 p-4">
            <Image
              src="/charts/chart5_ot_vs_sat.png"
              alt="العمل الإضافي مقابل الرضا"
              width={1200}
              height={700}
              className="w-full h-auto"
            />
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">متوسط الرضا حسب مستوى العمل الإضافي</CardTitle>
          <CardDescription>تأثير ساعات العمل الإضافي على مستوى الرضا الوظيفي</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-[280px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={overtimeSatisfaction} margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                <YAxis domain={[0, 10]} tick={{ fontSize: 12 }} />
                <Tooltip
                  contentStyle={{
                    borderRadius: '8px',
                    border: '1px solid #e5e7eb',
                    boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)',
                    textAlign: 'right',
                    direction: 'rtl',
                  }}
                  formatter={(value: number, _name: string, props: { payload: { count: number } }) => [
                    `${value.toFixed(2)}/10 (${props.payload.count} موظف)`,
                    'متوسط الرضا',
                  ]}
                />
                <Bar dataKey="value" fill="#0891b2" radius={[6, 6, 0, 0]} maxBarSize={80} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="border-emerald-200 bg-emerald-50/50">
          <CardContent className="pt-6">
            <div className="text-center space-y-2">
              <div className="mx-auto rounded-full bg-emerald-100 p-3 w-fit">
                <ArrowUpRight className="h-6 w-6 text-emerald-600" />
              </div>
              <p className="font-semibold text-emerald-800">عمل إضافي مرتفع</p>
              <p className="text-2xl font-bold text-emerald-600">5.43/10</p>
              <p className="text-xs text-emerald-600/70">أعلى رضا على الرغم من كثرة الساعات</p>
            </div>
          </CardContent>
        </Card>
        <Card className="border-amber-200 bg-amber-50/50">
          <CardContent className="pt-6">
            <div className="text-center space-y-2">
              <div className="mx-auto rounded-full bg-amber-100 p-3 w-fit">
                <Minus className="h-6 w-6 text-amber-600" />
              </div>
              <p className="font-semibold text-amber-800">عمل إضافي منخفض</p>
              <p className="text-2xl font-bold text-amber-600">4.70/10</p>
              <p className="text-xs text-amber-600/70">رضا متوسط رغم قلة الساعات</p>
            </div>
          </CardContent>
        </Card>
        <Card className="border-rose-200 bg-rose-50/50">
          <CardContent className="pt-6">
            <div className="text-center space-y-2">
              <div className="mx-auto rounded-full bg-rose-100 p-3 w-fit">
                <ArrowDownRight className="h-6 w-6 text-rose-600" />
              </div>
              <p className="font-semibold text-rose-800">عمل إضافي متوسط</p>
              <p className="text-2xl font-bold text-rose-600">4.25/10</p>
              <p className="text-xs text-rose-600/70">أقل رضا في الفئة المتوسطة</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

// ─── Tab 4: Predictive Analysis ────────────────────────────────────────────

function PredictiveAnalysisTab() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card className="border-emerald-200">
          <CardContent className="pt-6">
            <div className="text-center space-y-3">
              <div className="mx-auto rounded-full bg-emerald-100 p-3 w-fit">
                <Brain className="h-6 w-6 text-emerald-600" />
              </div>
              <p className="font-semibold">الانحدار اللوجستي</p>
              <p className="text-4xl font-bold text-emerald-600">{(predictive.logistic_regression_accuracy * 100).toFixed(1)}%</p>
              <p className="text-sm text-muted-foreground">دقة النموذج</p>
              <Progress value={predictive.logistic_regression_accuracy * 100} className="h-2" />
            </div>
          </CardContent>
        </Card>
        <Card className="border-amber-200">
          <CardContent className="pt-6">
            <div className="text-center space-y-3">
              <div className="mx-auto rounded-full bg-amber-100 p-3 w-fit">
                <BarChart3 className="h-6 w-6 text-amber-600" />
              </div>
              <p className="font-semibold">شجرة القرار</p>
              <p className="text-4xl font-bold text-amber-600">{(predictive.decision_tree_accuracy * 100).toFixed(1)}%</p>
              <p className="text-sm text-muted-foreground">دقة النموذج</p>
              <Progress value={predictive.decision_tree_accuracy * 100} className="h-2" />
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <BarChart3 className="h-5 w-5 text-emerald-600" />
            أهمية الميزات - نموذج شجرة القرار
          </CardTitle>
          <CardDescription>ترتيب العوامل المؤثرة في التنبؤ بدوران العمالة</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="relative w-full rounded-lg overflow-hidden bg-muted/30 p-4">
            <Image
              src="/charts/chart6_feature_importance.png"
              alt="أهمية الميزات"
              width={1200}
              height={600}
              className="w-full h-auto"
            />
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">أهمية الميزات</CardTitle>
            <CardDescription>شجرة القرار - نسبة الأهمية لكل عامل</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {Object.entries(predictive.feature_importance)
                .sort((a, b) => b[1] - a[1])
                .map(([feature, importance]) => (
                  <div key={feature} className="space-y-1.5">
                    <div className="flex items-center justify-between text-sm">
                      <span className="font-medium">{featureNameMap[feature] || feature}</span>
                      <span className="font-mono text-muted-foreground">{(importance * 100).toFixed(1)}%</span>
                    </div>
                    <Progress value={importance * 100} className="h-2.5" />
                  </div>
                ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">معاملات الانحدار اللوجستي</CardTitle>
            <CardDescription>تأثير كل متغير على احتمالية دوران العمالة</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {Object.entries(predictive.lr_coefficients)
                .sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))
                .map(([feature, coefficient]) => {
                  const isPositive = coefficient > 0;
                  return (
                    <div key={feature} className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                      <div className="flex items-center gap-2">
                        {isPositive ? (
                          <ArrowUpRight className="h-4 w-4 text-rose-500" />
                        ) : (
                          <ArrowDownRight className="h-4 w-4 text-emerald-500" />
                        )}
                        <span className="text-sm font-medium">{featureNameMap[feature] || feature}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge variant={isPositive ? 'destructive' : 'default'} className="font-mono">
                          {coefficient > 0 ? '+' : ''}{coefficient.toFixed(4)}
                        </Badge>
                        <span className="text-xs text-muted-foreground">
                          {isPositive ? 'يزيد الدوران' : 'يقلل الدوران'}
                        </span>
                      </div>
                    </div>
                  );
                })}
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">تفسير النتائج التنبؤية</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="p-4 rounded-lg bg-emerald-50 border border-emerald-200">
              <h4 className="font-semibold text-emerald-800 mb-2 flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4" />
                أقوى عوامل التنبؤ
              </h4>
              <p className="text-sm text-emerald-700 leading-relaxed">
                <strong>سنوات الخدمة</strong> هي أهم عامل تنبؤي بدوران العمالة (34.5%)، يليها <strong>معدل الغياب الشهري</strong> (28.5%).
                هذا يشير إلى أن الموظفين الأقدم عرضة أكثر لمغادرة المنظمة، وكذلك الموظفون ذوو معدلات الغياب المرتفعة.
              </p>
            </div>
            <div className="p-4 rounded-lg bg-amber-50 border border-amber-200">
              <h4 className="font-semibold text-amber-800 mb-2 flex items-center gap-2">
                <AlertTriangle className="h-4 w-4" />
                تأثير الأداء والرضا
              </h4>
              <p className="text-sm text-amber-700 leading-relaxed">
                <strong>تقييم الأداء</strong> له معامل إيجابي (+0.4585) مما يعني أن الأداء الأعلى يرتبط بارتفاع احتمالية المغادرة (قد يشير إلى أن الموظفين المتميزين يجدون فرصاً أفضل).
                بينما <strong>الرضا الوظيفي</strong> له معامل سلبي (-0.2647) مما يشير إلى أن زيادة الرضا تقلل من احتمالية الدوران.
              </p>
            </div>
            <div className="p-4 rounded-lg bg-blue-50 border border-blue-200">
              <h4 className="font-semibold text-blue-800 mb-2 flex items-center gap-2">
                <BarChart3 className="h-4 w-4" />
                دقة النماذج
              </h4>
              <p className="text-sm text-blue-700 leading-relaxed">
                نموذج الانحدار اللوجستي حقق دقة 66.7% بينما حققت شجرة القرار دقة 60%. قد تكون الدقة المحدودة ناتجة عن حجم العينة الصغير (50 موظفاً)
                أو تعقيد العلاقات بين المتغيرات التي لا يمكن التقاطها بنماذج خطية بسيطة.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

// ─── Main Page ──────────────────────────────────────────────────────────────

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-emerald-50/30">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 p-2.5 shadow-lg shadow-emerald-500/20">
                <BarChart3 className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl sm:text-2xl font-bold bg-gradient-to-l from-emerald-700 to-teal-600 bg-clip-text text-transparent">
                  لوحة تحليلات الموارد البشرية
                </h1>
                <p className="text-xs sm:text-sm text-muted-foreground">
                  تحليل شامل لأداء ورضا الموظفين | 50 موظف - 8 أقسام
                </p>
              </div>
            </div>
            <Badge variant="outline" className="hidden sm:flex items-center gap-1.5 bg-emerald-50 text-emerald-700 border-emerald-200">
              <div className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
              بيانات محدّثة
            </Badge>
          </div>
        </div>
      </header>

      {/* Dashboard Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <Tabs defaultValue="overview" className="w-full">
          <TabsList className="w-full flex bg-white/80 backdrop-blur-md border shadow-sm mb-6 h-auto p-1.5">
            <TabsTrigger value="overview" className="flex-1 py-2.5 text-sm sm:text-base gap-2">
              <BarChart3 className="h-4 w-4" />
              <span className="hidden sm:inline">المقاييس العامة</span>
              <span className="sm:hidden">عام</span>
            </TabsTrigger>
            <TabsTrigger value="departments" className="flex-1 py-2.5 text-sm sm:text-base gap-2">
              <Building2 className="h-4 w-4" />
              <span className="hidden sm:inline">تحليل الأقسام</span>
              <span className="sm:hidden">الأقسام</span>
            </TabsTrigger>
            <TabsTrigger value="satisfaction" className="flex-1 py-2.5 text-sm sm:text-base gap-2">
              <ScatterIcon className="h-4 w-4" />
              <span className="hidden sm:inline">الرضا مقابل الأداء</span>
              <span className="sm:hidden">الرضا</span>
            </TabsTrigger>
            <TabsTrigger value="predictive" className="flex-1 py-2.5 text-sm sm:text-base gap-2">
              <Brain className="h-4 w-4" />
              <span className="hidden sm:inline">التحليل التنبؤي</span>
              <span className="sm:hidden">تنبؤي</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="overview">
            <OverallMetricsTab />
          </TabsContent>
          <TabsContent value="departments">
            <DepartmentAnalysisTab />
          </TabsContent>
          <TabsContent value="satisfaction">
            <SatisfactionVsPerformanceTab />
          </TabsContent>
          <TabsContent value="predictive">
            <PredictiveAnalysisTab />
          </TabsContent>
        </Tabs>
      </div>

      {/* Footer */}
      <footer className="mt-auto border-t bg-white/60 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-center text-xs text-muted-foreground">
            لوحة تحليلات الموارد البشرية — تحليل البيانات من {(new Date().getFullYear())} | إجمالي 50 موظف عبر 8 أقسام
          </p>
        </div>
      </footer>
    </main>
  );
}
