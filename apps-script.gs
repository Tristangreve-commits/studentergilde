// Google Apps Script til tilmeldinger og guldbilletter.
// Sæt den ind under Udvidelser > Apps Script i jeres Google Sheet (se README.md).

function doPost(e) {
  const p = e.parameter;
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  if (sheet.getLastRow() === 0) sheet.appendRow(['Tidspunkt', 'Type', 'Navn', 'Svar', 'Kode']);
  sheet.appendRow([new Date(), p.type || '', p.navn || '', p.svar || '', p.kode || '']);
  return ContentService.createTextOutput('ok');
}
