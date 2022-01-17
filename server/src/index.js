const express = require('express')
const app = express()
var cors = require('cors')
const port = 8080
const host = '0.0.0.0'

const routes = require('./routes')

app.use(cors())
app.use(express.static('../build/'))

routes(app)

app.listen(port, host, () => {
  console.log(`App listening at http://${host}:${port}`)
})
