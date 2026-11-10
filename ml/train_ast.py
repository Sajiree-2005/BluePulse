"""RUN ON COLAB (GPU). UNTESTED here: no torch/HF access in the build sandbox. Validate every stage yourself.
!pip install torch==2.15.0 transformers==4.57.6 optimum-onnx==0.1.0 onnx==1.23.2 onnxruntime==1.31.1 soundfile scikit-learn
Data: manifest.csv with columns path,label,site  (labels: blast,vessel,biology,environmental_noise,ambient). Split BY SITE."""
import sys, numpy as np, pandas as pd, soundfile as sf, torch
from transformers import ASTFeatureExtractor, ASTForAudioClassification
LABELS = ["blast", "vessel", "biology", "environmental_noise", "ambient"]; SR = 16000; WIN = 3 * SR
fe = ASTFeatureExtractor.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593")
model = ASTForAudioClassification.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593", num_labels=5, ignore_mismatched_sizes=True)
df = pd.read_csv("manifest.csv"); sites = sorted(df.site.unique()); val_sites = sites[::5]
tr, va = df[~df.site.isin(val_sites)], df[df.site.isin(val_sites)]
def batch(rows):
    xs, ys = [], []
    for r in rows.itertuples():
        x, sr = sf.read(r.path, dtype="float32"); x = x if x.ndim == 1 else x.mean(1); x = x[:WIN] if len(x) >= WIN else np.pad(x, (0, WIN-len(x)))
        xs.append(x); ys.append(LABELS.index(r.label))
    return fe(xs, sampling_rate=SR, return_tensors="pt"), torch.tensor(ys)
dev = "cuda" if torch.cuda.is_available() else "cpu"; model.to(dev); opt = torch.optim.AdamW(model.parameters(), 3e-5)
w = torch.tensor(1 / tr.label.value_counts().reindex(LABELS).fillna(1).values, dtype=torch.float32).to(dev); w = w / w.sum() * 5
for ep in range(5):
    model.train(); tr = tr.sample(frac=1, random_state=ep)
    for i in range(0, len(tr), 8):
        f, y = batch(tr.iloc[i:i+8]); loss = torch.nn.functional.cross_entropy(model(**{k: v.to(dev) for k, v in f.items()}).logits, y.to(dev), weight=w)
        opt.zero_grad(); loss.backward(); opt.step()
    model.save_pretrained(f"/content/drive/MyDrive/bluepulse/ckpt_ep{ep}")      # Drive checkpoint every epoch
    model.eval(); ok = 0
    with torch.no_grad():
        for i in range(0, len(va), 8):
            f, y = batch(va.iloc[i:i+8]); ok += (model(**{k: v.to(dev) for k, v in f.items()}).logits.argmax(-1).cpu() == y).sum().item()
    print("epoch", ep, "val acc", ok/len(va))
# Next: temperature scaling on val logits, then:  optimum-cli export onnx --model <ckpt> onnx_out/
# then onnxruntime.quantization.quantize_dynamic(..., weight_type=QuantType.QInt8); compare logits with PyTorch; test in docker --cpus=0.1 --memory=512m
