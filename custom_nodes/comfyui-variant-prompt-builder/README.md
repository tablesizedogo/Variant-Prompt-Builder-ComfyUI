# Variant Prompt Builder (ComfyUI custom node)

Technical reference for this node. For the full project overview, see the
[repository README](../../README.md).

## Category

`utils/text` → **Variant Prompt Builder**

## Inputs

| Name | Type | Description |
|---|---|---|
| `general_text` | STRING (multiline) | Base prompt, prepended to every variant. |
| `variant_text` | STRING (multiline) | Numbered list of variants, e.g. `1. black cat 2. white cat`. Inline or one-per-line both work. |
| `images_per_variant` | INT (min 1) | How many images to generate for each variant. |
| `use_same_seed` | BOOLEAN | `True`: reuse the same seed(s) across every variant (matched noise, good for side-by-side comparisons). `False`: every generation gets a unique seed. |
| `seed` | INT | Base seed. Supports ComfyUI's fixed / increment / randomize control. |

## Outputs

| Name | Type | Description |
|---|---|---|
| `prompt` | STRING (**list**) | One combined prompt per image to generate. |
| `seed` | INT (**list**) | One seed per image, paired index-for-index with `prompt`. |
| `count` | INT | Number of variants detected in `variant_text`. |

`prompt` and `seed` are ComfyUI **list outputs**. Connect `prompt` into a
`CLIPTextEncode` node's `text` input and `seed` into a `RandomNoise` node's
`noise_seed` input, and ComfyUI's native list-execution will run the rest of
the graph once per list entry — no loop node, subgraph, or extra logic
required downstream.

## Parsing rules

Variants are separated by **counting markers**: `1.`, `2.`, `3.`, ... The
parser only treats a number as a new marker if it continues the counting
sequence starting from the first number found. This means:

- `1. a cat with 3 legs 2. a dog` → two variants (`"a cat with 3 legs"`,
  `"a dog"`) — the `3` doesn't break the sequence because the next expected
  marker is `2`, not `3`.
- `1. version 2.5 notes 2. changelog` → two variants — `2.5` is not treated
  as a marker because it's immediately followed by another digit.
- Markers can be inline (`1. a 2. b`) or on separate lines.

## Seeding formulas

Given `seed` (base), `v` = variant index (0-based), `k` = image index within
a variant (0-based):

```
use_same_seed = True   ->  seed(v, k) = seed + k
use_same_seed = False  ->  seed(v, k) = seed + v * images_per_variant + k
```

## No external dependencies

This node only uses the Python standard library (`re`). No `pip install` is
required beyond having ComfyUI itself running.
