from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os
import logging

# استدعاء وحدات النظام التي قمت ببرمجتها بعبقرية
from data_ingestion import TrialBalanceProcessor
from reconciliation import ReconciliationEngine
from ai_agent import FinancialAuditorAgent

# إعداد السيرفر
app = FastAPI(title="Kasir Tech - Financial AI Agent API", version="1.0")

@app.get("/")
async def root_health_check():
    """
    نقطة فحص الصحة (Health Check). 
    تخبر أنظمة المراقبة والمستخدمين أن السيرفر يعمل بكفاءة.
    """
    return {
        "status": "online",
        "service": "Kasir Tech Financial AI Agent",
        "message": "السيرفر يعمل بكفاءة. يرجى التوجه إلى /docs لاستخدام الواجهة البرمجية."
    }

# مسار مؤقت لحفظ الملفات المرفوعة
TEMP_FILE_PATH = "temp_uploaded_tb.xlsx"

@app.post("/audit-trial-balance/")
async def audit_trial_balance(file: UploadFile = File(...)):
    """
    هذا هو المنفذ (Endpoint) الذي سيستقبل ملفات الإكسل من أي مكان في العالم
    """
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="يجب أن يكون الملف بصيغة Excel (.xlsx)")

    try:
        # 1. حفظ الملف المرفوع مؤقتاً
        with open(TEMP_FILE_PATH, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        logging.info(f"تم استقبال الملف: {file.filename}")

        # 2. تشغيل مسار تنظيف البيانات (المرحلة 1)
        processor = TrialBalanceProcessor(TEMP_FILE_PATH)
        
        # نعدل الكود ليقوم باستلام البيانات من دالة التحميل وتمريرها فوراً لدالة التنظيف
        raw_df = processor.load_data() 
        clean_df = processor.clean_and_normalize(raw_df) # تمرير صريح للبيانات

        # 3. تشغيل محرك المطابقة (المرحلة 2)
        engine = ReconciliationEngine(clean_df)
        reconciliation_report = engine.run_checks()

        # 4. تشغيل الوكيل الذكي (المرحلة 3)
        agent = FinancialAuditorAgent()
        audit_report = agent.analyze_discrepancy(reconciliation_report, clean_df)

        # 5. تنظيف البيئة (حذف الملف المؤقت)
        if os.path.exists(TEMP_FILE_PATH):
            os.remove(TEMP_FILE_PATH)

        # 6. إرجاع النتيجة النهائية للمستخدم
        return {
            "status": "success",
            "math_analysis": reconciliation_report,
            "ai_audit_report": audit_report
        }

    except Exception as e:
        # في حال حدوث أي خطأ، نعيد رسالة خطأ واضحة
        raise HTTPException(status_code=500, detail=str(e))