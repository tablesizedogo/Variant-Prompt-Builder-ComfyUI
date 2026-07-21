"""
ComfyUI Variant Prompt Builder
------------------------------
Combine one base ("general") prompt with a numbered list of variants and
expand it into a batch of prompts (and matching seeds) that ComfyUI's
native list-execution turns into one image generation per variant.

Example
-------
general_text: "a cute image of a cat"
variant_text: "1. black cat 2. white cat 3. big cat 4. orange cat"

produces the prompt list:
    "a cute image of a cat, black cat"
    "a cute image of a cat, white cat"
    "a cute image of a cat, big cat"
    "a cute image of a cat, orange cat"

See the repository README for full documentation.
"""

import re

MAX_SEED = 0xFFFFFFFFFFFFFFFF


def _split_numbered(text):
    """
    Split `text` on COUNTING markers (1. 2. 3. ...). Markers may appear
    inline ("1. black cat 2. white cat") or one per line. Only numbers that
    continue the counting sequence are treated as separators, so a stray
    number inside a variant's own text (e.g. "cat with 3 legs") is left
    untouched and does not create a spurious split.

    Returns a list of cleaned variant strings, in order.
    """
    if not text:
        return []

    # \b(\d+)\.(?!\d)  -> a number at a word boundary, followed by a dot
    # that is NOT followed by another digit (so "2.5" is never a marker).
    marker = re.compile(r"\b(\d+)\.(?!\d)")
    matches = list(marker.finditer(text))

    accepted = []
    expected = None
    for m in matches:
        num = int(m.group(1))
        if expected is None:
            expected = num
        if num == expected:
            accepted.append(m)
            expected += 1

    variants = []
    for i, m in enumerate(accepted):
        start = m.end()
        end = accepted[i + 1].start() if i + 1 < len(accepted) else len(text)
        chunk = text[start:end].strip().strip(" ,;\n\t")
        if chunk:
            variants.append(chunk)
    return variants


class VariantPromptBuilder:
    """
    Inputs
    ------
    general_text        : base prompt, prepended to every variant.
    variant_text         : numbered list of variants ("1. ... 2. ... 3. ...").
    images_per_variant   : how many images to generate for each variant.
    use_same_seed        : True  -> reuse the same seed(s) across every
                                     variant, so equivalent images line up
                                     (e.g. image #1 of every variant shares
                                     the same starting noise).
                            False -> every single generation gets its own
                                     unique seed.
    seed                 : base seed value.

    Outputs (all lists, except count)
    ----------------------------------
    prompt : STRING list, one entry per image to generate.
    seed   : INT list, one entry per image to generate (paired with prompt).
    count  : INT, number of variants detected in variant_text.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "general_text": ("STRING", {
                    "multiline": True,
                    "default": "a cute image of a cat",
                }),
                "variant_text": ("STRING", {
                    "multiline": True,
                    "default": "1. black cat 2. white cat 3. big cat 4. orange cat",
                }),
                "images_per_variant": ("INT", {
                    "default": 1, "min": 1, "max": 1000,
                }),
                "use_same_seed": ("BOOLEAN", {
                    "default": True,
                    "label_on": "same seed for all variants",
                    "label_off": "different seed per generation",
                }),
                "seed": ("INT", {
                    "default": 0, "min": 0, "max": MAX_SEED,
                    "control_after_generate": True,
                }),
            }
        }

    RETURN_TYPES = ("STRING", "INT", "INT")
    RETURN_NAMES = ("prompt", "seed", "count")
    OUTPUT_IS_LIST = (True, True, False)
    FUNCTION = "build"
    CATEGORY = "utils/text"

    def build(self, general_text, variant_text, images_per_variant, use_same_seed, seed):
        general = (general_text or "").strip()
        variants = _split_numbered(variant_text)

        # No numbered variants found -> fall back to the general text alone.
        if not variants:
            variants = [""]

        n = images_per_variant if (images_per_variant and images_per_variant > 0) else 1

        prompts = []
        seeds = []
        for v_idx, variant in enumerate(variants):
            if general and variant:
                combined = f"{general}, {variant}"
            elif general:
                combined = general
            else:
                combined = variant

            for k in range(n):
                prompts.append(combined)
                if use_same_seed:
                    s = seed + k                       # same seed set, reused per variant
                else:
                    s = seed + v_idx * n + k            # unique seed per generation
                seeds.append(s & MAX_SEED)

        return (prompts, seeds, len(variants))


NODE_CLASS_MAPPINGS = {
    "VariantPromptBuilder": VariantPromptBuilder,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VariantPromptBuilder": "Variant Prompt Builder",
}
