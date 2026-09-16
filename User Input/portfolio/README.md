# /portfolio/ — Build Gallery

Feeds the **Build Gallery** page. Two kinds of entry: a **Build** (a finished
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

## Required fields

`Title`, `Type` are always required. `Breakdown` is required for the full
detail page to have content. `Location` is required only when `Type: Event`.
`Keywords` is optional but is how this entry connects to products/brands —
an entry with no keywords still works, it just won't cross-link anywhere.

## Keyword reminder

See the root README for the full explanation — case doesn't matter, but
`flash-bang` and `flash bang` are different keywords. Don't use a generic
keyword that more than one brand's product could match.
