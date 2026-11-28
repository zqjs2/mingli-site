Set-Location G:\mingli-site
Write-Host "Step 1/2  building site ..." -ForegroundColor Cyan
python -m mkdocs build --clean
if ($LASTEXITCODE -ne 0) { Write-Host "build failed, stopped." -ForegroundColor Red; exit 1 }
Write-Host "Step 2/2  deploying to Cloudflare Pages ..." -ForegroundColor Cyan
$env:CLOUDFLARE_API_TOKEN = (Get-Content G:\mingli-site\.cf-token -Raw).Trim()
$env:HTTPS_PROXY = "http://127.0.0.1:10808"
$env:HTTP_PROXY  = "http://127.0.0.1:10808"
& G:\cf\wrangler.cmd pages deploy site --project-name zqjs --branch main
Write-Host "Done. https://zqjs.ziqing.ccwu.cc" -ForegroundColor Green
