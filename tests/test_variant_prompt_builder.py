"""
Unit tests for the Variant Prompt Builder ComfyUI custom node.

The node lives outside a normal Python package (ComfyUI custom nodes are
loaded dynamically from a folder, not imported by name), so it's loaded
here directly from its file path.

Run with:
    pip install -r requirements-dev.txt
    pytest tests/ -v
"""
import importlib.util
import os

import pytest

NODE_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "custom_nodes",
    "comfyui-variant-prompt-builder",
    "__init__.py",
)

_spec = importlib.util.spec_from_file_location("variant_prompt_builder", NODE_PATH)
node_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(node_module)

VariantPromptBuilder = node_module.VariantPromptBuilder
split_numbered = node_module._split_numbered


# ---------------------------------------------------------------------------
# Splitting logic
# ---------------------------------------------------------------------------

def test_inline_variants_are_split_correctly():
    variants = split_numbered("1. black cat 2. white cat 3. big cat 4. orange cat")
    assert variants == ["black cat", "white cat", "big cat", "orange cat"]


def test_line_separated_variants_are_split_correctly():
    variants = split_numbered("1. happy\n2. sad\n3. surprised")
    assert variants == ["happy", "sad", "surprised"]


def test_numbers_inside_variant_text_do_not_break_the_sequence():
    variants = split_numbered("1. a cat with 3 legs 2. a dog with 2 tails")
    assert variants == ["a cat with 3 legs", "a dog with 2 tails"]


def test_decimal_numbers_are_not_treated_as_markers():
    variants = split_numbered("1. version 2.5 release notes 2. changelog")
    assert variants == ["version 2.5 release notes", "changelog"]


def test_empty_text_returns_no_variants():
    assert split_numbered("") == []


def test_text_without_numbers_returns_no_variants():
    assert split_numbered("just a plain sentence") == []


# ---------------------------------------------------------------------------
# Prompt building
# ---------------------------------------------------------------------------

def test_general_and_variant_text_are_combined():
    prompts, seeds, count = VariantPromptBuilder().build(
        general_text="a cute image of a cat",
        variant_text="1. black cat 2. white cat",
        images_per_variant=1,
        use_same_seed=True,
        seed=100,
    )
    assert count == 2
    assert prompts == [
        "a cute image of a cat, black cat",
        "a cute image of a cat, white cat",
    ]


def test_no_general_text_falls_back_to_variant_only():
    prompts, _, count = VariantPromptBuilder().build(
        general_text="",
        variant_text="1. red 2. blue",
        images_per_variant=1,
        use_same_seed=True,
        seed=0,
    )
    assert count == 2
    assert prompts == ["red", "blue"]


def test_no_variants_falls_back_to_general_text_only():
    prompts, _, count = VariantPromptBuilder().build(
        general_text="a lonely prompt",
        variant_text="",
        images_per_variant=1,
        use_same_seed=True,
        seed=0,
    )
    assert count == 1
    assert prompts == ["a lonely prompt"]


# ---------------------------------------------------------------------------
# Seeding logic
# ---------------------------------------------------------------------------

def test_same_seed_toggle_on_reuses_seed_across_variants():
    _, seeds, _ = VariantPromptBuilder().build(
        general_text="a cat",
        variant_text="1. a 2. b",
        images_per_variant=1,
        use_same_seed=True,
        seed=100,
    )
    assert seeds == [100, 100]


def test_same_seed_toggle_off_gives_a_unique_seed_per_variant():
    _, seeds, _ = VariantPromptBuilder().build(
        general_text="a cat",
        variant_text="1. a 2. b",
        images_per_variant=1,
        use_same_seed=False,
        seed=100,
    )
    assert seeds == [100, 101]


def test_multiple_images_per_variant_with_same_seed_matches_columns():
    # With same_seed ON, image #1 of every variant shares a seed, and
    # image #2 of every variant shares a (different) seed, so variants
    # stay visually comparable at each image index.
    _, seeds, _ = VariantPromptBuilder().build(
        general_text="a cat",
        variant_text="1. a 2. b",
        images_per_variant=2,
        use_same_seed=True,
        seed=100,
    )
    assert seeds == [100, 101, 100, 101]


def test_multiple_images_per_variant_with_different_seed_are_all_unique():
    _, seeds, _ = VariantPromptBuilder().build(
        general_text="a cat",
        variant_text="1. a 2. b",
        images_per_variant=2,
        use_same_seed=False,
        seed=100,
    )
    assert seeds == [100, 101, 102, 103]
    assert len(set(seeds)) == len(seeds)


def test_total_output_length_is_variants_times_images_per_variant():
    prompts, seeds, count = VariantPromptBuilder().build(
        general_text="a cat",
        variant_text="1. a 2. b 3. c",
        images_per_variant=3,
        use_same_seed=True,
        seed=0,
    )
    assert count == 3
    assert len(prompts) == len(seeds) == 3 * 3


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
