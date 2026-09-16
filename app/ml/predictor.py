from pathlib import Path
import json
import joblib
from app.ml.preprocessor import clean_text
MODEL_DIR=Path('models'); DEFAULT_MODEL=MODEL_DIR/'complaint_classifier.pkl'; _model=None; _loaded_path=None

def get_model():
    global _model,_loaded_path
    active=DEFAULT_MODEL
    registry=MODEL_DIR/'active_model.json'
    if registry.exists():
        try:
            name=json.loads(registry.read_text()).get('active_model')
            if name: active=MODEL_DIR/name
        except Exception: pass
    if _model is None or _loaded_path != active:
        if not active.exists(): raise FileNotFoundError('Trained model not found. Run: python app/ml/train_model.py')
        _model=joblib.load(active); _loaded_path=active
    return _model

def predict_category(text:str)->dict:
    cleaned=clean_text(text); model=get_model(); category=model.predict([cleaned])[0]
    result={'category':category,'clean_text':cleaned}
    if hasattr(model,'predict_proba'):
        probs=model.predict_proba([cleaned])[0]; classes=model.named_steps['classifier'].classes_
        result['confidence']=float(max(probs)); result['probabilities']={str(c):float(p) for c,p in zip(classes,probs)}
    else: result['confidence']=None; result['probabilities']=None
    return result
