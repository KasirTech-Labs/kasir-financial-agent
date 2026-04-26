import os
import logging
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FinancialAuditorAgent:
    def __init__(self):
        # 1. تحميل المفاتيح السرية من ملف .env بأمان
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            logging.error("لم يتم العثور على مفتاح GROQ_API_KEY في ملف .env!")
            raise ValueError("API Key is missing")

        # 2. تهيئة محرك Llama 3 عبر Groq (اخترنا النسخة الأسرع 8b أو الأذكى 70b)
        logging.info("جاري تهيئة الاتصال بنموذج Llama 3...")
        self.model_name = os.getenv("GROQ_MODEL_NAME", "llama-3.1-70b-versatile")
        self.llm = ChatGroq(
            temperature=0.2, 
            model_name=self.model_name, # نستخدم المتغير هنا
            groq_api_key=self.api_key
        )

    def analyze_discrepancy(self, reconciliation_report, clean_df):
        logging.info("الوكيل الذكي يبدأ تحليل الفروقات المالية...")
        
        # 3. تحويل جدول الباندا إلى نص (Markdown) ليفهمه النموذج اللغوي
        data_string = clean_df.to_markdown()
        
        # 4. هندسة التلقين (Prompt Engineering) الاحترافية
        system_prompt = """
        أنت مراجع حسابات مالي خبير (Senior Financial Auditor).
        تم إعطاؤك تقرير مطابقة ميزان مراجعة، بالإضافة إلى البيانات المالية النظيفة.
        
        تقرير المطابقة:
        {report}
        
        البيانات المالية:
        {data}
        
        مهمتك:
        1. تحليل المشكلة بناءً على الأرقام المقدمة.
        2. تحديد الحسابات التي قد تكون سبباً في عدم التوازن (العجز/الزيادة).
        3. كتابة تقرير تدقيق مالي موجز واحترافي باللغة العربية يشرح المشكلة ويقترح خطوات الحل للمحاسبين.
        
        اكتب التقرير بشكل مباشر دون مقدمات عامة.
        """
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "قم بتحليل البيانات وإصدار التقرير النهائي.")
        ])
        
        # 5. بناء السلسلة (Chain) وتنفيذها
        chain = prompt_template | self.llm
        
        logging.info("جاري توليد التقرير...")
        response = chain.invoke({
            "report": str(reconciliation_report),
            "data": data_string
        })
        
        return response.content

# ==========================================
# اختبار تكامل النظام بالكامل (End-to-End Test)
# ==========================================
if __name__ == "__main__":
    from data_ingestion import TrialBalanceProcessor
    from reconciliation import ReconciliationEngine
    
    print("\n[1] معالجة البيانات...")
    processor = TrialBalanceProcessor("messy_trial_balance.xlsx")
    processor.load_data()
    clean_df = processor.clean_and_normalize()
    
    print("\n[2] محرك المطابقة...")
    engine = ReconciliationEngine(clean_df)
    final_report = engine.run_checks()
    
    print("\n[3] تحليل الوكيل الذكي (Llama 3)...")
    agent = FinancialAuditorAgent()
    audit_report = agent.analyze_discrepancy(final_report, clean_df)
    
    print("\n" + "="*50)
    print(" 📄 تقرير التدقيق المالي النهائي ")
    print("="*50)
    print(audit_report)