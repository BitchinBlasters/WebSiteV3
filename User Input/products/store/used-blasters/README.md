# /products/store/used-blasters/ — Store page, Used Blasters section

One subfolder per item — same layout style as `/products/3d-printed/`.

## Folder layout

```
/rex-mk2-carbine/
    info.txt
    rex-mk2-carbine.jpg   <- matches folder name = main thumbnail
    rex-mk2-carbine 2.jpg <- extra photo
```

## Template — info.txt

```
Title: Rex MK2 Carbine — Used
Description: One-liner shown on the product card, condition notes etc.
Price: $180
Brand: Rex Tactical
Keywords: rex-mk2
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
