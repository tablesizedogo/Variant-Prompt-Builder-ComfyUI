# Example inputs and outputs

## Example 1 — basic variant set

**general_text**
```
a cute image of a cat
```

**variant_text**
```
1. black cat 2. white cat 3. big cat 4. orange cat
```

**images_per_variant:** `1`
**use_same_seed:** `True`
**seed:** `100`

**Result: 4 images generated**

| # | Prompt sent to the model | Seed |
|---|---|---|
| 1 | `a cute image of a cat, black cat` | 100 |
| 2 | `a cute image of a cat, white cat` | 100 |
| 3 | `a cute image of a cat, big cat` | 100 |
| 4 | `a cute image of a cat, orange cat` | 100 |

---

## Example 2 — multiple images per variant, matched seeds

Same inputs as above, but **images_per_variant = 2** and **use_same_seed =
True**. Image #1 of every variant shares a seed, and image #2 of every
variant shares a different (but also consistent) seed — useful for
comparing variants side-by-side under matched noise.

**Result: 8 images generated**

| # | Prompt | Seed |
|---|---|---|
| 1 | `a cute image of a cat, black cat` | 100 |
| 2 | `a cute image of a cat, black cat` | 101 |
| 3 | `a cute image of a cat, white cat` | 100 |
| 4 | `a cute image of a cat, white cat` | 101 |
| 5 | `a cute image of a cat, big cat` | 100 |
| 6 | `a cute image of a cat, big cat` | 101 |
| 7 | `a cute image of a cat, orange cat` | 100 |
| 8 | `a cute image of a cat, orange cat` | 101 |

---

## Example 3 — fully unique seeds

Same inputs as Example 1, but **use_same_seed = False**. Every image gets
its own seed, so no two generations share starting noise.

| # | Prompt | Seed |
|---|---|---|
| 1 | `a cute image of a cat, black cat` | 100 |
| 2 | `a cute image of a cat, white cat` | 101 |
| 3 | `a cute image of a cat, big cat` | 102 |
| 4 | `a cute image of a cat, orange cat` | 103 |

---

## Example 4 — one-per-line variants

Variants don't need to be on one line — this works identically to Example 1:

**variant_text**
```
1. black cat
2. white cat
3. big cat
4. orange cat
```
