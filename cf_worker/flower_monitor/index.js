export default {
    async fetch(request, env) {
      return await handleRequest(request, env)
    }
  }
  
  //https://api.telegram.org/botxxxxxxxxxxxxxxxxxx/setWebhook?url=https://flower-monitor.xxxx.workers.dev
  async function handleRequest(request, env) {
    if (request.method == "POST") {
      const payload = await request.json();
      
      if ('message' in payload) { 
        var msgText;
        if ('text' in payload.message) {
          msgText = payload.message.text.toString();
        } else {
          msgText = 'ignore';
        }
  
        const chatId = payload.message.chat.id;
  
        if (msgText == 'see' || msgText == 'See') { // 'see' message
          var datetime = new Date(Date.now());
          datetime.setHours(datetime.getHours() + 8); //UTC+8
          const sleeptime = new Set(['23','0','1','2','3','4','5','6']);
  
          if (sleeptime.has(datetime.getHours().toString())) { // if in sleet time, just send sleeping text
            var textSend = "\u{1F31C}\u{1F31C}\u{1F31C}\u{1F31C}\u{1F31C}\u{1F31C}\u{1F31C}\u{1F31C}\u{1F31C}\u{1F31C}\u{1F31C}\n";
            textSend += "\u{1F60A}\u{1F60A}主人，我正在睡觉觉.\u{1F60A}\u{1F60A}\n";
            textSend += "\u{1F331}\u{1F331}\u{1F331}\u{1F331}\u{1F331}\u{1F331}\u{1F331}\u{1F331}\u{1F331}\u{1F331}\u{1F331}"
  
            const botURL = "https://api.telegram.org/bot" + env.BOT_TOKEN + "/sendMessage";
            const msgSend = JSON.stringify({"chat_id": chatId, "text": textSend, "parse_mode": "HTML"});
            await fetch(botURL, {method: 'POST', headers: {"Content-Type":"application/json"}, body: msgSend});
          } else { // not in sleep time, then trigger to send photo
            const data = JSON.stringify({"chat_id": chatId, "with_env": true , "with_img": true, "with_chat": true, "is_cron": false});
            const flowerURL = "https://flower.xxxxxx/flower-status/"
            await fetch(flowerURL, {method: 'POST', headers: {"Content-Type":"application/json", 'Authorization': 'Bearer ' + env.AUTH_TOKEN}, body: data});
          }
        } else if(msgText == 'ignore') { // do nothing
          console.log("ignore");
        } else { // other text message
          const textSend = payload.message.text + "\n\u{1F331}\u{1F331}\u{1F331}";
          const botURL = "https://api.telegram.org/bot" + env.BOT_TOKEN + "/sendMessage";
          const msgSend = JSON.stringify({"chat_id": chatId, "text": textSend, "parse_mode": "HTML"});
          await fetch(botURL, {method: 'POST', headers: {"Content-Type":"application/json"}, body: msgSend});
        }
      }
    }
    return new Response("OK") // Doesn't really matter
  }
  
  async function getFilename(dt) {
      const yearStr = dt.getFullYear().toString();
      
      const monthStr = await timeStr(dt.getMonth() + 1);
      const dayStr = await timeStr(dt.getDate());
      const hourStr = await timeStr(dt.getHours());
      const minuteStr = await timeStr(dt.getMinutes());
      
      const ts = yearStr + monthStr + '/' + dayStr + '/' + hourStr + '_' + minuteStr + '.jpg';
  
      return ts;
  }
  
  async function timeStr(t) {
      var tStr =  t.toString();
      if (tStr.length == 1) {
          tStr = '0' + tStr;
      }
      return tStr;
  }
  
  