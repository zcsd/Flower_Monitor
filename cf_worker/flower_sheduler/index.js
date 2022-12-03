// src/index.js
var src_default = {
    async scheduled(controller, env, ctx) {
      ctx.waitUntil(scheduler(env));
    }
  };
  
  async function scheduler(env) {
    var curr_time = new Date(Date.now());
    curr_time.setHours(curr_time.getHours() + 8);
  
    const sleep_time = new Set(['23','0','1','2','3','4','5','6']);
  
    if (sleep_time.has(curr_time.getHours().toString()) == false && curr_time.getMinutes().toString() == '1') {
      // 7:01 8:01 ... 22:01 capture photo and store
      const capture_url = "https://flower.xxxxxx/flower-status/";
      var with_chat = false;
  
      if (curr_time.getHours().toString() == '12') {
        // 12:01 Send msg to tg group 
        with_chat = true;
      }
      const data = JSON.stringify({"chat_id": env.CHAT_ID, "with_env": true , "with_img": true, "with_chat": with_chat, "is_cron": true});
      await fetch(capture_url, {method: 'POST', headers: {"Content-Type":"application/json", 'Authorization': 'Bearer ' + env.AUTH_TOKEN}, body: data});
    } else {
      // 23:01 23:31 00:01 00:31 ... 06:31 07:31 08:31 ... 22:31 23:01
      // record enviroments 
      const env_url = "https://flower.xxxxxx/flower-env/";
      const data = JSON.stringify({"chat_id": env.CHAT_ID, "with_env": true , "with_img": false, "with_chat": false, "is_cron": true});
      await fetch(env_url, {method: 'POST', headers: {"Content-Type":"application/json", 'Authorization': 'Bearer ' + env.AUTH_TOKEN}, body: data});
    }
  }
  
  export {
    src_default as default
  };