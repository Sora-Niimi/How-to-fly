# 一键 MD → PDF（利用 Edge 无头模式）
# 依赖：先运行 py -3 md2pdf.py --html 生成 HTML

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir
$HtmlFile = Join-Path $ProjectDir "如何在宿舍优雅地导管🛫.html"
$PdfFile  = Join-Path $ProjectDir "如何在宿舍优雅地导管🛫.pdf"

Write-Host "[*] Converting HTML to PDF via Edge headless mode..."

# 查找 Edge 路径
$edgePaths = @(
    "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
)
$edge = $null
foreach ($p in $edgePaths) {
    if (Test-Path $p) { $edge = $p; break }
}

if (-not $edge) {
    Write-Host "[!] Edge not found. Using Chrome fallback..."
    $chromePaths = @(
        "C:\Program Files\Google\Chrome\Application\chrome.exe",
        "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    )
    foreach ($p in $chromePaths) {
        if (Test-Path $p) { $edge = $p; break }
    }
}

if (-not $edge) {
    Write-Host "[!] No Chrome/Edge found. Please open the HTML file manually and Ctrl+P -> Save as PDF."
    exit 1
}

$absPath = (Get-Item $HtmlFile).FullName
$fileUrl = "file:///" + ($absPath -replace '\\', '/')

$args = @(
    "--headless",
    "--disable-gpu",
    "--print-to-pdf=`"$PdfFile`"",
    "--no-pdf-header-footer",
    $fileUrl
)

Write-Host "[*] Running: $edge"
& $edge @args 2>$null

if (Test-Path $PdfFile) {
    Write-Host "[OK] PDF generated: '$PdfFile'"
    Write-Host ""
    Write-Host "NOTE: This is a basic conversion. For the best result with"
    Write-Host "styled backgrounds, quotes, and fonts, use the browser print"
    Write-Host "method: open the HTML file and press Ctrl+P."
} else {
    Write-Host "[!] PDF generation failed. Fall back to browser print method."
}
