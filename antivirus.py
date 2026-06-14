<!DOCTYPE html>
<html lang="tl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>KINEME - Philippine Political News</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 20px;
      background: #0a0a0a;
      color: #fff;
      text-align: center;
    }
    h1 { color: #ff0000; }
    .news { max-width: 800px; margin: 20px auto; text-align: left; background: #1a1a1a; padding: 20px; border-radius: 10px; }
    button {
      padding: 12px 25px;
      font-size: 16px;
      background: #0066ff;
      color: white;
      border: none;
      border-radius: 5px;
      margin: 10px;
      cursor: pointer;
    }
    .ad-popup {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: #fff;
      color: #000;
      padding: 30px;
      border-radius: 15px;
      box-shadow: 0 0 20px rgba(255,0,0,0.8);
      z-index: 9999;
      max-width: 400px;
      display: none;
    }
  </style>
</head>
<body>

  <h1>📰 KINEME</h1>
  <p>Philippine Political News</p>

  <div class="news">
    <h2>Volunteer lawyers backing up impeach team</h2>
    <p>By: Gabriel Pabico Lalu, Kenneth Christiane Basilio — INQUIRER.net</p>
    <p>June 12, 2026</p>
    <p>MANILA, Philippines — Instead of the “bloodbath” she claimed...</p>
  </div>

  <button onclick="scanNow()">Scan for Updates</button>
  <button onclick="showAd()">Test Ad</button>

  <!-- Pop-up Ad -->
  <div id="adPopup" class="ad-popup">
    <h2>📢 Kineme Advertisement</h2>
    <p id="adText"></p>
    <button onclick="closeAd()">Close</button>
  </div>

  <script>
    const ads = [
      "🔥 Star this repo para mas maraming updates! ⭐",
      "💰 Gusto mo ng custom website o tool? PM me!",
      "❤️ Support Gamecrit2345 sa GitHub",
      "🛡️ Educational Project Only",
      "🚀 More projects coming soon!",
      "Like & Share para lumabas pa ang iba pang content!"
    ];

    function showAd() {
      const randomAd = ads[Math.floor(Math.random() * ads.length)];
      document.getElementById('adText').innerHTML = randomAd;
      document.getElementById('adPopup').style.display = 'block';
    }

    function closeAd() {
      document.getElementById('adPopup').style.display = 'none';
    }

    // Auto pop-up ads every 15-30 seconds
    setInterval(() => {
      if (Math.random() > 0.4) {  // 60% chance
        showAd();
      }
    }, 18000);

    // First ad after 7 seconds
    setTimeout(showAd, 7000);

    function scanNow() {
      alert("🔍 Scanning for latest news... (Simulation only)");
      setTimeout(showAd, 1200);
    }
  </script>

</body>
</html>
