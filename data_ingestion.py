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
        target_df = df if df is not None else getattr(self, 'raw_data', None)
        
        if target_df is None:
            raise ValueError("لم يتم تحميل البيانات! تأكد من استدعاء load_data() أولاً.")
            
        target_df.columns = target_df.columns.str.strip()
        
        column_mapping = {
            'مدين': 'المدين', 'دائن': 'الدائن',
            'حساب': 'اسم الحساب', 'إسم الحساب': 'اسم الحساب',
            'رقم': 'رقم الحساب', 'رقم حساب': 'رقم الحساب'
        }
        target_df.rename(columns=column_mapping, inplace=True)

        # =================================================================
        # 🚀 خوارزمية تصفية التداخل (Double Counting Filter)
        # =================================================================
        
        # 1. إزالة صف الإجمالي من أسفل الملف لأنه يضاعف الأرقام
        if 'اسم الحساب' in target_df.columns:
            target_df = target_df[~target_df['اسم الحساب'].astype(str).str.contains('الإجمالي|اجمالي', na=False)]

        # 2. استخراج الحسابات النهائية فقط (Leaf Nodes) باستخدام رقم الحساب
        if 'رقم الحساب' in target_df.columns:
            # إزالة الصفوف الفارغة (مثل عناوين: الأصول، الخصوم وحقوق الملكية)
            target_df = target_df.dropna(subset=['رقم الحساب'])
            target_df['رقم الحساب'] = target_df['رقم الحساب'].astype(str).str.strip()
            
            # استبعاد القيم التي قرأتها بايثون كـ 'nan' كنص
            target_df = target_df[target_df['رقم الحساب'] != 'nan']

            # استخراج جميع أرقام الحسابات الموجودة في الملف
            all_accounts = target_df['رقم الحساب'].tolist()

            # دالة داخلية تفحص ما إذا كان الحساب "نهائياً"
            def is_leaf(acc):
                for other in all_accounts:
                    # إذا وجدنا حساباً آخر يبدأ بنفس هذا الرقم (وأطول منه)، إذن هذا الحساب تجميعي (أب)
                    if other != acc and other.startswith(acc):
                        return False 
                return True # لا يوجد له أبناء، إذن هو حساب نهائي

            # تطبيق الدالة السحرية لإبقاء الحسابات النهائية فقط
            target_df['is_leaf'] = target_df['رقم الحساب'].apply(is_leaf)
            target_df = target_df[target_df['is_leaf'] == True]
            target_df = target_df.drop(columns=['is_leaf']) # تنظيف العمود المؤقت
            
        # =================================================================

        # تنظيف البيانات الرياضية
        if 'المدين' in target_df.columns:
            target_df['المدين'] = pd.to_numeric(target_df['المدين'], errors='coerce').fillna(0)
            
        if 'الدائن' in target_df.columns:
            target_df['الدائن'] = pd.to_numeric(target_df['الدائن'], errors='coerce').fillna(0)
            
        self.df = target_df
        return target_df

if __name__ == "__main__":
    # قمنا بتحديث اسم الملف هنا ليقرأ الملف الفوضوي الذي صنعناه
    processor = TrialBalanceProcessor("messy_trial_balance.xlsx")
    processor.load_data()
    clean_df = processor.clean_and_normalize()
    print("\n--- البيانات بعد التنظيف الهندسي ---")
    print(clean_df)