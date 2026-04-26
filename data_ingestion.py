import pandas as pd
import logging

# إعداد نظام تسجيل الأخطاء (أسلوب مهندسي مايكروسوفت)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TrialBalanceProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.raw_data = None
        self.clean_data = None

    def load_data(self):
        """مهمة هذه الدالة قراءة ملف الإكسل فقط"""
        try:
            logging.info(f"جاري قراءة الملف: {self.file_path}")
            # استخدمنا openpyxl كمحرك لقراءة ملفات xlsx الحديثة
            self.raw_data = pd.read_excel(self.file_path, engine='openpyxl')
            logging.info("تمت قراءة الملف بنجاح.")
            
            # 👈 السطر المعماري المفقود: إرجاع البيانات للملف الرئيسي!
            return self.raw_data
            
        except Exception as e:
            logging.error(f"حدث خطأ أثناء قراءة الملف: {e}")
            raise

    def clean_and_normalize(self, df=None):
        # 1. المرونة الهندسية: إذا مررنا df استخدمه، وإلا ابحث عن self.df
        target_df = df if df is not None else getattr(self, 'raw_data', None)
        
        # 2. حماية النظام من الانهيار (Guard Clause)
        if target_df is None:
            raise ValueError("لم يتم تحميل البيانات! تأكد من استدعاء load_data() أولاً.")
            
        # 3. إزالة المسافات المخفية
        target_df.columns = target_df.columns.str.strip()
        
        # 4. قاموس المرادفات
        column_mapping = {
            'مدين': 'المدين',
            'دائن': 'الدائن',
            'الرصيد المدين': 'المدين',
            'الرصيد الدائن': 'الدائن',
            'حساب': 'اسم الحساب',
            'إسم الحساب': 'اسم الحساب',
            'رقم': 'رقم الحساب',
            'رقم حساب': 'رقم الحساب'
        }
        
        target_df.rename(columns=column_mapping, inplace=True)

        # 5. تنظيف البيانات الرياضية
        if 'المدين' in target_df.columns:
            target_df['المدين'] = pd.to_numeric(target_df['المدين'], errors='coerce').fillna(0)
            
        if 'الدائن' in target_df.columns:
            target_df['الدائن'] = pd.to_numeric(target_df['الدائن'], errors='coerce').fillna(0)
            
        # 6. تحديث البيانات داخل الكلاس وإرجاعها
        self.df = target_df
        return target_df

if __name__ == "__main__":
    # قمنا بتحديث اسم الملف هنا ليقرأ الملف الفوضوي الذي صنعناه
    processor = TrialBalanceProcessor("messy_trial_balance.xlsx")
    processor.load_data()
    clean_df = processor.clean_and_normalize()
    print("\n--- البيانات بعد التنظيف الهندسي ---")
    print(clean_df)