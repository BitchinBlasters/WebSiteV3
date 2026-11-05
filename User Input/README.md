# User Input — Content System

This folder is the entire "backend" for the Bitchin' Blasters site. You add
content here (images/videos + a matching `.txt` file), commit and push, and
the site rebuilds itself automatically — no code editing required.

## How it works, in one paragraph

Every piece of content (a build photo, a product, a brand) is a **pair**: one
media file (image or a txt pointing at a YouTube video) and one `.txt` file
that describes it. A shared build script reads every pair, reads every
`Keywords:` line, and cross-links anything that shares a keyword — a build
photo tagged `flash-bang` will automatically show a button to the "Flash
Bang" product, and that product's page will automatically show a "see
examples" link back to every build/event tagged with `flash-bang`.

## Folder map

| Folder | Feeds into | Pairing style |
|---|---|---|
| `/portfolio/` | Gallery page | Flat: `name.jpg` + `name.txt` (numbered extras: `name 2.jpg`) |
| `/products/store/spare-deals/` | Store page | One subfolder per item |
| `/products/store/used-blasters/` | Store page | One subfolder per item |
| `/products/3d-printed/` | 3D Printing page | One subfolder per item |
| `/brands/` | Brands We Endorse page | Flat: `name.png` + `name.txt` |
| `/your-build/` | (reserved — not active yet) | — |
| `/image-assets/` | Hero/background images site-wide | One shared `assets.txt` |
| `/analytics/` | Visit counter (page views into the sign-ups sheet) | `visit-counter.txt` + receiver script |

Every folder above (except `/image-assets/` and `/your-build/`) has its own
`README.md` with the exact `.txt` template and image-naming example for that
folder specifically — check there before adding your first entry.

## The golden rule: keywords must match EXACTLY

Keyword matching is **not smart** — it's a plain text match (case doesn't
matter, but everything else does). `flash-bang` and `Flash-Bang` are treated
as the same keyword. `flash-bang` and `flash bang` (hyphen vs space) are
**NOT** the same keyword — they will silently fail to connect, with no error
shown anywhere.

**Avoid generic keywords that could apply to more than one brand's product.**
If two different brands both make a "barrel," don't tag both products just
`barrel` — they'll get mixed together anywhere that keyword is used. Prefix
with the brand or product line instead:
- `rex-barrel` (Rex Tactical's barrel)
- `acme-barrel` (Acme Airsoft's barrel)

A good habit: before typing a new keyword, search the other txt files in this
folder tree for it first, to make sure you're not accidentally colliding two
unrelated things — or splitting one thing into two spellings.

## Naming multiple images/photos of the same thing

Whichever file matches the `.txt` file's name **exactly** is the main
thumbnail. Any file with the same name plus a space and a number —
`flash-bang-carry 2.jpg`, `flash-bang-carry 3.jpg` — is treated as an
additional photo of that same entry. Numbers can skip (2, then 4 is fine) —
whatever exists gets shown, in order, with no error.

## Automation

A GitHub Action rebuilds the site automatically:
- Every Sunday at midnight (Brisbane time)
- Or any time, on demand, via the "Run workflow" button in the repo's
  **Actions** tab — use this if you only added one thing and don't want to
  wait for the weekly run.

You never need to run anything locally. Add your files, commit, push (or
just upload through GitHub's web UI), and the rebuild handles the rest.

## Priority — choosing the order things appear in

Add a `Priority:` line to any entry's `.txt` file (builds, events, products and brands) to choose where it appears:

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
