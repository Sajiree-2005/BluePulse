"""RUN ON COLAB. UNTESTED here. Development backup only: NOT a Nugen model; never use for final results.
!pip install transformers==4.57.6 peft==0.21.2 trl==1.17.1 accelerate==1.15.0 fastapi uvicorn nest_asyncio
Step 1 train LoRA on nugen/pairs.jsonl; step 2 serve /v1/chat/completions; step 3 `cloudflared tunnel --url http://localhost:8000` and set LLM_PROVIDER=colab."""
import json, sys
BASE = "Qwen/Qwen2.5-0.5B-Instruct"
if sys.argv[1:] == ["train"]:
    from datasets import Dataset; from peft import LoraConfig; from trl import SFTTrainer, SFTConfig
    rows = [json.loads(l) for l in open("pairs.jsonl")]
    ds = Dataset.from_list([{"messages": [{"role": "user", "content": r["instruction"]}, {"role": "assistant", "content": r["response"]}]} for r in rows])
    SFTTrainer(model=BASE, train_dataset=ds, args=SFTConfig(output_dir="lora", num_train_epochs=3, per_device_train_batch_size=4, learning_rate=2e-4),
               peft_config=LoraConfig(r=16, lora_alpha=32, task_type="CAUSAL_LM")).train(); print("train done: save the LoRA adapter to ./lora")
else:
    import torch, uvicorn; from fastapi import FastAPI; from peft import AutoPeftModelForCausalLM; from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(BASE); m = AutoPeftModelForCausalLM.from_pretrained("lora", torch_dtype=torch.float16).cuda().eval(); app = FastAPI()
    @app.post("/v1/chat/completions")
    def chat(req: dict):
        ids = tok.apply_chat_template(req["messages"], add_generation_prompt=True, return_tensors="pt").cuda()
        o = m.generate(ids, max_new_tokens=req.get("max_tokens", 300), do_sample=False, output_scores=True, return_dict_in_generate=True)
        lp = torch.stack([torch.log_softmax(s[0], -1).max() for s in o.scores]).mean().exp().item()   # proxy confidence, NOT Nugen's score
        return {"choices": [{"message": {"role": "assistant", "content": tok.decode(o.sequences[0][ids.shape[1]:], skip_special_tokens=True)}}], "confidence_score": round(100*lp, 1), "provider": "colab-proxy"}
    uvicorn.run(app, host="0.0.0.0", port=8000)
