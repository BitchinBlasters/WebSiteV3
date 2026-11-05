# /products/3d-printed/ — 3D Printing page

One subfolder per item. The image matching the folder's own name is the
thumbnail; any other image in the folder is pulled in as an extra photo
automatically (the "name + number" convention isn't required in here, since
the folder itself already groups everything — but it still works if you use
it anyway).

## Folder layout

```
/flash-bang/
    info.txt
    flash-bang.jpg      <- matches folder name = main thumbnail
    flash-bang 2.jpg    <- extra photo
```

## Template — info.txt

```
Title: Flash Bang Grenade Prop
Description: One-liner shown on the product card
Brand: Acme Airsoft
Status: In Stock
Keywords: flash-bang
```

- `Status` — either `In Stock` or `Print to Order`. This is a text field, not
  a folder, on purpose — so you can flip an item's status later without
  moving any files or breaking links that point at it.
- `Brand` — must match a name in `/brands/` exactly. This is what makes the
  brand's logo (and hover submenu) show up automatically on any build page
  that uses this product.
- `Keywords` — how this product connects back to builds/events that feature
  it, and to the gallery's "see examples" filter.

## Required fields

`Title`, `Status` are always required. `Brand` is optional but skips the
brand-logo linking if left out. `Keywords` is optional but is how this
product connects to anything else on the site.

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
