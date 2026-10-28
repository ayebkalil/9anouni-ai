import re

REPEAL_PATTERN = re.compile(
    r"تلغى\s+(?:أحكام\s+)?الفصل\s+(\d+(?:\s+مكرر|\s+ثالثا)?)\s+من\s+(.+?)(?:\s+لسنة\s+(\d{4}))?(?=\s*$|\.)"
)

text1 = "تلغى أحكام الفصل 14 من قانون المالية لسنة 2020."
text2 = "تلغى أحكام الفصل 14 مكرر من مجلة الأداء على القيمة المضافة."

with open("scratch_output.txt", "w", encoding="utf-8") as f:
    f.write("Test 1:\n")
    m1 = REPEAL_PATTERN.search(text1)
    if m1:
        f.write(str(m1.groups()) + "\n")
    else:
        f.write("No match 1\n")

    f.write("Test 2:\n")
    m2 = REPEAL_PATTERN.search(text2)
    if m2:
        f.write(str(m2.groups()) + "\n")
    else:
        f.write("No match 2\n")
