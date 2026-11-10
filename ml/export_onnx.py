"""RUN ON COLAB after training. UNTESTED here (no torch). Exports ONNX, quantises to int8, checks parity, writes model_card.json.
!pip install torch==2.15.0 transformers==4.57.6 onnx==1.23.2 onnxruntime==1.31.1 onnxscript
python export_onnx.py --ckpt /content/drive/MyDrive/bluepulse/ckpt_ep4 --out onnx_out
NOTE: ASTFeatureExtractor pads to 1024 frames (10 s) by default, so inference cost is for 1024 frames. Measure on docker --cpus=0.1 --memory=512m;
if too slow, retrain with a shorter max_length (crop the positional-embedding grid) before exporting."""
import argparse, hashlib, json, pathlib, numpy as np, onnxruntime as ort, torch
from onnxruntime.quantization import QuantType, quantize_dynamic
from transformers import ASTForAudioClassification
ap = argparse.ArgumentParser(); ap.add_argument("--ckpt", required=True); ap.add_argument("--out", default="onnx_out"); ap.add_argument("--temperature", type=float, default=1.0); a = ap.parse_args()
out = pathlib.Path(a.out); out.mkdir(exist_ok=True); m = ASTForAudioClassification.from_pretrained(a.ckpt).eval()
class W(torch.nn.Module):
    def __init__(s, m): super().__init__(); s.m = m
    def forward(s, input_values): return s.m(input_values=input_values).logits
x = torch.randn(1, m.config.max_length, m.config.num_mel_bins)
torch.onnx.export(W(m), (x,), str(out/"model_fp32.onnx"), input_names=["input_values"], output_names=["logits"], dynamic_axes={"input_values": {0: "batch"}, "logits": {0: "batch"}}, opset_version=17, dynamo=False)
quantize_dynamic(str(out/"model_fp32.onnx"), str(out/"model.onnx"), weight_type=QuantType.QInt8)
ref = m(input_values=x).logits.detach().numpy()
for name in ("model_fp32.onnx", "model.onnx"):
    got = ort.InferenceSession(str(out/name), providers=["CPUExecutionProvider"]).run(None, {"input_values": x.numpy()})[0]
    print(name, "max |logit diff|", float(np.abs(ref-got).max()), "argmax equal:", int(ref.argmax()) == int(got.argmax()))
sha = hashlib.sha256((out/"model.onnx").read_bytes()).hexdigest()
json.dump({"labels": ["blast", "vessel", "biology", "environmental_noise", "ambient"], "mean": -4.2677393, "std": 4.5689974, "num_mel_bins": m.config.num_mel_bins,
           "max_length": m.config.max_length, "sample_rate": 16000, "temperature": a.temperature, "sha256": sha, "version": "v1", "thresholds": {"blast": 0.7}}, open(out/"model_card.json", "w"), indent=2)
print("size MB", (out/"model.onnx").stat().st_size/1e6, "sha256", sha[:12], "-> publish model.onnx + model_card.json; check int8 accuracy on your TEST split before trusting it")
