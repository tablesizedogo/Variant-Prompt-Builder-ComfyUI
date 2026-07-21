# Changelog

## v1.1.0 — Multi-workflow support
- Added three ready-to-use workflows tailored to different model loading styles:
  - `workflows/flux.json` — specialized Flux / Flux.2 pipeline
  - `workflows/aio.json` — single CheckpointLoaderSimple (all-in-one models)
  - `workflows/checkpoint.json` — separate UNET + CLIP + VAE loaders
- Renamed and cleaned the original Flux workflow (removed specific 9B naming and unofficial model references).
- Updated documentation to explain the three model-type options and emphasize “download → install → generate”.
- Fixed LICENSE and pyproject.toml placeholders with real author information.

## v1.0.0 — Variant Prompt Builder
- Replaced the single numbered-list splitter with a two-field node:
  `general_text` (base prompt) + `variant_text` (numbered variants),
  combined per-variant as `"general, variant"`.
- Added `images_per_variant` parameter to generate more than one image
  per variant.
- Added `use_same_seed` toggle: matched seeds across variants (for
  side-by-side comparison) vs. fully unique seeds per generation.
- The node now generates and outputs its own seed list, wired directly
  into the sampler's seed / RandomNoise node — no manual seed entry needed.
- Added a pytest unit test suite and GitHub Actions CI.

## v0.2.0 — Numbered Prompt Splitter (superseded)
- Introduced ComfyUI list-execution: one numbered text block → N prompts
  → N images from a single queue action.
- Sequential-number detection so stray numbers inside a prompt's own text
  aren't mistaken for a new list item.

## v0.1.0 — Baseline
- Original single-prompt, single-image Flux.2 txt2img workflow,
  unmodified from the official Comfy-Org template.
