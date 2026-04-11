import google.generativeai as genai
from app.core.config import settings
from app.models.models import Task
from typing import List

class AIService:
    def __init__(self):
        # إعداد محرك Gemini باستخدام المفتاح الموجود في .env
        genai.configure(api_key=settings.AI_MODEL_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    async def get_task_suggestion(self, user_name: str, tasks: List[Task]) -> str:
        """
        إرسال قائمة المهام للـ AI والحصول على نصيحة ذكية.
        """
        if not tasks:
            return f"أهلاً {user_name}! ليس لديك مهام مسجلة حالياً. ما رأيك في إضافة أول مهمة لليوم؟"

        # صياغة الـ Prompt بشكل احترافي
        tasks_str = "\n".join([
            f"- {t.title} (الأولوية: {t.priority}, التصنيف: {t.category})"
            for t in tasks if not t.is_completed
        ])

        prompt = f"""
        أنت مساعد شخصي ذكي خبير في إدارة الوقت والإنتاجية.
        المستخدم اسمه: {user_name}
        لديه المهام التالية غير المكتملة لليوم:
        {tasks_str}

        بناءً على هذه القائمة، قدم له نصيحة واحدة ذكية ومختصرة جداً وجذابة باللغة العربية لكي يبدأ يومه بنشاط.
        بدلاً من سرد المهام، ركز على ما يجب البدء به ولماذا.
        ابدأ التحية بـ "يا باشا" أو "يا بطل".
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"عذراً {user_name}، واجهت مشكلة في تحليل المهام حالياً، لكن استمر في العمل الرائع!"

# إنشاء نسخة وحيدة من الخدمة (Singleton)
ai_service = AIService()
