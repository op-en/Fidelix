# Open Energy Fidelix

This is part of the [Open Energy Project](http://op-en.se/), a research project aiming to make it easier and faster to prototype smart energy services.

## Description

A small python script that polls a fidelix service and posts the data to mqtt.

For now, inspect the source for more info!


## Persistance

To save the data to a database, a small script can be set up that sends all mqtt packets to influxdb for example.

If you want to do this in node-red, here is an example flow:

[{"id":"e4c17872.2588f8","type":"mqtt-broker","z":"5b6dea68.af3184","broker":"mqtt","port":"1883","clientid":"","usetls":false,"verifyservercert":true,"compatmode":true,"keepalive":"60","cleansession":true,"willTopic":"","willQos":"0","willRetain":null,"willPayload":"","birthTopic":"","birthQos":"0","birthRetain":null,"birthPayload":""},{"id":"d71d2961.eb4778","type":"influxdb","z":"5b6dea68.af3184","hostname":"influx","port":"8086","database":"SURE","name":"SURE Database"},{"id":"4bc78b50.005324","type":"influxdb out","z":"5b6dea68.af3184","influxdb":"d71d2961.eb4778","name":"","measurement":"","x":671,"y":290,"wires":[]},{"id":"27724328.08e90c","type":"mqtt in","z":"5b6dea68.af3184","name":"","topic":"/fidelix/#","broker":"e4c17872.2588f8","x":189,"y":265,"wires":[["2079426e.47cb5e"]]},{"id":"a31a38a6.caaab8","type":"debug","z":"5b6dea68.af3184","name":"","active":true,"console":"false","complete":"false","x":659,"y":244,"wires":[]},{"id":"2079426e.47cb5e","type":"function","z":"5b6dea68.af3184","name":"parse float","func":"msg.measurement = \"fidelix-\" + msg.topic.substr(msg.topic.lastIndexOf('/') + 1);\n\ntry{\n  msg.payload = JSON.parse(msg.payload);\n} catch(e){\n  \n}\n\nfor (var key in msg.payload) {\n    if (!msg.payload.hasOwnProperty(key)) continue;\n    msg.payload[key] = parseFloat(msg.payload[key])\n}\n\nreturn msg;","outputs":1,"noerr":0,"x":399,"y":264,"wires":[["a31a38a6.caaab8","4bc78b50.005324"]]}]
