# Workflows

Three ready-to-load ComfyUI workflows that already have the **Variant Prompt Builder** node wired in.
Pick the one that matches how you load models. All are designed to be as user-friendly as possible: open the file, select your model(s), type variants, queue.

---

## `flux.json`

**For:** Flux / Flux.2 family models.

Uses the specialized Flux pipeline (UNETLoader + CLIPLoader + VAELoader + Flux2Scheduler + EmptyFlux2LatentImage + CFGGuider + SamplerCustomAdvanced).

Based on Comfy-Org style Flux.2 templates, modified so:

- Positive prompt comes from Variant Prompt Builder
- Noise seed comes from Variant Prompt Builder

**Requirements:** Working Flux / Flux.2 setup (diffusion model, text encoder, VAE) already in your ComfyUI `models/` folders.

---

## `aio.json`

**For:** All-in-one / single-file checkpoints (most SD 1.5, SDXL, Pony, Illustrious, many community “AIO” packs).

Uses **one** loader node: `CheckpointLoaderSimple`.

Standard KSampler + EmptyLatentImage pipeline. Extremely simple to use — just pick your .safetensors checkpoint and go.

---

## `checkpoint.json`

**For:** Models distributed as separate files (model / UNET + CLIP + VAE).

Uses **three** separate loader nodes:

- UNETLoader (or equivalent model loader)
- CLIPLoader
- VAELoader

Useful when you keep components in different folders or mix-and-match.

---

## Common notes for all three

- The Variant Prompt Builder is already connected to the positive `CLIPTextEncode` and to the seed/noise input.
- Negative prompt is still a normal text box (you can leave the default or change it).
- Workflows end on a `PreviewImage` node. Replace with `SaveImage` if you want automatic disk saves.
- After loading, always double-check that the correct model files are selected in the loader node(s) for *your* installation.
- The custom node must be installed first (see main README).

These workflows are intentionally minimal and self-contained so a new user can go from download → first batch of variants in under a minute.
