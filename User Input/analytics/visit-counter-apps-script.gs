// Bitchin' Blasters - sign-ups sheet setup + visit counter receiver.
var SHEET_ID = '1cW5cOF-IH6pj4tmDF8RjX10WNF6tSbWux1Az_4FBYFE';

function clean(v, max) {
  v = String(v == null ? '' : v).slice(0, max);
  return /^[=+\-@]/.test(v) ? "'" + v : v;
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

// One-off: builds the tabs, headers and Page Summary formulas. Safe to run once.
function setup() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  ss.rename("Bitchin' Blasters – Sign-ups & Site Visits");
  ss.setSpreadsheetTimeZone('Australia/Brisbane');
  var defs = [
    ['Sign-ups', ['Date Signed Up','Name','Email','Sales & Deals','Events & Field Updates','Industry News & Updates','New Listings','Source','Notes']],
    ['Early Birds', ['Date Registered','Name','Email','Code Sent (THATSBITCHIN25)','Code Used','Also on Sign-ups list','Notes']],
    ['Site Visits', ['Timestamp','Page','Referrer','Device','Region','Visitor ID']],
    ['Page Summary', ['Page','Views (all time)','Views (last 7 days)','Views (today)','Unique visitors (all time)']]
  ];
  for (var i = 0; i < defs.length; i++) {
    var sh = i === 0 ? ss.getSheets()[0] : ss.insertSheet();
    sh.setName(defs[i][0]);
    var h = sh.getRange(1, 1, 1, defs[i][1].length);
    h.setValues([defs[i][1]]).setFontWeight('bold').setFontColor('#2AFF00').setBackground('#080D08').setWrap(true);
    sh.setFrozenRows(1);
    sh.setColumnWidths(1, defs[i][1].length, i === 3 ? 170 : 190);
  }
  var ps = ss.getSheetByName('Page Summary');
  var pages = ['/','/who-we-are.html','/your-build.html','/3d-printing.html','/store.html','/build-gallery.html','/brands.html','/signup.html','/terms.html'];
  var rows = [];
  for (var r = 0; r < pages.length; r++) {
    var n = r + 2;
    rows.push([pages[r],
      "=COUNTIF('Site Visits'!$B:$B,$A" + n + ")",
      "=COUNTIFS('Site Visits'!$B:$B,$A" + n + ",'Site Visits'!$A:$A,\">=\"&(NOW()-7))",
      "=COUNTIFS('Site Visits'!$B:$B,$A" + n + ",'Site Visits'!$A:$A,\">=\"&TODAY())",
      "=IFERROR(ROWS(UNIQUE(FILTER('Site Visits'!$F:$F,'Site Visits'!$B:$B=$A" + n + "))),0)"]);
  }
  rows.push(['TOTAL','=SUM(B2:B10)','=SUM(C2:C10)','=SUM(D2:D10)',
    "=IFERROR(ROWS(UNIQUE(FILTER('Site Visits'!$F2:$F,'Site Visits'!$F2:$F<>\"\"))),0)"]);
  ps.getRange(2, 1, rows.length, 5).setFormulas(rows);
  ps.getRange(11, 1, 1, 5).setFontWeight('bold');
}
