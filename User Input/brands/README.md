# /brands/ — Brands We Endorse page

Flat pairing, same style as `/portfolio/` — logo file + `.txt` file sharing
the exact same name.

```
acme-airsoft.png
acme-airsoft.txt
```

If a brand ever needs more than one image, the same numbered-extras
convention as portfolio works here too (`acme-airsoft 2.png`).

## Template — acme-airsoft.txt

```
Title: Acme Airsoft
Description: One-liner shown on the Brands page
Keywords: acme
Supplier Link: https://acmeairsoft.example.com
```

`Keywords` here is just for reference/consistency — the actual product ↔
brand link is made by each product's own `Brand:` field (see
`/products/3d-printed/README.md`), not by matching this brand's keywords.

## Important — logo is optional per product-linkage

If a brand referenced by a product's `Brand:` field doesn't have a matching
entry here (or has no image), it's simply skipped wherever brand logos would
normally show (e.g. on a build page) — no broken image, no placeholder text.

## Required fields

`Title` is always required. Everything else is optional.

## Priority (optional — controls the order)

Add a `Priority:` line to any entry's `.txt` file to choose where it appears:

```
Priority: 1
```

- **Lowest number goes first.** `1` is the top spot, then `2`, `3` and so on.
- Entries **without** a Priority line go **after** all the numbered ones, in A-Z order by title.
- Two entries with the same number are put in A-Z order by title.
- Gaps are fine (1, 5, 10) so you can slot something in later. Decimals work too (`1.5`).
- If the number is not a plain number (for example `top`), it is ignored and the entry is treated as having no Priority.

## Series (optional — keep related entries side by side)

Give two or more entries the same `Series:` line and they are kept next to each other, in their Priority order:

```
Series: Scylla HPA
```

- Use exactly the same words on every part (capitals do not matter).
- On the Gallery a series counts as one step in the photo, video, photo, video pattern, so part 1 and part 2 are never split by a photo.
- Everything else about each part stays the same: its own thumbnail, preview and page.
- Works in every folder: portfolio, products, brands.
- Give the parts the same Type so they land in the same section.
