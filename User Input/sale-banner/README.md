# /sale-banner/ — sale pop-up and Store banner

One file, `sale-banner.txt`, controls two things at once:

- a pop-up on the home page that appears after a delay (once per visit)
- a banner at the top of the Store page

```
Enabled: yes
Popup: yes
Title: Example Sale On Now
Description: Optional one-line detail, e.g. what's included or when it ends.
Button: View the Sale
Link: https://paste-the-sale-link-here
Delay: 60
```

- `Enabled` — `yes` shows both, `no` hides both. Use `no` when the sale ends.
- `Popup` — `no` turns off just the home-page pop-up and keeps the Store banner. Defaults to `yes`.
- `Title` — the big headline.
- `Description` — optional. Leave it blank for a headline-only banner.
- `Button` — the button label. Defaults to "View the Sale".
- `Link` — where the button goes. **If this is blank, no button is shown**, so
  paste the sale link in here.
- `Delay` — seconds before the pop-up opens on the home page. Default 60.

No sale is running at the moment, so `Enabled` and `Popup` are `no` and Title, Description and Link are blank. The old Jefftron sale page is kept in the `_archive` folder.

After editing, run **Rebuild site from User Input** from the Actions tab.
