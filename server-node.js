const net = require("net");

const host = "localhost";
const port = 26200;

const server = net.createServer(function (socket) {
  socket.on("connect", function (buffer) {
    console.log("connect", buffer.toString());
  });
  socket.on("error", function (buffer) {
    console.log("error", buffer.toString());
  });

  let base_url = "http://127.0.0.1:8000";
  let endpoint = "/listen/strategy/signal";
  let url = base_url + endpoint;

  socket.on("data", function (buffer) {
    let data = JSON.parse(buffer.toString());
    let req = require("request");
    req.post(
      url,
      {
        json: { 
            strategy: data.table_name,
            signal: data.new 
        }
      },
      function (error, response, body) {
        if (!error && response.statusCode == 200) {
          console.log(body);
        }
      }
    );
  });
});

server.listen(port, host);

// Sample data
/* {
    relid: '16389',
    level: 'ROW',
    name: 'signaltrigger',
    when: 'AFTER',
    old: null,
    table_name: 'bounce_scalper',
    event: 'INSERT',
    args: null,
    table_schema: 'public',
    new: {
      symbol: 'AUCTIONUSDT',
      STOCHd_9_3_3: 33.33333333333298,
      'BBM_6_2.0': 5.626666666666666,
      'BBU_6_2.0': 5.641573786516034,
      close: 5.61,
      volume: 3.78,
      STOCHk_9_3_3: 16.666666666666476,
      signal: 1,
      RSI_9: 22.186686945278694,
      low: 5.61,
      interval: '1m',
      high: 5.61,
      ATRr_12: 0.004841215664736577,
      time: '2022-07-08 14:08:00',
      processed: 0,
      'BBL_6_2.0': 5.611759546817298,
      open: 5.61,
      ADX_9: 31.58699678270313
    }
  } */
