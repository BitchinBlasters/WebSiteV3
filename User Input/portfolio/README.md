# /portfolio/ — Gallery

Feeds the **Gallery** page. Two kinds of entry: a **Build** (a finished
blaster you made) or an **Event** (a skirmish day, meetup, etc). Photos and
video-highlight entries both live here, side by side.

## File pairing

One media file (or one txt-only entry pointing at YouTube) + one `.txt` file,
**sharing the exact same name** (extension aside):

```
flash-bang-carry.jpg
flash-bang-carry.txt
```

Extra photos of the same entry: same name + a space + a number.
```
flash-bang-carry.jpg      <- main thumbnail
flash-bang-carry 2.jpg
flash-bang-carry 3.jpg
```

## Template — Build (photo)

```
Title: Flash Bang Carry
Description: One-liner shown on the gallery card
Breakdown: The longer written build story shown on the full build page —
can be multiple sentences/paragraphs.
Type: Build
Keywords: flash-bang, 3d-printed, cqb-loadout
```

## Template — Event (photo)

```
Title: QLD Skirmish Day - March
Description: One-liner shown on the gallery card
Breakdown: Written recap of the day
Type: Event
Location: Ipswich, QLD
Keywords: flash-bang
```

## Template — Build or Event with a YouTube highlight

Same as above, plus:

```
YouTube: https://youtube.com/watch?v=XXXXXXXXXXX
Hover Start: 0:45
Keywords: flash-bang (1:32), 3d-printed (0:45), cqb-loadout (2:10)
```

- `Hover Start` — where the preview starts when someone hovers the thumbnail.
- The `(mm:ss)` next to a keyword is where THAT specific thing appears in the
  video — used for the keyword jump-buttons under the full player. Optional
  per keyword; leave it off a keyword that isn't tied to a specific moment.
- Every clip — however it was triggered (hover, click, or a keyword jump) —
  always plays for exactly 20 seconds and then pauses. This is fixed
  site-wide, not something you set per video.

## Writing the Breakdown (paragraphs and sub-headings)

```
Breakdown: The first paragraph of the story.
It can run over several lines and stays one paragraph.

Parts List
Next paragraph, with a short heading line above it.

Final paragraph.
```

- A **blank line** starts a new paragraph.
- A single line break inside a paragraph stays a line break.
- A **short line on its own** (40 characters or fewer, not ending in a full stop, comma or similar) becomes a **sub-heading**.
- `Description` is different: one line, shown under the tile on the Gallery.

## How the Gallery shows entries

- Under every tile: the **Title** (bold) and the **Description** (small, tan, two lines at most, then `...`).
- All categories showing: each category is a sideways carousel (4 tiles wide on a computer, 2 on a phone).
- One category open: a grid of tiles (4 wide on a computer, 2 on a phone).
- Header buttons: pick a category (click again to return to all); filter **Photos** or **Videos** (click again to return to All); search.
- Each category banner's title is a button, with an X in the corner to return to all categories.

## Required fields

`Title`, `Type` are always required. `Breakdown` is required for the full
detail page to have content. `Location` is required only when `Type: Event`.
`Keywords` is optional but is how this entry connects to products/brands —
an entry with no keywords still works, it just won't cross-link anywhere.

## Keyword reminder

See the root README for the full explanation — case doesn't matter, but
`flash-bang` and `flash bang` are different keywords. Don't use a generic
keyword that more than one brand's product could match.

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


## Type decides which Gallery category it appears in

`Type:` must be one of **Build**, **Event**, **Tech Tip** or **Review**. Each goes into the matching
category of the Gallery page. An entry with any other Type is not posted (the rebuild log says so).
Photos and videos alternate within each section, ordered by `Priority:`. A section with nothing in it
shows "Content coming soon".

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


## YouTube entries need no picture

For an entry with a `YouTube:` line you can leave out the thumbnail picture. The site uses the video's own YouTube
thumbnail. If you do add a picture with the same name as the txt file, that picture is used instead.
