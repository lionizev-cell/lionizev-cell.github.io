# CLAUDE.md — เว็บความลับพลังตัวเลข (www.palangtuaylek.com)

เจ้าของ: ธนวัตน์ จิระเมธาทรัพย์ (เพจความลับพลังตัวเลข) แก้เว็บจากมือถือเป็นหลัก
เว็บนี้คือ "กติกาล่าสุด" ของศาสตร์ที่เจ้าของใช้ คำอ่านเบอร์ หนังสือ คอนเทนต์ และคำตอบลูกค้าทุกที่ต้องยึดตามผลของเว็บนี้

## โครงสร้าง repo
- โฮสต์บน GitHub Pages โดเมน www.palangtuaylek.com (ไฟล์ CNAME) ไม่มีขั้นตอน build ทุกหน้าเป็น HTML ไฟล์เดียวจบ
- `palangtuaylek.html` แอปหลัก: วิเคราะห์เบอร์ ชื่อ ทะเบียนรถ บ้านเลขที่ ฯลฯ ผูกดวง ระบบจ่ายเงิน แผงแอดมิน (ไฟล์ใหญ่ ~1.7MB อย่าอ่านทั้งไฟล์ ให้ grep หาฟังก์ชันที่ต้องการ)
- `index.html` หน้าแรก, `duang.html` เว็บดูดวง (ต้องสีและผลไม่ขัดกับแอปหลัก), `ebook.html` หน้าอีบุ๊ก, `suadmon.html` หนังสือสวดมนต์
- บทความ: `bt-*.html` (21 บท), `lek-00..99.html` ความหมายคู่เลข, `fan-*.html` ทำนายฝัน, `sv-*.html` หน้าบริการ, `duang-2570-*.html`, `chong-2570.html`, `fs-2570.html`
- ข้อมูล: `stock.json` เบอร์ที่ลงขาย, `smpimg.json` `rvimg.json` รูปตัวอย่าง/รีวิว (base64), `sitemap.xml`, `manifest.json` + `.well-known/assetlinks.json` สำหรับแอป Android
- `index-1-3-1.html` `old-link.html` เป็นของเก่า ห้ามใช้เป็นแหล่งอ้างอิง

## จุดสำคัญใน palangtuaylek.html
- `const CONFIG={...}` ค่าตั้งเว็บ
  - `codeSalt` ห้ามเปลี่ยน รหัสปลดล็อกของลูกค้าทุกคนจะใช้ไม่ได้
  - `adminHash` `slipApi` ห้ามแตะ เว้นแต่เจ้าของสั่ง
  - `chatUrl` ลิงก์ LINE OA ใช้ `https://lin.ee/tnnRdLE` (บัญชี @367xgtjh)
- `const P={` ความหมายคู่เลข [เกรด g/m/b, ชื่อคู่, ความหมาย] | `const GSEX={` กฎตามเพศ | `SUM_OVR` + `sumGen()` ผลรวมเบอร์ | `const POS=[` ตำแหน่ง 012-ABCDEFG และน้ำหนัก
- `LORD` `EXALT` `HOUSE` การผูกดวง สุริยยาตร์แบบ myhora ลัคนาอันโตนาทีสามัญ
- `render()` หน้าผลเบอร์, `topOfferHtml()` ข้อเสนอตามคะแนน, `stickyCtaHtml()` ปุ่มลอยล่างจอ, `deepPreviewHtml()` ตัวอย่างเจาะลึก (คู่แนะนำต้องซ่อนเป็น "?"), `payHtml()` กล่องจ่าย 399
- `cntHit()` / `CNT_KEYS` ตัวนับสถิติที่ abacus.jasoncameron.dev ห้ามเปลี่ยนชื่อ key เดิม (สรุปยอดรายสัปดาห์อ่านจาก key เหล่านี้)
- ถ้าแก้คู่เลข/กฎในตาราง ต้องแก้ `lek-*.html` และ `bt-*.html` ที่พูดถึงเรื่องเดียวกันให้ตรงกันด้วย

## กติกาเนื้อหาที่ลูกค้าเห็น
- เขียนเป็นเสียงอาจารย์ ("ผม") ภาษาคนธรรมดา ตรง มั่นใจ ไม่ใช่ภาษาบทความ AI
- ห้ามใช้คำว่า "ระบบ" กับลูกค้า ให้เป็นการวิเคราะห์ของอาจารย์
- ห้ามประทับป้าย "เบอร์ดี ใช้ได้เลย" หรือ "ใช้ต่อได้เลย" บนเบอร์ปัจจุบันของลูกค้า ใช้ "เข้ากับดวงคุณดี" แทน
- คำเรียกเลขในดวง: "เลขพลังดีที่ควรมีในเบอร์" "เลขพลังปานกลาง" "เลขพลังอ่อนควรร้อยเรียงอย่างระวัง" ห้ามใช้ "เลขที่ควรเลี่ยง"
- ใช้คำว่า เรือน ไม่ใช่ บ้าน ในเรื่องดวง
- ผลรวมเบอร์อ่านเป็นเลข 2 หลัก ไม่ทอน
- ส่วนฟรีบอกจุดเด่นและจุดอ่อน ส่วนจ่ายเงินบอกวิธีแก้ (คู่แนะนำ ตัวอย่างเบอร์) อย่าเผยคู่แนะนำในส่วนฟรี
- Meta ไม่ให้โพสต์ลิงก์เว็บบนเพจ Facebook (ไม่เกี่ยวกับโค้ด แต่อย่าเขียนคอนเทนต์ที่พึ่งลิงก์บนเพจ)

## ทดสอบก่อนส่งไฟล์ทุกครั้ง
GitHub รันการตรวจอัตโนมัติทุก PR และทุกการอัปโหลดเข้า main (`.github/workflows/check-site.yml` เรียก `tests/check_site.py`) ตรวจค่า codeSalt/adminHash/slipApi และผลเบอร์ ทะเบียน ชื่อ เทียบกับเวอร์ชันก่อนหน้า รันเองได้ด้วย `python3 tests/check_site.py <ไฟล์ก่อนแก้> palangtuaylek.html`

แก้ palangtuaylek.html แล้วต้องรันเทียบไฟล์ก่อนแก้ ผลคะแนน คู่เลข ผลรวม พีระมิด ต้องไม่เปลี่ยน ยกเว้นจุดที่ตั้งใจแก้ และต้องไม่มี error ในหน้า

```python
# python3 test_site.py palangtuaylek.html 0892456915  (ใช้ Playwright + Chromium)
import sys; from playwright.sync_api import sync_playwright
html, phone = sys.argv[1], sys.argv[2]; errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":390,"height":844})
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.route("**/*", lambda r: r.continue_() if r.request.url.startswith("file:") else r.abort())
    pg.goto("file://"+__import__("os").path.abspath(html)); pg.wait_for_timeout(700)
    pg.evaluate("()=>{try{localStorage.clear()}catch(e){}}")
    pg.evaluate("m=>setMode(m)","phone"); pg.fill("#phone",phone); pg.fill("#job","ขายของออนไลน์")
    for k,v in [("sex","ชาย"),("dd","12"),("mm","พฤษภาคม"),("yy","2533"),("hh","07"),("mi","43"),("prov","เลย")]:
        pg.select_option("#"+k,label=v)
    pg.click("#gobtn"); pg.wait_for_timeout(3000)
    print(pg.inner_text("#result")); print("ERRORS:", errs); b.close()
```
- ทดสอบอย่างน้อย 2 เบอร์: เบอร์คะแนนสูง (0892456915 ≈ 907) และเบอร์คะแนนกลาง (0812345678 ≈ 600)
- โหมดอื่นใช้ `setMode('plate')` + `#plate`, `setMode('name')` + `#fname` `#lname`
- ทดสอบขนาดจอมือถือ (กว้าง 390px) เพราะลูกค้าเกือบทั้งหมดใช้มือถือ

## การส่งงาน
- เจ้าของอัปเดตเว็บโดยอัปโหลดไฟล์ชื่อเดิมทับบน GitHub ผ่านมือถือ ให้ส่งไฟล์ที่แก้แล้วทั้งไฟล์ พร้อมสรุปสั้น ๆ ว่าเปลี่ยนอะไร
- ถ้ามีสิทธิ์ push: ทำ branch ใหม่ เปิด PR ห้าม push ตรงเข้า main โดยไม่ได้รับอนุญาต
- แก้จากเวอร์ชันล่าสุดใน repo เสมอ (git pull ก่อน) เพราะเจ้าของแก้จากมือถือบ่อย
