# /products/store/spare-deals/ — Store page, Spare Deals section

One subfolder per item — same layout style as `/products/3d-printed/`.

## Folder layout

```
/used-hopup-unit/
    info.txt
    used-hopup-unit.jpg   <- matches folder name = main thumbnail
    used-hopup-unit 2.jpg <- extra photo
```

## Template — info.txt

```
Title: Used Hop-Up Unit
Description: One-liner shown on the product card
Price: $25
Brand: Acme Airsoft
Keywords: acme-hopup
```

## Required fields

`Title`, `Price` are always required. `Brand` and `Keywords` are optional,
same rules as `/products/3d-printed/README.md`.

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
- On Pics & Vids a series counts as one step in the photo, video, photo, video pattern, so part 1 and part 2 are never split by a photo.
- Everything else about each part stays the same: its own thumbnail, preview and page.
- Works in every folder: portfolio, products, brands.
- Give the parts the same Type so they land in the same section.
