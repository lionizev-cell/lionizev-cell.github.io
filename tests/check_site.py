"""ตรวจเว็บความลับพลังตัวเลขก่อนขึ้นจริง

ใช้: python3 tests/check_site.py <ไฟล์เวอร์ชันก่อนแก้> <ไฟล์เวอร์ชันใหม่>
(ทั้งสองเป็น palangtuaylek.html)

สิ่งที่ตรวจ
1. ค่าสำคัญใน CONFIG (codeSalt adminHash slipApi) ต้องไม่เปลี่ยน ถ้าเปลี่ยน = ไม่ผ่าน
2. หน้าวิเคราะห์เบอร์ ทะเบียนรถ และชื่อ ต้องเปิดได้ ออกผล และไม่มี error = ไม่ผ่านถ้าพัง
3. คะแนน ผลรวม และคู่เลข เทียบกับเวอร์ชันก่อนแก้ ถ้าเปลี่ยนจะแจ้งเตือน (ไม่ถือว่าพัง
   เพราะบางครั้งเจ้าของตั้งใจเปลี่ยนกฎ) ให้ดูว่าตั้งใจหรือไม่
ผลสรุปเขียนลงไฟล์ตาม GITHUB_STEP_SUMMARY ถ้ามี
"""
import os
import re
import sys

from playwright.sync_api import sync_playwright

BIRTH = [("sex", "ชาย"), ("dd", "12"), ("mm", "พฤษภาคม"), ("yy", "2533"),
         ("hh", "07"), ("mi", "43"), ("prov", "เลย")]
CASES = [
    ("phone", {"#phone": "0892456915"}, "เบอร์ 089-245-6915"),
    ("phone", {"#phone": "0812345678"}, "เบอร์ 081-234-5678"),
    ("plate", {"#plate": "1กข 2345"}, "ทะเบียน 1กข 2345"),
    ("name", {"#fname": "ธนวัตน์", "#lname": "จิระเมธาทรัพย์"}, "ชื่อ ธนวัตน์ จิระเมธาทรัพย์"),
]
SECRETS = ["codeSalt", "adminHash", "slipApi"]
# ของที่ต้องมีอยู่ในไฟล์เสมอ และคำที่ห้ามขึ้นกับลูกค้า (ถ้าเจอ = มีคนอัปไฟล์ชุดเก่าทับ)
MUST_HAVE = {"function funnelHooks": "ตัวนับขั้นการขาย funnelHooks หายไป", "lin.ee/TJ05Mnd": "ลิงก์ LINE ใหม่ TJ05Mnd หายไป"}
MUST_NOT = {"เข้ากับดวง ใช้ต่อได้เลย": "หน้าผลเบอร์กลับมาใช้คำว่า ใช้ต่อได้เลย กับเบอร์ของลูกค้า",
            "good:\"ใช้ต่อได้เลย\"": "คำแนะนำเบอร์ดีกลับมาใช้คำว่า ใช้ต่อได้เลย",
            "ระบบทำผลสรุป": "กล่องบันทึกรูปกลับมาใช้คำว่า ระบบ",
            "lin.ee/ujF7VHa": "มีลิงก์ LINE เก่า ujF7VHa", "lin.ee/tnnRdLE": "มีลิงก์ LINE เก่า tnnRdLE"}


def config_values(path):
    html = open(path, encoding="utf-8").read()
    out = {}
    for key in SECRETS:
        m = re.search(key + r'\s*:\s*"([^"]*)"', html)
        out[key] = m.group(1) if m else None
    return out


def run_case(page, path, mode, fields):
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto("file://" + os.path.abspath(path), wait_until="domcontentloaded")
    page.wait_for_timeout(800)
    page.evaluate("()=>{try{localStorage.clear()}catch(e){}}")
    page.evaluate("m=>setMode(m)", mode)
    for sel, val in fields.items():
        page.fill(sel, val)
    page.fill("#job", "ขายของออนไลน์")
    for key, val in BIRTH:
        page.select_option("#" + key, label=val)
    page.click("#gobtn")
    page.wait_for_timeout(3000)
    text = page.inner_text("#result")
    core = {
        "score": re.findall(r"(\d{3,4})\s*/\s*1000", text)[:1],
        "sum": re.findall(r"ผลรวม\s*(\d{1,3})", text)[:1],
        "pairs": re.findall(r"\n(\d{2})\n", text)[:20],
    }
    return text, core, errors


def analyse(path):
    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for mode, fields, label in CASES:
            page = browser.new_page(viewport={"width": 390, "height": 844})
            page.route("**/*", lambda r: r.continue_() if r.request.url.startswith("file:") else r.abort())
            try:
                results[label] = run_case(page, path, mode, fields)
            except Exception as exc:  # หน้าพังจนกรอกไม่ได้
                results[label] = ("", {}, ["เปิดหน้าไม่ได้: " + str(exc)[:200]])
            page.close()
        browser.close()
    return results


def main():
    old_path, new_path = sys.argv[1], sys.argv[2]
    fails, warns, oks = [], [], []

    old_cfg, new_cfg = config_values(old_path), config_values(new_path)
    for key in SECRETS:
        if old_cfg[key] != new_cfg[key]:
            fails.append(f"ค่า `{key}` ใน CONFIG ถูกเปลี่ยน ถ้าไม่ได้ตั้งใจ ให้แก้กลับเป็นค่าเดิม"
                         + (" (รหัสปลดล็อกของลูกค้าทุกคนจะใช้ไม่ได้)" if key == "codeSalt" else ""))
    if not fails:
        oks.append("ค่าสำคัญใน CONFIG ไม่ถูกแตะ")
    new_html = open(new_path, encoding="utf-8").read()
    guard = [msg for key, msg in MUST_HAVE.items() if key not in new_html]
    guard += [msg for key, msg in MUST_NOT.items() if key in new_html]
    for msg in guard:
        fails.append(msg + " (น่าจะอัปไฟล์ชุดเก่าทับ ให้ดึงไฟล์ล่าสุดจาก GitHub แล้วแก้ใหม่)")
    if not guard:
        oks.append("ตัวนับขั้นการขาย ลิงก์ LINE และคำที่ลูกค้าเห็น ถูกต้อง")

    old_res, new_res = analyse(old_path), analyse(new_path)
    for _, _, label in CASES:
        text, core, errors = new_res[label]
        if errors:
            fails.append(f"{label}: หน้าเว็บมีข้อผิดพลาด {errors[0][:150]}")
            continue
        if len(text.strip()) < 200:
            fails.append(f"{label}: กดวิเคราะห์แล้วไม่มีผลออกมา")
            continue
        old_core = old_res[label][1]
        if old_core and old_core != core:
            changed = [k for k in core if core.get(k) != old_core.get(k)]
            warns.append(f"{label}: ผลเปลี่ยนจากเดิมในส่วน {', '.join(changed)} "
                         f"(เดิม {old_core.get('score')}/{old_core.get('sum')} ใหม่ {core.get('score')}/{core.get('sum')}) "
                         "ถ้าไม่ได้ตั้งใจเปลี่ยนกฎ ให้ตรวจก่อน Merge")
        else:
            oks.append(f"{label}: ออกผลปกติ ผลเหมือนเดิม")

    lines = ["## ผลตรวจเว็บ palangtuaylek", ""]
    lines += ["### ❌ ต้องแก้ก่อน Merge"] + [f"- {x}" for x in fails] + [""] if fails else []
    lines += ["### ⚠️ ผลเปลี่ยน ตรวจว่าตั้งใจหรือไม่"] + [f"- {x}" for x in warns] + [""] if warns else []
    lines += ["### ✅ ผ่าน"] + [f"- {x}" for x in oks]
    report = "\n".join(lines)
    print(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(report + "\n")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
