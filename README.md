<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1d4e6b,100:2f7f8f&height=170&section=header&text=Miguel%20Carrasco&fontColor=ffffff&fontSize=44&fontAlignY=34&desc=AI%20%2F%20LLM%20engineer&descAlignY=56&descSize=18" width="100%" alt="Miguel Carrasco, AI / LLM engineer"/>

Hi, I'm Miguel. I work on LLM systems, and lately most of my time goes into small decision models: models that read a prompt and a list of options and return a probability for each option, instead of generating text. They're fast enough to sit in front of every request, so I use them for routing, triage and classification. The part I care about most is whether those probabilities can be trusted, so I measure calibration as well as accuracy.

**[clef](https://github.com/MiguelCarrascoB/clef)** is where most of this lives. It's a self-hosted server for Cloudflare's 9B multimodal decision model with an OpenAI-compatible API. Most of the work went into serving: one GPU worker with micro-batching and length bucketing, CPU layer streaming and int8 so it runs on 8 to 16 GB cards, and an eval module that reports ECE and Brier next to accuracy. On my RX 7900 XTX it does 149 ms p50 per record and about 8.9 req/s at concurrency 16. I also found that nf4 changes the top answer on roughly 9% of inputs, so the docs recommend int8 instead.

**[laya-router](https://github.com/MiguelCarrascoB/laya-router)** uses a smaller decision model to pick the cheapest LLM that can handle a prompt, plus a prompt-injection check before anything is routed. It works, but with the real model the confidence gate sends most prompts to the expensive tier, so the next step is a labelled eval set to tune it. That's written up in the README.

**[qwen-image-2.1-playground](https://github.com/MiguelCarrascoB/qwen-image-2.1-playground)** is a side project: a plain-JS web UI on top of ComfyUI for running Qwen-Image-2.1 locally on Apple Silicon and AMD GPUs, with text-to-image and image editing. Qwen-Image-2.1-Turbo support is next.

### What I'm working on now

Training my own decision model with [Unsloth](https://unsloth.ai/docs/basics/train-your-own-decision-model-with-unsloth): a LoRA fine-tune with a classifier head, evaluated on the public typed-decisions benchmark. The plan is to publish the model card, the exact training config and a before/after table with calibration numbers. The goal is to serve it from clef afterwards.

### Log

- **2026-10** · Starting the Unsloth decision model
- **2026-10** · clef: low-memory modes, calibration evals, docs site
- **2026-09** · qwen-image-2.1-playground and laya-router

Python, PyTorch, Transformers, FastAPI, ROCm, MLX, Docker.<br/>
[LinkedIn](https://www.linkedin.com/in/miguelcarrascobn)

<details>
<summary>En español</summary>

Hola, soy Miguel. Trabajo con sistemas basados en LLMs, y últimamente sobre todo con modelos de decisión pequeños: modelos que reciben un prompt y una lista de opciones y devuelven una probabilidad para cada una, en vez de generar texto. Son lo bastante rápidos para ponerlos delante de cada petición, así que los uso para enrutar, priorizar y clasificar. Lo que más me importa es si esas probabilidades son fiables, así que mido la calibración además de la precisión.

- **clef**: servidor propio para el modelo de decisión de 9B de Cloudflare, con API compatible con OpenAI, modos de poca memoria (funciona en GPUs de 8 a 16 GB) y evaluación con ECE y Brier.
- **laya-router**: elige el LLM más barato capaz de resolver cada prompt y filtra intentos de prompt injection.
- **qwen-image-2.1-playground**: interfaz web para generar y editar imágenes en local con Qwen-Image-2.1.

Ahora mismo estoy entrenando mi propio modelo de decisión con Unsloth.

</details>
