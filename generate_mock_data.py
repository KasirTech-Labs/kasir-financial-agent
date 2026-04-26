import pandas as pd
import numpy as np

def create_messy_trial_balance():
    print("جاري بناء ميزان المراجعة الفوضوي...")
    
    # 1. تعمدنا وضع مسافات قبل وبعد أسماء الأعمدة
    # 2. تعمدنا إدخال رموز ونصوص في حقول الأرقام (SAR, $, -)
    data = {
        'رقم الحساب ': [1001, np.nan, 1002, 1003, np.nan, 2001, 2002], 
        '  اسم الحساب': ['النقدية (بنك)', np.nan, 'العملاء', 'المخزون', np.nan, 'الموردين', 'قروض بنكية'], 
        ' المدين ': [' 50000 ', np.nan, '15000 SAR', '20,000', np.nan, '-', '0'], 
        'الدائن': ['0', np.nan, '0', '-', np.nan, '12000 $', ' 30000 ']
    }

    df = pd.DataFrame(data)

    # حفظ البيانات في ملف إكسل
    file_name = "messy_trial_balance.xlsx"
    df.to_excel(file_name, index=False)
    
    print(f"تم إنشاء الملف بنجاح باسم: {file_name}")
    print("البيانات قبل التنظيف تبدو هكذا:")
    print(df)

if __name__ == "__main__":
    create_messy_trial_balance()
    #python generate_mock_data.py