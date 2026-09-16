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
