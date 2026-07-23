"""
将 Markdown 文件转换为精美排版的 PDF（通过浏览器打印）
支持：中文、Emoji、引用块、删除线、代码块等

使用方法：
  py -3 md2pdf.py          → 生成 HTML 并在浏览器中打开，Ctrl+P 打印为 PDF
  py -3 md2pdf.py --html   → 仅生成 HTML 文件，不打开浏览器
"""

import re
import sys
import io
import webbrowser
import markdown

# 强制 UTF-8 输出，避免 Windows GBK 编码问题
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ============================================================
# 配置
# ============================================================
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
INPUT_MD = os.path.join(PROJECT_DIR, "如何在宿舍优雅地导管🛫.md")
OUTPUT_HTML = os.path.join(PROJECT_DIR, "如何在宿舍优雅地导管🛫.html")

# ============================================================
# 1. 读取 Markdown
# ============================================================
with open(INPUT_MD, "r", encoding="utf-8") as f:
    md_text = f.read()

# 处理 ~~删除线~~（Python markdown 库默认不支持）
md_text = re.sub(r"~~(.+?)~~", r"<del>\1</del>", md_text)

# 关键：保留原始行结构 —— 每行末尾加两个空格 = markdown 硬换行
# 这样原文的 "一句一行" 不会被合并成段落
lines = md_text.split("\n")
processed_lines = []
for line in lines:
    # 空行、标题行、引用行里面的空行保持原样
    stripped = line.rstrip()
    if stripped == "":
        processed_lines.append("")
    else:
        # 行末加两个空格 → markdown 硬换行 <br>
        processed_lines.append(stripped + "  ")
md_text = "\n".join(processed_lines)

# 转换为 HTML（启用常用扩展）
html_body = markdown.markdown(
    md_text,
    extensions=[
        "extra",        # 表格、代码块、脚注等
        "codehilite",   # 代码高亮
        "toc",          # 目录
        "sane_lists",   # 更智能的列表处理
    ],
    extension_configs={
        "codehilite": {
            "css_class": "highlight",
            "guess_lang": False,
        },
    },
    output_format="html5",
)

# ============================================================
# 2. 精美的 HTML 模板 + 打印级 CSS
# ============================================================
HTML_TEMPLATE = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>如何在宿舍优雅地导管🛫</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
  /* ========== 页面设置（浏览器打印时生效） ========== */
  @page {{
    size: A4;
    margin: 2cm 1.5cm 2cm 2cm;
  }}

  /* ========== 基础排版 ========== */
  :root {{
    --text-color: #2c2c2c;
    --heading-color: #1a1a1a;
    --border-color: #e0e0e0;
    --accent: #3a7bd5;
    --bg-quote: #f7f9fc;
    --bg-code: #f4f5f7;
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    max-width: 800px;
    margin: 0 auto;
    padding: 40px 20px;
    font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", "微软雅黑",
                 "Hiragino Sans GB", "WenQuanYi Micro Hei",
                 "Helvetica Neue", Arial, sans-serif;
    font-size: 15px;
    line-height: 1.9;
    color: var(--text-color);
    text-align: left;
  }}

  /* ========== 标题层级 ========== */
  h1 {{
    font-size: 24px;
    font-weight: 700;
    color: var(--heading-color);
    text-align: left;
    margin: 1.5em 0 0.5em 0;
  }}

  h1:first-of-type {{
    margin-top: 1.5em;
    font-size: 30px;
    font-weight: 800;
  }}

  h2 {{
    font-size: 20px;
    font-weight: 700;
    color: var(--heading-color);
    margin: 1.6em 0 0.5em 0;
    padding-left: 12px;
    border-left: 4px solid var(--accent);
  }}

  h3 {{
    font-size: 16px;
    font-weight: 600;
    color: #444;
    margin: 1.3em 0 0.4em 0;
  }}

  /* ========== 段落 ========== */
  p {{
    margin: 1.2em 0;
  }}

  /* 换行也带一点间距，让分行可见 */
  br {{
    display: block;
    margin: 0.2em 0;
  }}

  /* ========== 强调与装饰 ========== */
  strong {{
    font-weight: 700;
    color: #1a1a1a;
  }}

  del {{
    color: #999;
    text-decoration: line-through;
  }}

  em {{
    font-style: italic;
    color: #555;
  }}

  /* ========== 引用块（重点美化） ========== */
  blockquote {{
    margin: 1.2em 0;
    padding: 1em 1.4em;
    background: var(--bg-quote);
    border-left: 4px solid var(--accent);
    border-radius: 0 8px 8px 0;
    font-size: 14px;
    color: #555;
  }}

  blockquote blockquote {{
    background: #eef2f7;
    border-left-color: #6c9bd2;
    margin: 0.5em 0;
  }}

  blockquote p {{
    margin: 1em 0;
  }}

  /* 引用块内第一个和最后一个段落不额外撑开 */
  blockquote p:first-child {{
    margin-top: 0;
  }}

  blockquote p:last-child {{
    margin-bottom: 0;
  }}

  /* ========== 列表 ========== */
  ul, ol {{
    margin: 0.6em 0;
    padding-left: 2.2em;
  }}

  li {{
    margin: 0.25em 0;
  }}

  /* ========== 行内代码 ========== */
  code {{
    font-family: "Cascadia Code", "Fira Code", "JetBrains Mono",
                 "Consolas", "Courier New", monospace;
    font-size: 0.88em;
    background: var(--bg-code);
    padding: 2px 7px;
    border-radius: 4px;
    color: #c7254e;
  }}

  /* ========== 代码块（暗色主题） ========== */
  pre {{
    font-family: "Cascadia Code", "Fira Code", "JetBrains Mono",
                 "Consolas", "Courier New", monospace;
    font-size: 13px;
    line-height: 1.55;
    background: #282c34;
    color: #abb2bf;
    padding: 1.2em 1.4em;
    border-radius: 8px;
    overflow-x: auto;
    white-space: pre-wrap;
    word-break: break-all;
    margin: 1em 0;
  }}

  pre code {{
    background: none;
    color: inherit;
    padding: 0;
    border-radius: 0;
    font-size: inherit;
  }}

  /* ========== 水平分割线 ========== */
  hr {{
    border: none;
    border-top: 1px dashed var(--border-color);
    margin: 2em 0;
  }}

  /* ========== 表格 ========== */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 13px;
  }}

  th, td {{
    border: 1px solid var(--border-color);
    padding: 8px 14px;
    text-align: left;
  }}

  th {{
    background: var(--bg-code);
    font-weight: 600;
  }}

  /* ========== 图片 ========== */
  img {{
    max-width: 100%;
    height: auto;
    border-radius: 4px;
  }}

  /* ========== 链接 ========== */
  a {{
    color: var(--accent);
    text-decoration: none;
  }}

  /* ==================== 打印样式 ==================== */
  @media print {{
    body {{
      max-width: none;
      margin: 0;
      padding: 0;
      font-size: 11pt;
      print-color-adjust: exact;
      -webkit-print-color-adjust: exact;
    }}

    h1 {{
      font-size: 21pt;
    }}

    h1:first-of-type {{
      font-size: 26pt;
      font-weight: 800;
    }}

    h2 {{
      font-size: 17pt;
      page-break-after: avoid;
    }}

    h3 {{
      font-size: 13pt;
      page-break-after: avoid;
    }}

    blockquote {{
      font-size: 11pt;
      page-break-inside: avoid;
    }}

    pre {{
      font-size: 9.5pt;
      page-break-inside: avoid;
      white-space: pre-wrap;
    }}

    table {{
      page-break-inside: avoid;
    }}

    p {{
      orphans: 3;
      widows: 3;
    }}

    code {{
      font-size: 0.9em;
    }}
  }}

  /* ==================== 屏幕预览提示条 ==================== */
  .print-hint {{
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: linear-gradient(135deg, #3a7bd5, #6c5ce7);
    color: #fff;
    text-align: center;
    padding: 10px 20px;
    font-size: 14px;
    z-index: 9999;
    box-shadow: 0 2px 12px rgba(0,0,0,0.15);
  }}

  .print-hint kbd {{
    background: rgba(255,255,255,0.2);
    padding: 2px 8px;
    border-radius: 4px;
    font-family: inherit;
    border: 1px solid rgba(255,255,255,0.3);
    margin: 0 3px;
  }}

  .print-hint strong {{
    color: #fff;
  }}

  @media screen {{
    .print-hint {{
      display: block;
    }}
    body {{
      padding-top: 50px;
    }}
  }}
</style>
</head>
<body>

<div class="print-hint">
  🖨️  <strong>打印为 PDF：</strong>按 <kbd>Ctrl+P</kbd> → 目标另存为 PDF →
  边距选<strong>"无"</strong> → 勾选<strong>"背景图形"</strong> → 保存
</div>

{html_body}

</body>
</html>"""

# ============================================================
# 3. 输出 HTML 文件
# ============================================================
with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(HTML_TEMPLATE)

print(f"[OK] HTML generated: '{OUTPUT_HTML}'")
print()

# ============================================================
# 4. 在浏览器中打开（除非指定 --html）
# ============================================================
if "--html" not in sys.argv:
    webbrowser.open(OUTPUT_HTML)
    print("[>>] Opened in browser for preview")
    print()
    print("+--------------------------------------------------+")
    print("|  PRINT TO PDF STEPS:                             |")
    print("|                                                  |")
    print("|  1. Press Ctrl+P to open Print dialog            |")
    print("|  2. Destination: 'Save as PDF'                   |")
    print("|  3. Layout: Portrait                             |")
    print("|  4. Paper size: A4                               |")
    print("|  5. Margins: 'None'                              |")
    print("|  6. [v] Check 'Background graphics'              |")
    print("|  7. Click 'Save'                                 |")
    print("|                                                  |")
    print("|  TIP: Edge/Chrome gives the best result          |")
    print("+--------------------------------------------------+")
else:
    print("[>>] Open the HTML file in browser, then Ctrl+P to print as PDF")
