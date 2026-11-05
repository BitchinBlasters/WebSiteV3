# Visit counter

Counts page views into the "Site Visits" tab of the Sign-ups & Site Visits sheet. No third-party service.

1. Deploy `visit-counter-apps-script.gs` as a web app (Execute as: Me, Access: Anyone).
2. Put its address in `visit-counter.txt` as `Endpoint: https://script.google.com/macros/s/.../exec`.
3. Run "Rebuild site from User Input". Until an endpoint is set, no tracking code is added to any page.

Stored per view: time, page, referring site, Mobile/Desktop, random visitor ID. No IP, name or email.
Skipped when the browser sends Do Not Track, on localhost, and in any browser that has opened a page with `?notrack` on the end
(e.g. https://bitchinblasters.com.au/?notrack on your own phone and PC, once).
