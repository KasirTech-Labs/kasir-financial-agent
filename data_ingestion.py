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
        except Exception as e:
            logging.error(f"حدث خطأ أثناء قراءة الملف: {e}")
            raise

    def clean_and_normalize(self):
        logging.info("بدء عملية تنظيف البيانات...")
        df = self.raw_data.copy()
        
        # 1. حذف الصفوف الفارغة بالكامل
        df.dropna(how='all', inplace=True)
        
        # 2. توحيد أسماء الأعمدة (إزالة المسافات المخفية)
        df.columns = df.columns.str.strip()
        
        # 3. تنظيف الأعمدة المالية (المدين والدائن)
        financial_columns = ['المدين', 'الدائن']
        for col in financial_columns:
            # تحويل كل شيء لنص مؤقتاً لتجنب أخطاء تضارب الأنواع
            df[col] = df[col].astype(str)
            
            # إزالة المسافات من الأطراف
            df[col] = df[col].str.strip()
            
            # تحويل الشرطة المحاسبية إلى صفر
            df[col] = df[col].replace('-', '0')
            
            # إزالة أي نصوص أو فواصل (SAR, $, ,) وإبقاء الأرقام فقط
            df[col] = df[col].replace(r'[^\d\.]', '', regex=True)
            
            # تحويل العمود إلى أرقام عشرية حقيقية
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
        # 4. إصلاح أرقام الحسابات (إزالة الأصفار العشرية مثل 1001.0)
        df['رقم الحساب'] = pd.to_numeric(df['رقم الحساب'], errors='coerce').astype('Int64')
        
        self.clean_data = df
        logging.info("اكتمل تنظيف البيانات بنجاح.")
        return self.clean_data


if __name__ == "__main__":
    # قمنا بتحديث اسم الملف هنا ليقرأ الملف الفوضوي الذي صنعناه
    processor = TrialBalanceProcessor("messy_trial_balance.xlsx")
    processor.load_data()
    clean_df = processor.clean_and_normalize()
    print("\n--- البيانات بعد التنظيف الهندسي ---")
    print(clean_df)