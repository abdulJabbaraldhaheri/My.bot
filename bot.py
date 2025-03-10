from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import logging
import time
import os

# إعدادات تسجيل الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# دالة للتحقق من الاتصال بالإنترنت
def check_internet_connection():
    try:
        # محاولة الاتصال بموقع معروف (مثل Google)
        os.system("ping -c 1 google.com > /dev/null 2>&1")
        return True
    except Exception as e:
        return False

# دالة بدء البوت
async def start(update: Update, context):
    user = update.effective_user
    user_data = """🎉 مرحبًا بك في بوت عبد الجبار الظاهري! 🎉

🤖 هذا البوت يحتوي على العديد من الأقسام المخصصة لدفعة تقنية المعلومات في جامعة السعيدة.

📚 **ملازم:** هنا سيتم توفير الملازم الدراسية على مدار السنوات الدراسية 🤗.
📝 **ملخصات ودفاتر:** سيتم بقدر المستطاع توفير الملخصات والدفاتر لمساعدتك في المراجعة 📖.
📹 **صور محاضرات:** سيتم مشاركة الصور المهمة للمحاضرات كمرجع في المستقبل إن شاء الله 📸.
💻 **أكواد وبرامج:** سيتم توفير الأكواد والبرامج التي ستساعدنا في مشاريعنا الدراسية 💡.
📱 **برامج وتطبيقات:** هنا ستجد برامج وتطبيقات مفيدة لدراستك وعملك 💾.

🌟 أنا هنا لمساعدتك في الحصول على أفضل المحتويات التعليمية التي تحتاجها لدراستك 🚀.

📱 **للتواصل: 773907583**
 **واتساب:** [اضغط هنا للتواصل عبر واتساب](https://wa.me/966773907583)

 📨 **تلغرام:** [اضغط هنا للتواصل عبر تلغرام](https://t.me/abdul7jabbar)

 ✨ **نحن هنا لخدمتكم! لمساعدة في التواصل معنا لأي استفسار أو مساعدةمساعدةì
"""

    # طباعة بيانات المستخدم في السجل
    logging.info(f"User joined: {user.first_name} {user.last_name} | Username: @{user.username} | ID: {user.id}")

    await update.message.reply_text(user_data)

    # إرسال القوائم
    reply_markup = ReplyKeyboardMarkup(
        [
            [KeyboardButton("📚 ملازم"), KeyboardButton("📝 ملخصات ودفاتر")],
            [KeyboardButton("📹 صور محاضرات"), KeyboardButton("💻 أكواد وبرامج")],
            [KeyboardButton("📱 برامج وتطبيقات")],
        ],
        resize_keyboard=True
    )

    await update.message.reply_text(
        "اختر القسم الذي تود الوصول إليه:",
        reply_markup=reply_markup
    )

# دالة لمعالجة القوائم
async def handle_message(update: Update, context):
    user_message = update.message.text

    # القائمة الرئيسية
    if user_message == "📚 ملازم":
        reply_markup = ReplyKeyboardMarkup(
            [
                [KeyboardButton("📅 سنة أولى"), KeyboardButton("📅 سنة ثانية")],
                [KeyboardButton("📅 سنة ثالثة"), KeyboardButton("📅 سنة رابعة")],
                [KeyboardButton("🔙 العودة إلى القائمة الرئيسية")],
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "اختر السنة التي تود الوصول إليها:",
            reply_markup=reply_markup
        )

    # قوائم السنوات
    elif user_message in ["📅 سنة أولى", "📅 سنة ثانية", "📅 سنة ثالثة", "📅 سنة رابعة"]:
        # تخزين السنة المختارة في context.user_data
        context.user_data['selected_year'] = user_message
        reply_markup = ReplyKeyboardMarkup(
            [
                [KeyboardButton("📆 ترم أول"), KeyboardButton("📆 ترم ثاني")],
                [KeyboardButton("🔙 العودة إلى قسم الملازم")],
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            f"🎓 اختر الترم الذي تود الاطلاع على محتوياته لـ {user_message}.",
            reply_markup=reply_markup
        )

    # قوائم الترم
    elif user_message in ["📆 ترم أول", "📆 ترم ثاني"]:
        # تخزين الترم المختار في context.user_data
        context.user_data['selected_term'] = user_message
        reply_markup = ReplyKeyboardMarkup(
            [
                [KeyboardButton("📂 الملف رابط مباشر"), KeyboardButton("📥 الملف جاهز")],
                [KeyboardButton("🔙 العودة إلى السنة")],
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            f"📚 اختر نوع الملف الذي تود الاطلاع عليه في {user_message}.",
            reply_markup=reply_markup
        )

    # قوائم الملفات
    elif user_message == "📂 الملف رابط مباشر":
        # استرجاع السنة والترم المختارين من context.user_data
        selected_year = context.user_data.get('selected_year', '')
        selected_term = context.user_data.get('selected_term', '')

        if selected_year == "📅 سنة أولى" and selected_term == "📆 ترم أول":
            reply_markup = ReplyKeyboardMarkup(
                [
                    [KeyboardButton("📚 ملزمة اللغة العربية"), KeyboardButton("🕌 ملزمة الثقافة الإسلامية")],
                    [KeyboardButton("💻 ملزمة برمجة الحاسوب"), KeyboardButton("📘 ملزمة مهارات الحاسوب عملي")],
                    [KeyboardButton("📘 ملزمة مهارات الحاسوب نظري"), KeyboardButton("📝 ملزمة اللغة الإنجليزية")],
                    [KeyboardButton("🔙 العودة إلى الترم")],
                ],
                resize_keyboard=True
            )
            await update.message.reply_text(
                "📂 اختر الملزمة التي تود تنزيلها من الروابط أدناه:",
                reply_markup=reply_markup
            )
        elif selected_year == "📅 سنة أولى" and selected_term == "📆 ترم ثاني":
            reply_markup = ReplyKeyboardMarkup(
                [
                    [KeyboardButton("🧮 التصميم المنطقي"), KeyboardButton("💡 مقدمة في تقنية المعلومات")],
                    [KeyboardButton("📐 رياضيات"), KeyboardButton("📝 اللغة الإنجليزية")],
                    [KeyboardButton("📊 الإحصاء والاحتمالات"), KeyboardButton("💻 برمجة الحاسوب")],
                    [KeyboardButton("📞 مهارات الاتصال"), KeyboardButton("🔙 العودة إلى الترم")],
                ],
                resize_keyboard=True
            )
            await update.message.reply_text(
                "📂 اختر الملزمة التي تود تنزيلها من الروابط أدناه:",
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                "😊💖 سيتم إضافة البيانات قريبًا. شكرًا لتفهمك!"
            )

    # روابط الملازم
    elif user_message == "📚 ملزمة اللغة العربية":
        await update.message.reply_text(
            "📚 ملزمة اللغة العربية:\n\nرابط التنزيل:\nhttps://drive.google.com/file/d/17W0UegYV3U5awM5LWT6-O3Z22bw6K-Dz/view?usp=sharing"
        )

    elif user_message == "🕌 ملزمة الثقافة الإسلامية":
        await update.message.reply_text(
            "🕌 ملزمة الثقافة الإسلامية:\n\nرابط التنزيل:\nhttps://drive.google.com/file/d/17VuZqjcwuRwezzDHiw2aTlvSDnzffynx/view?usp=sharing"
        )

    elif user_message == "💻 ملزمة برمجة الحاسوب":
        await update.message.reply_text(
            "💻 ملزمة برمجة الحاسوب:\n\nرابط التنزيل:\nhttps://drive.google.com/file/d/17WeDphPwJ2VefEdsdF115g9jLS8bZU32/view?usp=sharing"
        )

    elif user_message == "📘 ملزمة مهارات الحاسوب عملي":
        await update.message.reply_text(
            "📘 ملزمة مهارات الحاسوب عملي:\n\nرابط التنزيل:\nhttps://drive.google.com/file/d/17XyY6Ukxf6OAdm1auDQArNmofqdXIxNE/view?usp=sharing"
        )

    elif user_message == "📘 ملزمة مهارات الحاسوب نظري":
        await update.message.reply_text(
            "📘 ملزمة مهارات الحاسوب نظري:\n\nرابط التنزيل:\nhttps://drive.google.com/file/d/17YnGLmsq1-ECIPEoLIp0-IhWMC1oNrGz/view?usp=sharing"
        )

    elif user_message == "📝 ملزمة اللغة الإنجليزية":
        await update.message.reply_text(
            "📝 ملزمة اللغة الإنجليزية:\n\nرابط التنزيل:\nhttps://drive.google.com/file/d/17YnGLmsq1-ECIPEoLIp0-IhWMC1oNrGz/view?usp=sharing"
        )

    # روابط الملازم لترم ثاني سنة أولى
    elif user_message == "🧮 التصميم المنطقي":
        await update.message.reply_text(
            "🧮 التصميم المنطقي:\n\nرابط التنزيل:\nhttps://drive.google.com/file/d/18qJnAia6XfcijUwzotwE3XcR-OegGK0K/view?usp=sharing"
        )

    elif user_message == "💡 مقدمة في تقنية المعلومات":
        await update.message.reply_text(
            "💡 مقدمة في تقنية المعلومات:\n\nرابط التنزيل:\nhttps://drive.google.com/file/d/19hY8iylSxF7kfM2sRD4qmY86HkHpcLOf/view?usp=sharing"
        )

    elif user_message == "📐 ري��ضيات":
        await update.message.reply_text(
            "📐 رياضيات:\n\nرابط التنزيل:\nسيتم إضافة البيانات قريبًا. شكرًا لتفهمك😊💖 "
        )

    elif user_message == "📊 الإحصاء والاحتمالات":
        await update.message.reply_text(
            "📊 الإحصاء والاحتمالات:\n\nرابط التنزيل:\nسيتم إضافة البيانات قريبًا. شكرًا لتفهمك😊💖 "
        )

    elif user_message == "💻 برمجة الحاسوب":
        await update.message.reply_text(
            "💻 برمجة الحاسوب:\n\nرابط التنزيل:\n سيتم إضافة البيانات قريبًا. شكرًا لتفهمك😊💖 "
        )

    elif user_message == "📞 مهارات الاتصال":
        await update.message.reply_text(
            "📞 مهارات الاتصال:\n\nرابط التنزيل:\nhttps://drive.google.com/file/d/1IxKBzgSTxNN3WqBP7_VJ5CqkdDtCZewV/view?usp=sharing"
        )

    # قائمة برامج وتطبيقات
    elif user_message == "📱 برامج وتطبيقات":
        reply_markup = ReplyKeyboardMarkup(
            [
                [KeyboardButton("تطبيق محاكاة التصميم المنطقي")],
                [KeyboardButton("🔙 العودة إلى القائمة الرئيسية")],
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "📱 اختر القسم الذي تود الوصول إليه:",
            reply_markup=reply_markup
        )

    # قائمة تطبيق محاكاة التصميم المنطقي
    elif user_message == "تطبيق محاكاة التصميم المنطقي":
        reply_markup = ReplyKeyboardMarkup(
            [
                [KeyboardButton("📥 الملف جاهز"), KeyboardButton("📂 الملف برابط مباشر")],
                [KeyboardButton("🔙 العودة إلى برامج وتطبيقات")],
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "اختر الطريقة التي تود الحصول على التطبيق:",
            reply_markup=reply_markup
        )

    # قائمة الملف جاهز
    elif user_message == "📥 الملف جاهز":
        await update.message.reply_text(
            "📥 الملف جاهز:\n\nسيتم التوفير قريبًا 😊🌷"
        )

    # قائمة الملف برابط مباشر
    elif user_message == "📂 الملف برابط مباشر":
        await update.message.reply_text(
            "📂 الملف برابط مباشر:\n\nرابط تنزيل \nhttps://drive.google.com/file/d/1KjYHSCZJEWGsU6YARQ5G4Al9nnsfL3xR/view?usp=sharing"
        )

    # قائمة ملخصات ودفاتر
    elif user_message == "📝 ملخصات ودفاتر":
        reply_markup = ReplyKeyboardMarkup(
            [
                [KeyboardButton("📝 ملخصات"), KeyboardButton("📒 دفاتر")],
                [KeyboardButton("🔙 العودة إلى القائمة الرئيسية")],
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "اختر القسم الذي تود الوصول إليه:",
            reply_markup=reply_markup
        )

    # قائمة ملخصات
    elif user_message == "📝 ملخصات":
        await update.message.reply_text(
            "📝 ملخصات:\n\nسيتم إضافة الملخصات قريبًا. شكرًا لتفهمك😊💖"
        )

    # قائمة دفاتر
    elif user_message == "📒 دفاتر":
        reply_markup = ReplyKeyboardMarkup(
            [
                [KeyboardButton("📒 دفاتر سنة أولى"), KeyboardButton("📒 دفاتر سنة ثانية")],
                [KeyboardButton("📒 دفاتر سنة ثالثة"), KeyboardButton("📒 دفاتر سنة رابعة")],
                [KeyboardButton("🔙 العودة إلى ملخصات ودفاتر")],
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "اختر السنة التي تود الوصول إليها:",
            reply_markup=reply_markup
        )

    # قوائم دفاتر السنوات
    elif user_message in ["📒 دفاتر سنة أولى", "📒 دفاتر سنة ثانية", "📒 دفاتر سنة ثالثة", "📒 دفاتر سنة رابعة"]:
        context.user_data['selected_year'] = user_message
        reply_markup = ReplyKeyboardMarkup(
            [
                [KeyboardButton("📒 دفاتر ترم أول"), KeyboardButton("📒 دفاتر ترم ثاني")],
                [KeyboardButton("🔙 العودة إلى دفاتر")],
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            f"اختر الترم الذي تود الاطلاع على دفاتره لـ {user_message}:",
            reply_markup=reply_markup
        )

    # قوائم دفاتر الترم
    elif user_message in ["📒 دفاتر ترم أول", "📒 دفاتر ترم ثاني"]:
        context.user_data['selected_term'] = user_message
        selected_year = context.user_data.get('selected_year', '')

        if selected_year == "📒 دفاتر سنة أولى" and user_message == "📒 دفاتر ترم ثاني":
            reply_markup = ReplyKeyboardMarkup(
                [
                    [KeyboardButton("📒 دفتر الرياضيات"), KeyboardButton("📒 دفتر الإحصاء والاحتمالات")],
                    [KeyboardButton("📒 دفتر التصميم المنطقي"), KeyboardButton("📒 دفتر مقدمة في تقنية المعلومات")],
                    [KeyboardButton("📒 دفتر اللغة الإنجليزية"), KeyboardButton("📒 دفتر برمجة الحاسوب")],
                    [KeyboardButton("📒 دفتر مهارات الاتصال"), KeyboardButton("🔙 العودة إلى دفاتر سنة أولى")],
                ],
                resize_keyboard=True
            )
            await update.message.reply_text(
                "اختر الدفتر الذي تود تنزيله:",
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                "😊💖 سيتم إضافة البيانات قريبًا. شكرًا لتفهمك!"
            )

   # روابط دفاتر سنة أولى ترم ثاني
    elif user_message == "📒 دفتر الرياضيات":
        await update.message.reply_text(
            "📒 دفتر الرياضيات:\n إعداد الطالب:- سلمان العزب \n\nرابط التنزيل:\nhttps://drive.google.com/file/d/1QhOMp3sW6EappwY8u3DAEk2UoC1M7wGJ/view?usp=drivesdk"
       )

    elif user_message == "📒 دفتر الإحصاء والاحتمالات":
        await update.message.reply_text(
            "📒 دفتر الإحصاء والاحتمالات:\n إعداد الطالب:- سلمان العزب \n\nرابط التنزيل:\nhttps://drive.google.com/file/d/1QyBdcPWQqLP60ZBSpRUB1vfNXj-88vm0/view?usp=drivesdk"

"\n📒 دفتر الإحصاء والاحتمالات:\n إعداد الطالبة :- اماني النجار \n\nرابط التنزيل:\nhttps://drive.google.com/file/d/1R2gnHQNaErHrIw1p4zZHBeAMrup3Ockc/view?usp=drivesdk"

 )

    elif user_message == "📒 دفتر التصميم المنطقي":
        await update.message.reply_text(
            "📒 دفتر التصميم المنطقي:\n\nرابط التنزيل:\nسيتم إضافته قريبًا😊💖"
        )

    elif user_message == "📒 دفتر مقدمة في تقنية المعلومات":
        await update.message.reply_text(
            "📒 دفتر مقدمة في تقنية المعلومات:\n\nرابط التنزيل:\nسيتم إضافته قريبًا😊💖"

      )

    elif user_message == "📒 دفتر اللغة الإنجليزية":
        await update.message.reply_text(
            "📒 دفتر اللغة الإنجليزية:\n\nرابط التنزيل:\nسيتم إضافته قريبًا😊💖"
        )

    elif user_message == "📒 دفتر برمجة الحاسوب":
        await update.message.reply_text(
            "📒 دفتر برمجة الحاسوب:\n\nرابط التنزيل:\nسيتم إضافته قريبًا😊💖"
        )

    elif user_message == "📒 دفتر مهارات الاتصال":
        await update.message.reply_text(
            "📒 دفتر مهارات الاتصال:\n\nرابط التنزيل:\nسيتم إضافته قريبًا😊💖"
        )

    # العودة بين القوائم
    elif user_message == "🔙 العودة إلى الترم":
        reply_markup = ReplyKeyboardMarkup(
            [
                [KeyboardButton("📂 الملف رابط مباشر"), KeyboardButton("📥 الملف جاهز")],
                [KeyboardButton("🔙 العودة إلى السنة")],
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "📚 اختر نوع الملف الذي تود الاطلاع عليه.",
            reply_markup=reply_markup
        )

    elif user_message == "🔙 العودة إلى السنة":
        reply_markup = ReplyKeyboardMarkup(
            [
                [KeyboardButton("📆 ترم أول"), KeyboardButton("📆 ترم ثاني")],
                [KeyboardButton("🔙 العودة إلى قسم الملازم")],
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "🎓 اختر الترم الذي تود الاطلاع على محتوياته.",
            reply_markup=reply_markup
        )

    elif user_message == "🔙 العودة إلى قسم الملازم":
        reply_markup = ReplyKeyboardMarkup(
            [
                [KeyboardButton("📅 سنة أولى"), KeyboardButton("📅 سنة ثانية")],
                [KeyboardButton("📅 سنة ثالثة"), KeyboardButton("📅 سنة رابعة")],
                [KeyboardButton("🔙 العودة إلى القائمة الرئيسية")],
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "اختر السنة التي تود الوصول إليها:",
            reply_markup=reply_markup
        )

    elif user_message == "🔙 العودة إلى برامج وتطبيقات":
        reply_markup = ReplyKeyboardMarkup(
            [
                [KeyboardButton("تطبيق محاكاة التصميم المنطقي")],
                [KeyboardButton("🔙 العودة إلى القائمة الرئيسية")],
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "📱 اختر القسم الذي تود الوصول إليه:",
            reply_markup=reply_markup
        )

    elif user_message == "🔙 العودة إلى ملخصات ودفاتر":
        reply_markup = ReplyKeyboardMarkup(
            [
                [KeyboardButton("📝 ملخصات"), KeyboardButton("📒 دفاتر")],
                [KeyboardButton("🔙 العودة إلى القائمة الرئيسية")],
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "اختر القسم الذي تود الوصول إليه:",
            reply_markup=reply_markup
        )

    elif user_message == "🔙 العودة إلى دفاتر":
        reply_markup = ReplyKeyboardMarkup(
            [
                [KeyboardButton("📒 دفاتر سنة أولى"), KeyboardButton("📒 دفاتر سنة ثانية")],
                [KeyboardButton("📒 دفاتر سنة ثالثة"), KeyboardButton("📒 دفاتر سنة رابعة")],
                [KeyboardButton("🔙 العودة إلى ملخصات ودفاتر")],
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "اختر السنة التي تود الوصول إليها:",
            reply_markup=reply_markup
        )

    elif user_message == "🔙 العودة إلى دفاتر سنة أولى":
        reply_markup = ReplyKeyboardMarkup(
            [
                [KeyboardButton("📒 دفاتر ترم أول"), KeyboardButton("📒 دفاتر ترم ثاني")],
                [KeyboardButton("🔙 العودة إلى دفاتر")],
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "اختر الترم الذي تود الاطلاع على دفاتره:",
            reply_markup=reply_markup
        )

    elif user_message == "🔙 العودة إلى القائمة الرئيسية":
        reply_markup = ReplyKeyboardMarkup(
            [
                [KeyboardButton("📚 ملازم"), KeyboardButton("📝 ملخصات ودفاتر")],
                [KeyboardButton("📹 صور محاضرات"), KeyboardButton("💻 أكواد وبرامج")],
                [KeyboardButton("📱 برامج وتطبيقات")],
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "اختر القسم الذي تود الوصول إليه:",
            reply_markup=reply_markup
        )

    else:
        await update.message.reply_text("😊💖 سيتم إضافة البيانات قريبًا. شكرًا لتفهمك!")

# تشغيل البوت مع إعادة التشغيل التلقائي عند الاتصال بالإنترنت
def run_bot():
    app = ApplicationBuilder().token("7617142739:AAGu5DdYlVwi5y1b0bniv5tmXY54jIwSkdU").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    while True:
        if check_internet_connection():
            try:
                run_bot()
            except Exception as e:
                logging.error(f"حدث خطأ: {e}, إعادة التشغيل بعد 10 ثوانٍ...")
                time.sleep(10)  # انتظر 10 ثوانٍ ثم حاول تشغيل البوت مرة أخرى
        else:
            logging.info("لا يوجد اتصال بالإنترنت، جاري الانتظار...")
            time.sleep(10)  # انتظر 10 ثوانٍ ثم حاول التحقق من الاتصال مرة أخرى
