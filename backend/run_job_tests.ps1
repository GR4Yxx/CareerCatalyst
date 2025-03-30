Write-Host "===== CareerCatalyst Job Finder Tests =====" -ForegroundColor Cyan

Write-Host ""
Write-Host "=== Testing Job Scraper ===" -ForegroundColor Yellow
python -m app.scripts.test_job_scraper

Write-Host ""
Write-Host ""
Write-Host "=== Testing Job Recommender ===" -ForegroundColor Yellow
python -m app.scripts.test_job_recommender

Write-Host ""
Write-Host "===== All tests completed =====" -ForegroundColor Cyan
Write-Host "Press any key to continue..."
$host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") | Out-Null 