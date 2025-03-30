@echo off
echo ===== CareerCatalyst Job Finder Tests =====

echo.
echo === Testing Job Scraper ===
python -m app.scripts.test_job_scraper

echo.
echo.
echo === Testing Job Recommender ===
python -m app.scripts.test_job_recommender

echo.
echo ===== All tests completed =====
pause 