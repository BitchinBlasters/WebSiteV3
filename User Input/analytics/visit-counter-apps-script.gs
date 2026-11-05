// Bitchin' Blasters - visit counter receiver.
// Paste this into a new Apps Script project (script.google.com), then
// Deploy > New deployment > Web app > Execute as: Me, Who has access: Anyone.
// Copy the web app URL into visit-counter.txt as:  Endpoint: <url>
var SHEET_ID = '19yYZ4rjOozJg7rSu44wn2ys_qIiMZPQZtYsZxmhgJ8I';

function clean(v, max) {
  v = String(v == null ? '' : v).slice(0, max);
  return /^[=+\-@]/.test(v) ? "'" + v : v;   // stop spreadsheet formulas being injected
}

function doPost(e) {
  try {
    var p = JSON.parse(e.postData.contents);
    var sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName('Site Visits');
    sheet.appendRow([new Date(), clean(p.page, 200), clean(p.ref, 100), clean(p.device, 20), '', clean(p.vid, 40)]);
  } catch (err) {}
  return ContentService.createTextOutput('ok');
}

function doGet() { return ContentService.createTextOutput('ok'); }
