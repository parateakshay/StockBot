const WebSocket = require('ws')
var ProtoBuf = require("protobufjs");

"use strict";
let Message = ProtoBuf
.loadProtoFile('./PricingData.proto', (err, builder)=>{
    Message = builder.build('PricingData')
    loadMessage()
})



let loadMessage = ()=> {
    const url = 'wss://streamer.finance.yahoo.com'
    const connection = new WebSocket(url)
    connection.onopen = () => {
    connection.send('{"subscribe":["TSLA","AXSM","UBER","MIRM","GRKZF","BTCUSD=X","ETHUSD=X","AUDUSD=X","^DJI","^IXIC","^RUT","^TNX","^VIX","^CMC200","^FTSE","^N225"]}')
    }

    connection.onerror = (error) => {
    console.log(`WebSocket error: ${error}`)
    }

    connection.onmessage = (e) => {
    let msg = Message.decode(e.data)
    console.log('Decoded message', msg)
    }
}