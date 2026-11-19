# BUILD LOG — entry gta6-meme-x-01

Entry untuk bounty make.fun "Post a GTA 6 meme on X". Akun: daring-coyote-94.
Gambar final entry: meme-final-boarding.jpg. Teks postingan final: POST-FINAL.md.
POST.json di repo ini masih berupa placeholder bawaan starter — alamat postingan
X yang asli baru diisi setelah postingannya terbit (di luar repo ini).

## v1 — komposit PIL dari screenshot game (ditolak)

Versi pertama merakit meme dari tangkapan layar NEON BAY, game bergaya GTA 6 yang
dibangun agen kami sendiri untuk bounty gta6-01, jadi leluconnya harfiah: Rockstar
menunda GTA 6 lagi, sementara agen AI kami sudah merilis game serupa di make.fun
dan dibayar. Maskot hantu dipotong dari mark resmi press kit lalu ditempel masuk
ke adegan — satu meme hantu berdiri di atap mobil dengan papan neon "make.fun" di
menara kota, satu lagi hantu bersantai di pantai memakai kacamata hitam di samping
papan "WAITING SINCE 2013". Teks atas-bawah ditulis tebal dengan PIL. Hasilnya
dianggap jelek dan tidak menarik oleh pemilik akun, jadi v1 gugur dan tidak pernah
dipakai. Program perakitnya (make_meme.py) dan berkas-berkas antara dari masa itu
sudah dihapus dari repo pada tahap perbaikan checker (lihat bagian terakhir).

## v2 — ilustrasi AI penuh

Atas arahan untuk membuat yang jauh lebih menarik, v2 digambar utuh sebagai
ilustrasi bergaya komik dengan mark resmi sebagai acuan bentuk hantu, lalu caption
ditambahkan belakangan memakai PIL supaya ejaannya pasti. Ada dua gambar:

- meme-v2-waiting.jpg: ruang tunggu tempat para gamer berubah jadi tengkorak
  bersarang laba-laba sambil tetap memegang controller, papan antrean menunjukkan
  "NOW SERVING: 2013", sedangkan hantu make.fun melenggang keluar lewat pintu
  bercahaya membawa karung USDC dan koin bintang magenta.
- meme-v2-joyride.jpg: hantu menaiki convertible pink sambil menebar uang,
  melewati antrean di halte reyot bertuliskan "GTA 6 BUS - EST. 2013", dengan
  billboard neon raksasa "make.fun" di belakangnya.

## v3 — boarding pass pertama (pindah format ke dokumen)

Pemindaian terhadap ratusan entry yang sudah masuk menunjukkan delapan teratas
didominasi tiruan dokumen dan antarmuka sehari-hari — layar kunci ponsel, paspor
Leonida, struk belanja, tangkapan chat — sedangkan ilustrasi murni hanya mengisi
peringkat bawah. Karena itu v3 beralih format: boarding pass "LEONIDA AIR" yang
tampak tua dan lecek, seolah dibeli tahun 2013 dan tidak pernah jadi terbang.
Penumpangnya ditulis "ME (AGE 15 -> 28)", penerbangannya GTA6 dari Vice City ke
Leonida, statusnya "BOARDING: STILL WAITING", dihiasi stempel merah DELAYED 2023,
2024, dan 2025, stiker magenta "UPGRADED - PAID BY MY AI AGENT ON make.fun", dan
logo hantu di kop tiket. Artefak dokumen semacam ini belum dipakai entry teratas
mana pun saat itu. Kelemahan v3: satu stempel menimpa nilai kolom tempat duduk,
dan teks stiker terpotong di sudut kertas yang melengkung.

## v4 — boarding pass final, dibangun di sesi khusus

Versi final dibuat dari nol di dalam satu sesi agen khusus supaya seluruh proses
pembuatannya tercatat sebagai transkrip entry. Gambar dasarnya berupa foto
boarding pass lusuh tanpa teks di atas meja kayu gelap, dihasilkan dengan
generate_image; sesudah itu semua tulisan digambar tajam memakai PIL — bukan
tempelan dari sesi lain. Hasilnya adalah meme-final-boarding.jpg (1920x1280):

- Kop magenta memuat logo hantu make.fun asli dari press kit di samping tulisan
  "LEONIDA AIR / BOARDING PASS".
- Isi tiket: PASSENGER: ME (AGE 15 -> 28), FLIGHT: GTA6, FROM: VICE CITY,
  TO: LEONIDA, DATE: 17 SEP 2013, GATE: 6, SEAT: 13Y, BOARDING: STILL WAITING.
- Ketiga stempel DELAYED dipindah ke zona kosong di tengah tiket sehingga tidak
  menimpa nilai kolom mana pun — cacat v3 diperbaiki.
- Stiker magenta "UPGRADED - PAID BY MY AI AGENT ON make.fun" kini utuh di atas
  kertas, tidak terpotong sudut — cacat v3 yang kedua juga diperbaiki.
- Uji baca pada ukuran 480px lulus: logo hantu, semua kolom, stempel, dan teks
  stiker tetap terbaca jelas.

POST-FINAL.md menyimpan teks postingan yang akan mendampingi gambar ini: pitch
berisi @makefunai, play code makefun-denim-bonnet-agate, dan tautan bounty.

## Perbaikan checker (tahap terakhir)

Checker kit memberi empat FAIL pada repo, dan tahap ini memperbaiki penyebabnya:

- Berkas beban mati dibuang dari repo: make_meme.py, tiga berkas metadata
  media-generation-*.json, pratinjau check-a-480.jpg dan check-b-480.jpg,
  ghost-cutout.png, dan video.mp4. Gambar-gambar meme lama (.jpg) dipertahankan
  sebagai riwayat.
- POSTS.md dihapus karena isinya sudah digantikan POST-FINAL.md.
- BUILD-LOG.md ini ditulis ulang seluruhnya di sesi perbaikan.
- main.ts diperkuat dua edit: (a) sesudah menyalin POST.json ke direktori output,
  program membaca kembali berkas hasil salinan dan membandingkannya persis dengan
  sumber — bila berbeda, program gagal dengan pesan yang jelas; (b) baris
  keluaran terakhir kini juga mencetak id status postingan yang terurai dari URL.
  Keduanya lolos uji asap di direktori sementara dengan POST.json contoh valid.
- POST.json tetap tidak diubah: masih placeholder, menunggu URL postingan asli.
