
const bodyParser = require("body-parser");
var express = require('express');
var cors = require('cors')

app= express()

app.use(cors())
app.use(bodyParser.json());

h1= {id: 1, host: "www.string.pl", blocked: true,
  ip: "123.123.123", threat: false}

h2= {id: 2, host: "www.string.pl", blocked: false,
  ip: "123.123.123", threat: true}

hb= {id: 1, host: "www.string.pl", ip: "123.123.123", time:Date()}
hb2= {id: 2, host: "www.host.pl", ip: "123.123.123", time:Date()}


t1= {id: 1, host: "www.string.pl", type: "host",details:"unsafe host", threat: true, detected:Date()}
t2= {id: 2, host: "www.int.pl", type: "host",details:"unsafe host", threat: true, detected:Date()}

hosts = [h1,h2]
ths = [t1,t2]
blacklist = [hb,hb2]
wl = [hb,hb2]




app.get('/hosts',async (req, res)=> {
    res.send(hosts)
})

app.get('/threats',async (req, res)=> {
  res.send(ths)
})


app.post('/blacklist', (req, res)=> {
  req.body.time = Date()
  blacklist.push(req.body)
  res.send()

})

app.post('/whitelist', (req, res)=> {
  req.body.time = Date()
  wl.push(req.body)
  res.send()

})

app.get('/blacklist',async (req, res)=> {
  res.send(blacklist)
})

app.get('/whitelist',async (req, res)=> {
  res.send(wl)
})


app.delete('/blacklist/:id',async (req, res)=> {
  blacklist.splice(blacklist.findIndex(v=>v.id=req.params.id));
  res.send(blacklist)
})

app.delete('/whitelist/:id',async (req, res)=> {
  wl.splice(wl.findIndex(v=>v.id=req.params.id));
  res.send(wl)
})



app.listen(3000, function() {
  console.log('Listening on port 3000')
});



