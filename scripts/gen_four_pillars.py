#!/usr/bin/env python3
"""Generate the four-pillars, 4x/day variant.

Social pillar = the 21 real Month of Connection challenges (traceable to
Dr. Dania's library). Physical / Financial / Mental pillars are drafted here in
EN + AR to complete the four-nudges-per-day model:
  Social 07:00 -> Physical 09:15 -> Financial 11:30 -> Mental 13:45 (UAE).

Outputs (one row per SEND = 21 days x 4 pillars = 84 rows):
  data/four-pillars/by-nudge.json / .csv
And a day-pivoted view (21 rows) for the optional single-combined-card format:
  data/four-pillars/by-day.json
"""
import json, csv, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "month-of-connection.json")
OUTDIR = os.path.join(ROOT, "data", "four-pillars")
os.makedirs(OUTDIR, exist_ok=True)

PILLARS = [
    {"key": "Social",    "en": "Social Wellbeing",    "ar": "الرفاه الاجتماعي", "emoji": "🤝", "slot": "07:00", "order": 1},
    {"key": "Physical",  "en": "Physical Wellbeing",  "ar": "الرفاه البدني",   "emoji": "🏃", "slot": "09:15", "order": 2},
    {"key": "Financial", "en": "Financial Wellbeing", "ar": "الرفاه المالي",   "emoji": "💡", "slot": "11:30", "order": 3},
    {"key": "Mental",    "en": "Mental Wellbeing",    "ar": "الرفاه النفسي",   "emoji": "🧠", "slot": "13:45", "order": 4},
]

# Physical / Financial / Mental drafts, 21 days each (EN, AR). Workplace/hospital
# appropriate; financial stays educational/awareness (no individualized advice).
PHYSICAL = [
    ("Stand and stretch for one minute before your next task.", "قِف وتمدّد لمدة دقيقة قبل مهمتك التالية."),
    ("Take the stairs or a short walk between tasks.", "اصعد الدرج أو امشِ قليلاً بين المهام."),
    ("Roll your shoulders back slowly five times.", "أدِر كتفيك للخلف ببطء خمس مرات."),
    ("Drink a glass of water now.", "اشرب كوب ماء الآن."),
    ("Rest your eyes: look far away for twenty seconds.", "أرِح عينيك: انظر إلى مكان بعيد لمدة عشرين ثانية."),
    ("Straighten your posture and unclench your jaw.", "اعتدل في جلستك وأرخِ فكّك."),
    ("Take a two-minute walk to reset your energy.", "امشِ دقيقتين لتجديد طاقتك."),
    ("Loosen your neck with gentle side-to-side stretches.", "أرخِ رقبتك بتمدد لطيف يميناً ويساراً."),
    ("Refill your water bottle and keep it close.", "أعد ملء زجاجة الماء واجعلها قريبة منك."),
    ("Stand up during your next phone call or reading.", "قِف أثناء مكالمتك أو قراءتك القادمة."),
    ("Take three slow, deep breaths to steady your body.", "خذ ثلاثة أنفاس عميقة بطيئة لتهدئة جسمك."),
    ("Stretch your wrists and hands between tasks.", "مدّد معصميك ويديك بين المهام."),
    ("Take a short movement break away from your screen.", "خذ استراحة حركة قصيرة بعيداً عن الشاشة."),
    ("Choose a healthy snack or fruit today.", "اختر وجبة خفيفة صحية أو فاكهة اليوم."),
    ("Walk while you talk when you can.", "امشِ أثناء حديثك عندما يمكنك ذلك."),
    ("Give your eyes a screen break for one minute.", "امنح عينيك استراحة من الشاشة لمدة دقيقة."),
    ("Stretch your back gently by reaching forward.", "مدّد ظهرك بلطف بالانحناء إلى الأمام."),
    ("Drink water before you feel thirsty in the heat.", "اشرب الماء قبل أن تشعر بالعطش في الحر."),
    ("Take a mindful pause to stand and breathe.", "خذ وقفة واعية لتقف وتتنفس."),
    ("Add one extra short walk to your day.", "أضف نزهة قصيرة إضافية إلى يومك."),
    ("Choose one movement habit to keep in September.", "اختر عادة حركة واحدة لتستمر عليها في سبتمبر."),
]

FINANCIAL = [
    ("Note one small expense you can plan for this week.", "دوّن مصروفاً بسيطاً يمكنك التخطيط له هذا الأسبوع."),
    ("Check one subscription you no longer use.", "راجع اشتراكاً واحداً لم تعد تستخدمه."),
    ("Set aside a small amount toward a simple goal.", "خصّص مبلغاً صغيراً لهدف بسيط."),
    ("Compare prices before one purchase today.", "قارن الأسعار قبل عملية شراء واحدة اليوم."),
    ("Write down one financial goal for the month.", "اكتب هدفاً مالياً واحداً لهذا الشهر."),
    ("Try a no-spend moment: pause one small buy.", "جرّب لحظة بلا إنفاق: أجّل عملية شراء صغيرة."),
    ("Review one bill for anything unexpected.", "راجع فاتورة واحدة بحثاً عن أي مبلغ غير متوقع."),
    ("Plan tomorrow's spending before it happens.", "خطّط لمصروف الغد قبل حدوثه."),
    ("Learn one new thing about budgeting today.", "تعلّم شيئاً جديداً عن إدارة الميزانية اليوم."),
    ("Separate a want from a need before buying.", "ميّز بين الرغبة والحاجة قبل الشراء."),
    ("Track today's small spends for awareness.", "تتبّع مصروفاتك الصغيرة اليوم لزيادة الوعي."),
    ("Set a simple reminder for an upcoming payment.", "اضبط تذكيراً بسيطاً لدفعة قادمة."),
    ("Consider a smart swap that saves a little.", "فكّر في بديل ذكي يوفّر القليل."),
    ("Read one saving tip from a trusted source.", "اقرأ نصيحة واحدة عن الادخار من مصدر موثوق."),
    ("Reflect on one money habit that helps you.", "تأمّل عادة مالية واحدة تفيدك."),
    ("Plan a low-cost way to enjoy your week.", "خطّط لطريقة ممتعة وقليلة التكلفة لأسبوعك."),
    ("Check progress toward one savings goal.", "تحقّق من تقدّمك نحو هدف ادخار واحد."),
    ("Avoid one impulse purchase today.", "تجنّب عملية شراء اندفاعية واحدة اليوم."),
    ("Notice one thing you're glad you didn't overspend on.", "دوّن أمراً تشعر بالامتنان لأنك لم تُفرط في الإنفاق عليه."),
    ("Review the week's spending calmly, without judgment.", "راجع مصروفات الأسبوع بهدوء ودون إصدار أحكام."),
    ("Choose one money habit to keep in September.", "اختر عادة مالية واحدة لتستمر عليها في سبتمبر."),
]

MENTAL = [
    ("Take three slow breaths before you start.", "خذ ثلاثة أنفاس بطيئة قبل أن تبدأ."),
    ("Set one clear intention for your day.", "حدّد نيّة واضحة واحدة ليومك."),
    ("Pause for thirty seconds between tasks.", "توقّف ثلاثين ثانية بين المهام."),
    ("Name one thing you're grateful for now.", "اذكر أمراً واحداً تشعر بالامتنان له الآن."),
    ("Give one task your full attention.", "امنح مهمة واحدة كامل انتباهك."),
    ("Notice a tense muscle and let it soften.", "لاحظ عضلة متوترة ودعها تسترخي."),
    ("Take a mindful break away from screens.", "خذ استراحة واعية بعيداً عن الشاشات."),
    ("Speak to yourself as kindly as to a friend.", "تحدّث إلى نفسك بلطف كما تخاطب صديقاً."),
    ("Write down what's on your mind to clear it.", "اكتب ما يشغل بالك لتصفّي ذهنك."),
    ("Let one small task be good enough today.", "دع مهمة صغيرة تكون جيدة بما يكفي اليوم."),
    ("Focus on what's within your control right now.", "ركّز على ما هو ضمن سيطرتك الآن."),
    ("Take a breath before replying to that message.", "خذ نفَساً قبل الرد على تلك الرسالة."),
    ("Step to a window for a short mental reset.", "اتّجه إلى نافذة لإعادة ضبط ذهنك قليلاً."),
    ("Acknowledge one thing you did well today.", "اعترف بأمر واحد أتقنته اليوم."),
    ("Protect a few minutes of quiet focus.", "احمِ بضع دقائق من التركيز الهادئ."),
    ("Notice your feelings without judging them.", "لاحظ مشاعرك دون أن تُصدر عليها أحكاماً."),
    ("Let go of one worry you cannot control.", "تخلَّ عن قلق واحد لا يمكنك التحكم فيه."),
    ("Finish one task fully before starting another.", "أنهِ مهمة واحدة تماماً قبل بدء أخرى."),
    ("Give yourself permission to pause and rest.", "اسمح لنفسك بالتوقف والراحة."),
    ("Reflect on one moment that went well this week.", "تأمّل لحظة واحدة سارت على ما يُرام هذا الأسبوع."),
    ("Choose one calm habit to keep in September.", "اختر عادة هدوء واحدة لتستمر عليها في سبتمبر."),
]

DRAFTS = {"Physical": PHYSICAL, "Financial": FINANCIAL, "Mental": MENTAL}


def theme_split(text):
    """Take the action title before ' - ' as the daily theme label."""
    return text.split(" - ", 1)[0].strip() if " - " in text else text.strip()


def main():
    social = json.load(open(SRC, encoding="utf-8"))
    assert len(social) == 21
    for lst in DRAFTS.values():
        assert len(lst) == 21

    by_nudge = []
    by_day = []
    for idx, day in enumerate(social):
        theme_en = theme_split(day["ChallengeEN"])
        theme_ar = theme_split(day["ChallengeAR"])
        day_row = {
            "Day": day["Day"], "RevealDate": day["RevealDate"],
            "DateLabel": day["DateLabel"], "Weekday": day["Weekday"],
            "WeekArc": day["WeekArc"], "DailyThemeEN": theme_en,
            "DailyThemeAR": theme_ar, "WhyItMatters": day["WhyItMatters"],
            "TomorrowTeaser": day["TomorrowTeaser"], "SocialCaption": day["SocialCaption"],
            "pillars": {},
        }
        for p in PILLARS:
            if p["key"] == "Social":
                en, ar = day["ChallengeEN"], day["ChallengeAR"]
                src = day["SourceRef"]
            else:
                en, ar = DRAFTS[p["key"]][idx]
                src = "draft"
            rec = {
                "Day": day["Day"], "RevealDate": day["RevealDate"],
                "DateLabel": day["DateLabel"], "Weekday": day["Weekday"],
                "WeekArc": day["WeekArc"],
                "DailyThemeEN": theme_en, "DailyThemeAR": theme_ar,
                "Pillar": p["key"], "PillarEN": p["en"], "PillarAR": p["ar"],
                "PillarEmoji": p["emoji"], "PillarOrder": p["order"], "SlotTime": p["slot"],
                "NudgeEN": en, "NudgeAR": ar, "SourceRef": src,
                "Status": "Scheduled", "SentDateTime": "", "RunID": "",
            }
            by_nudge.append(rec)
            day_row["pillars"][p["key"]] = {"en": en, "ar": ar, "slot": p["slot"], "source": src}
        by_day.append(day_row)

    assert len(by_nudge) == 84, len(by_nudge)

    cols = ["Day","RevealDate","DateLabel","Weekday","WeekArc","DailyThemeEN",
            "DailyThemeAR","Pillar","PillarEN","PillarAR","PillarEmoji",
            "PillarOrder","SlotTime","NudgeEN","NudgeAR","SourceRef",
            "Status","SentDateTime","RunID"]
    with open(os.path.join(OUTDIR, "by-nudge.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in by_nudge:
            w.writerow(r)
    with open(os.path.join(OUTDIR, "by-nudge.json"), "w", encoding="utf-8") as f:
        json.dump(by_nudge, f, ensure_ascii=False, indent=2)
    with open(os.path.join(OUTDIR, "by-day.json"), "w", encoding="utf-8") as f:
        json.dump(by_day, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(by_nudge)} sends (by-nudge) and {len(by_day)} days (by-day).")
    print("Slots:", ", ".join(f"{p['en']} {p['slot']}" for p in PILLARS))


if __name__ == "__main__":
    main()
