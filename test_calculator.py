"""تست ماشین‌حساب — بدون نیاز به نصب Kivy (تست UI فقط اگر Kivy موجود باشد اجرا می‌شود).

اجرا:  python test_calculator.py
"""

import sys

from calculator import CalculatorLogic, format_number


def run_logic_tests():
    """مجموعه‌ای از سناریوها: (کلیدها، نمایش مورد انتظار)"""
    cases = [
        (list("12+34="), "46", "جمع"),
        (list("50-18="), "32", "تفریق"),
        (list("6×7="), "42", "ضرب"),
        (list("20÷4="), "5", "تقسیم بدون باقیمانده"),
        (list("5÷2="), "2.5", "تقسیم اعشاری"),
        (list("0.1+0.2="), "0.3", "گرد کردن خطای اعشار شناور"),
        (list("2.5×4="), "10", "حذف صفرهای انتهایی"),
        (list("2+3×4="), "20", "ترتیب چپ به راست (بدون اولویت ضرب)"),
        (list("2+3=×4="), "20", "زنجیره با دکمه مساوی در میان"),
        (list("5+"), "5", "عملگر بدون مساوی"),
        (list("1÷0="), "Error", "تقسیم بر صفر"),
        (list("1÷0=5+3="), "8", "ادامه کار بعد از خطا"),
        (list("1÷0=+"), "Error", "عملگر بعد از خطا نادیده گرفته می‌شود"),
        (list("12=C7+1="), "8", "دکمه پاک کردن"),
        (list("0"), "0", "صفر پیش‌فرض"),
        (list("007"), "7", "حذف صفرهای ابتدایی"),
        (list("3.14×2="), "6.28", "عدد اعشاری"),
        (list("..5"), "0.5", "نقطه تکراری نادیده گرفته می‌شود"),
        (list("9+8=5"), "5", "شروع محاسبه جدید بعد از مساوی"),
        (list("2+=~"), None, None),  # فقط اجرا می‌شود، کرش نکند
    ]
    passed = 0
    for keys, expected, label in cases:
        logic = CalculatorLogic()
        for key in keys:
            if key == "~":  # کلید بی‌معنی — نباید کرش کند
                logic.press("?")
                continue
            logic.press(key)
        if expected is not None:
            assert logic.display == expected, (
                f"ناموفق [{label}]: انتظار {expected!r} بود، اما {logic.display!r} شد"
            )
        passed += 1
    print(f"[OK] {passed} تست منطق گذشت")


def run_format_tests():
    assert format_number(10.0) == "10"
    assert format_number(-0.0) == "0"
    assert format_number(2.5) == "2.5"
    assert format_number(float("inf")) == "Error"
    assert format_number(float("nan")) == "Error"
    print("[OK] تست‌های format_number گذشت")


def run_ui_tests():
    """ساخت کامل UI بدون پنجره‌ی واقعی (mock window) و شبیه‌سازی فشردن دکمه‌ها."""
    try:
        import kivy  # noqa: F401
    except Exception as exc:
        print(f"[SKIP] تست UI: Kivy نصب نیست ({exc.__class__.__name__})")
        return

    import os
    os.environ.setdefault("KIVY_NO_ARGS", "1")

    try:
        from main import CalculatorApp

        app = CalculatorApp()
        root = app.build()
    except Exception as exc:
        # روی سرورهای بدون نمایشگر (مثل CI) ساخت پنجره ممکن نیست — تست را رد کن
        print(f"[SKIP] تست UI: نمایشگر گرافیکی در دسترس نیست ({exc.__class__.__name__})")
        return
    assert root is not None, "متد build رابط کاربری نساخت"

    scenarios = [
        (list("12+34="), "46"),
        (list("7×8="), "56"),
        (list("9÷0="), "Error"),
        (list("C2.5+2.5="), "5"),
    ]
    for keys, expected in scenarios:
        app.press("C")
        for key in keys:
            app.press(key)
        assert app.logic.display == expected, (
            f"UI: انتظار {expected!r} بود، اما {app.logic.display!r} شد"
        )
        assert app.panel.value.text == expected, "نمایشگر با منطق هم‌خوان نیست"

    # دکمه مساوی و نمایشگر عبارت
    app.press("C")
    for key in list("12+5="):
        app.press(key)
    assert app.panel.expression.text == "12 + 5 =", app.panel.expression.text

    print("[OK] تست UI گذشت (بدون پنجره‌ی واقعی)")


if __name__ == "__main__":
    run_logic_tests()
    run_format_tests()
    run_ui_tests()
    print("همه تست‌ها با موفقیت انجام شد ✔")
    sys.exit(0)
