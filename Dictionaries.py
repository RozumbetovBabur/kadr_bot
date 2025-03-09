# Dictionaries.py

TEXTS = {
    "start": {
        1: "Tildi saylań! 👇",
        2: "Tilni tanlang! 👇",
        3: "Выберите язык! 👇"
    },
    "ask_name": {
        1: "Atıńızdı kiritiń:",
        2: "Ismingizni kiriting:",
        3: "Введите ваше имя:"
    },
    "ask_surname": {
        1: "Famılıyańızdı kiritiń:",
        2: "Familiyangizni kiriting:",
        3: "Введите вашу фамилию:"
    },
    "ask_phone": {
        1: "Telefon nomerińizdi jeberiń 📞",
        2: "Telefon raqamingizni jo‘nating 📞",
        3: "Отправьте свой номер телефона 📞"
    },
    "main_menu": {
        1: "🔽 Tiykarǵı menyu",
        2: "🔽 Asosiy menyu",
        3: "🔽 Главное меню"
    },
    "profile": {
        1: "👤 **Sizdiń profilińiz**\n\n📛 Atıńız: {first_name}\n🆔 Familiyańız : {last_name}\n📞 Telefon nomerńiz: {phone}",
        2: "👤 **Sizning profilingiz**\n\n📛 Ism: {first_name}\n🆔 Familiya: {last_name}\n📞 Telefon: {phone}",
        3: "👤 **Ваш профиль**\n\n📛 Имя: {first_name}\n🆔 Фамилия: {last_name}\n📞 Телефон: {phone}"
    },
    "phone": {
        1: "📲 Kontakt jıberiw",
        2: "📲 Kontakt jo‘natish",
        3: "📲 Отправить контакт"
    },
    "Profil": {
        1: "👤 Profilńiz",
        2: "👤 Profilngiz",
        3: "👤 Ваш профиль"
    },
    "jobs": {
        1: "📂 Jumısqa hújjet tapsırıw",
        2: "📂 Ishga hujjat topshirish",
        3: "📂 Заявка на работу"
    },
    "update": {
        1: "⚠️ Profil tabılmadı! /start di basıp qaytan dizimnen ótiń.",
        2: "⚠️ Profil topilmadi! /start ni bosib qayta ro‘yxatdan o‘ting.",
        3: "⚠️ Профиль не найден! Зарегистрируйтесь еще раз, нажав /start."
    },
    "registered": {
        1: "Siz aldın ro'yhatnan ótkensiz!",
        2: "Siz ro‘yxatdan o‘tgansiz!",
        3: "Вы уже зарегистрированы!"
    },
    "profile_btn": {
        1: "👤 Profil",
        2: "👤 Profil",
        3: "👤 Профиль"
    },
    "jobs_btn": {
        1: "📂 Jumısqa hújjet tapsırıw",
        2: "📂 Ishga hujjat topshirish",
        3: "📂 Заявка на работу"
    },
    "change_lang": {
        1: "🌍 Tildi ózgertiw ushın tildi saylań!",
        2: "🌍 Tilni o'zgartirish uchun tilni tanlang!",
        3: "🌍 Выберите язык для изменения!"
    },
    "ask_cv": {
        1: "📄 Obiektivka (maǵlıwmatnama) hújjetin jiberiń (PDF, DOC, JPG, ZIP formatlarında ).",
        2: "📄 Obyektivka (malumotnoma) hujjatini jo‘nating (PDF, DOC, JPG, ZIP formatlarida).",
        3: "📄 Отправьте документ об объективе (в форматах PDF, DOC, JPG, ZIP)"
    },
    "ask_diplom": {
        1: "✅ Obiektivka qabıllandı. Endi diplomdı jiberiw (PDF, DOC, JPG, ZIP formatlarında).",
        2: "✅ Obyektivka qabul qilindi. Endi diplomni jo‘natish (PDF, DOC, JPG, ZIP formatlarida).",
        3: "✅ Объектив принят. Теперь отправь диплом (в форматах PDF, DOC, JPG, ZIP)."
    },
    "yes": {
            1: "Awa",
            2: "Ha",
            3: "Да"
    },
    "no": {
            1: "Yaq",
            2: "Yo‘q",
            3: "Нет"
    },
    "ask_certificate": {
        1: "📜 Sizde shet-tili boyınsha sertifikat barma?",
        2: "📜 Sizda chet-tili bo‘yicha sertifikat bormi?",
        3: "📜 Есть ли у вас сертификат иностранного языка?"
    },
    "ask_cert_upload": {
        1: "📜 Sertifikattı jıberiw (JPG, PDF, DOC, ZIP).",
        2: "📜 Sertifikatni jo‘natish (JPG, PDF, DOC, ZIP).",
        3: "📜 Отправить сертификат (JPG, PDF, DOC, ZIP)."
    },
    "ask_send": {
        1: "✅ Sertifikat qabıllandı.",
        2: "✅ Sertifikat qabul qilindi.",
        3: "✅ Сертификат принят."
    },
    "ask_cer_ha": {
        1: "📜 Sertifikatdı jiberiw (PDF, DOC, JPG, ZIP formatlarında ).",
        2: "📜 Sertifikatni jo‘natish (PDF, DOC, JPG, ZIP formatlarida)..",
        3: "📜 Отправить сертификат (в форматах PDF, DOC, JPG, ZIP)."
    },
    "ask_cer_load": {
        1: "✅ Hújjetlerińiz qabıllandı...",
        2: "✅ Hujjatlaringiz qabul qilindi...",
        3: "✅ Ваши документы получены..."
    },
    "send_to_group": {
        1: "📌 Jańa hújjetler:\n👨💼 Atı: {first_name}\n🆔 Familiyası: {last_name}\n📞 Telefon nomeri: {phone}",
        2: "📌 Yangi hujjatlar:\n👨💼 Ism: {first_name}\n🆔 Familiyasi: {last_name}\n📞 Telefon raqami: {phone}",
        3: "📌 Новые документы:\n👨💼 Имя: {first_name}\n🆔 Фамилия: {last_name}\n📞 Телефон номер: {phone}"
    },
    "send_to_group_doc": {
        1: "📌 Jańa hújjetler:",
        2: "📌 Yangi hujjatlar:",
        3: "📌 Новые документы:"
    },
    "send_to_group_firstname": {
        1: "\n👨💼 Atı:",
        2: "\n👨💼 Ism:",
        3: "\n👨💼 Имя:"
    },
    "send_to_group_lastname": {
        1: "\n🆔 Familiyası:",
        2: "\n🆔 Familiyasi:",
        3: "\n🆔 Фамилия:"
    },
    "send_to_group_phone": {
        1: "\n📞 Telefon nomeri:",
        2: "\n📞 Telefon raqami:",
        3: "\n📞 Телефон номер:"
    },
    "completed": {
        1: "✅ Hújjetlerińiz tabıslı jiberildi!",
        2: "✅ Hujjatlaringiz muvaffaqiyatli jo‘natildi!",
        3: "✅ Ваши документы успешно отправлены!"
    }

}
