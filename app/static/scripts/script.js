// ==========================
// Fungsi untuk mengambil data terbaru dari server
// ==========================
function fetchData() {
  $.get("/get_latest_data", function (data) {
    if (data.error) {
      alert(data.error);
      return;
    }

    console.log(data);

    // Tampilkan data ke elemen-elemen HTML
    $("#varLuxLeft").text(data.varLuxLeft);
    $("#varLuxRight").text(data.varLuxRight);
    $("#varPositionServo").text(data.varPositionServo);
    $("#voltage").text(data.voltage);
    $("#current").text(data.current);
    $("#power").text(data.power);
    $("#energy_calc").text(data.energy_calc);
  });
}

// ==========================
// Fungsi untuk mengambil dan menampilkan data historis ke dalam tabel
// ==========================
function fetchHistoricalData() {
  $.get("/get_historical_data", function (data) {
    // Hapus semua baris yang ada di tabel terlebih dahulu
    $("#data-table tbody").empty();

    // Iterasi setiap data dan tambahkan ke tabel
    data.forEach(function (row) {
      const timestamp = new Date(row[7]).toLocaleString();
      const rowHtml = `
        <tr>
          <td>${timestamp}</td>
          <td>${row[0]}</td>
          <td>${row[1]}</td>
          <td>${row[2]}</td>
          <td>${row[3]}</td>
          <td>${row[4]}</td>
          <td>${row[5]}</td>
          <td>${row[6]}</td>
        </tr>
      `;
      $("#data-table tbody").append(rowHtml);
    });
  });
}

// ==========================
// Fungsi untuk menampilkan waktu lokal saat ini di halaman
// Format: MM/DD/YYYY, HH:MM:SS AM/PM
// ==========================
function updateLocalTime() {
  const now = new Date();
  const formattedTime = now.toLocaleString("en-US");
  $("#timestamp").text(formattedTime);
}

// ==========================
// Fungsi untuk mengekspor data historis dalam tabel ke file CSV
// ==========================
function exportToCSV() {
  const table = document.getElementById("data-table");
  const rows = table.querySelectorAll("tr");

  let csvContent = "";

  // Loop setiap baris dalam tabel dan konversi ke format CSV
  rows.forEach((row) => {
    const columns = row.querySelectorAll("th, td");
    const rowData = [];

    columns.forEach((column) => {
      // Escape tanda kutip dan bungkus setiap data dengan tanda kutip
      const cellData = column.innerText.replace(/"/g, '""');
      rowData.push(`"${cellData}"`);
    });

    csvContent += rowData.join(";") + "\n";
  });

  // Buat elemen <a> sementara untuk mendownload file CSV
  const link = document.createElement("a");
  link.href = "data:text/csv;charset=utf-8," + encodeURI(csvContent);
  link.target = "_blank";
  link.download = "historical_data.csv";

  // Jalankan klik secara otomatis untuk mulai download
  link.click();
}

// ==========================
// Eksekusi saat halaman dimuat
// ==========================
fetchData(); // Ambil data terbaru pertama kali
updateLocalTime(); // Tampilkan waktu saat ini pertama kali
fetchHistoricalData(); // Tampilkan data historis

// Update data terbaru setiap 5 detik
setInterval(fetchData, 5000);

// Update waktu lokal setiap 1 detik
setInterval(updateLocalTime, 1000);
