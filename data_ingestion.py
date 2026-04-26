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
        # 1. إزالة أي مسافات مخفية قبل أو بعد أسماء الأعمدة (مشكلة شائعة جداً)
        self.df.columns = self.df.columns.str.strip()
        
        # 2. قاموس المرادفات (The Mapping Dictionary)
        # توحيد كل المسميات المحاسبية الشائعة إلى المسميات القياسية التي يفهمها نظامنا
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
        
        # تطبيق التوحيد على أسماء الأعمدة
        self.df.rename(columns=column_mapping, inplace=True)

        # 3. تنظيف البيانات الرياضية (التأكد من أن المبالغ عبارة عن أرقام وليس نصوصاً)
        if 'المدين' in self.df.columns:
            self.df['المدين'] = pd.to_numeric(self.df['المدين'], errors='coerce').fillna(0)
            
        if 'الدائن' in self.df.columns:
            self.df['الدائن'] = pd.to_numeric(self.df['الدائن'], errors='coerce').fillna(0)
            
        # إرجاع البيانات النظيفة للمحرك
        return self.df

if __name__ == "__main__":
    # قمنا بتحديث اسم الملف هنا ليقرأ الملف الفوضوي الذي صنعناه
    processor = TrialBalanceProcessor("messy_trial_balance.xlsx")
    processor.load_data()
    clean_df = processor.clean_and_normalize()
    print("\n--- البيانات بعد التنظيف الهندسي ---")
    print(clean_df)