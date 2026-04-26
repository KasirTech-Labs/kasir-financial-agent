import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ReconciliationEngine:
    def __init__(self, clean_data):
        # 1. المحرك يستقبل البيانات النظيفة كـ (DataFrame) وليس كملف إكسل
        self.df = clean_data
        self.total_debit = 0
        self.total_credit = 0
        self.difference = 0
        self.is_balanced = False

    def run_checks(self):
        logging.info("بدء تشغيل محرك المطابقة (Reconciliation Engine)...")
        
        # 2. حساب المجاميع باستخدام دوال الباندا السريعة (Vectorized Operations)
        self.total_debit = self.df['المدين'].sum()
        self.total_credit = self.df['الدائن'].sum()
        
        # 3. حساب الفرق المطلق (Absolute Difference)
        self.difference = abs(self.total_debit - self.total_credit)
        
        # 4. التحقق من التوازن (مع التقريب لتجنب أخطاء الفواصل العشرية في البرمجة)
        if round(self.difference, 2) == 0:
            self.is_balanced = True
            logging.info("الميزان متطابق 100%. لا توجد فروقات.")
        else:
            self.is_balanced = False
            logging.warning(f"تحذير هندسي: الميزان غير متطابق. يوجد عجز/زيادة بقيمة: {self.difference}")
            
        return self.get_report()

    def get_report(self):
        # 5. التغليف في (JSON / Dictionary)
        # لماذا؟ لأن واجهات الـ API ونماذج الذكاء الاصطناعي تعشق هذه الصيغة لقراءتها
        report = {
            "Total_Debit": float(self.total_debit),
            "Total_Credit": float(self.total_credit),
            "Difference": float(self.difference),
            "Is_Balanced": self.is_balanced
        }
        return report

# ==========================================
# اختبار التكامل (Integration Test)
# هنا نقوم بربط المرحلة 1 بالمرحلة 2
# ==========================================
if __name__ == "__main__":
    # استدعاء المصنع من الملف الأول الذي برمجته أنت
    from data_ingestion import TrialBalanceProcessor
    
    print("\n--- 1. تشغيل مسار البيانات ---")
    processor = TrialBalanceProcessor("messy_trial_balance.xlsx")
    processor.load_data()
    clean_df = processor.clean_and_normalize()
    
    print("\n--- 2. تمرير البيانات لمحرك المطابقة ---")
    engine = ReconciliationEngine(clean_df)
    final_report = engine.run_checks()
    
    print("\n--- النتيجة النهائية للمحرك (JSON format) ---")
    print(final_report)