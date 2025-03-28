const express = require("express");
const fs = require('fs');
const jose = require('node-jose');
const app = express();


const identify_resp  = require('./data/pbaco.json')


app.use(express.json());
const PORT = 3000;

// GET well known jwks
app.get('/.well-known/jwks.json', (req, res) => {
 res.header("Content-Type",'application/json');
 res.send(JSON.stringify(identify_resp));
  const ks = fs.readFileSync('pbaco.json')
})



// Return authorize request
app.post("/api/create/jwks", (req, res) => {
 console.log('/create/jwks');
 res.header("Content-Type",'application/json');
const keyStore = jose.JWK.createKeyStore();

keyStore.generate("RSA", 2048, { alg: "RS256", use: "sig" }).then((result) => {
  fs.writeFileSync(
    "Keys.json",
    JSON.stringify(keyStore.toJSON(true), null, "  ")
  );
});
 res.send(JSON.stringify('Ok'));
})

app.get('/jwks.json', (req, res) => {
  const ks = fs.readFileSync("Keys.json");

  const keyStore = jose.JWK.asKeyStore(ks.toString());

  res.send(JSON.stringify(keyStore));
})


app.get("/tokens", async (req, res) => {
  const JWKeys = fs.readFileSync("keys.json");

  const keyStore = await jose.JWK.asKeyStore(JWKeys.toString());

  const [key] = keyStore.all({ use: "sig" });

  const opt = { compact: true, jwk: key, fields: { typ: "jwt" } };
  let date = new Date();
  date.setDate(date.getDate() + 1);
  const payload = JSON.stringify({
    exp: Math.floor(date / 1000),
    iat: Math.floor(Date.now() / 1000),
    sub: "test",
  });

  const token = await jose.JWS.createSign(opt, key).update(payload).final();

  res.send({ token });
});


app.post("/verify", async (req, res) => {
  let resourcePath = "jwks.json";

  let token = req.body;

  let decodedToken = jwt.decode(token, { complete: true });

  let kid = decodedToken.headers.kid;

  return new Promise(function (resolve, reject) {
    var jwksPromise = config.request("GET", resourcePath);

    jwksPromise
      .then(function (jwksResponse) {
        const jwktopem = require("jwk-to-pem");

        const jwt = require("jsonwebtoken");

        const [firstKey] = jwksResponse.keys(kid);
        const publicKey = jwktopem(firstKey);
        try {
          const decoded = jwt.verify(token, publicKey);
          resolve(decoded);
        } catch (e) {
          reject(e);
        }
      })
      .catch(function (error) {
        reject(error);
      });
  });
});

app.listen(PORT, console.log(`Listening on port ${PORT}....`));
