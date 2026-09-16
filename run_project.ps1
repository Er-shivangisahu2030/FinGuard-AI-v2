# Run this from the FinGuard-AI project root.
# First install dependencies and configure .env.

python scripts/generate_dataset.py
python scripts/prepare_data.py
python scripts/split_data.py
python app/ml/train_model.py
python app/ml/evaluate_model.py

Write-Host "`nML setup complete."
Write-Host "Start API with: uvicorn app.main:app --reload"
Write-Host "Start customer app with: streamlit run frontend/customer_app.py"
Write-Host "Start team dashboard with: streamlit run frontend/team_dashboard.py"
