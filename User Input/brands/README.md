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
