const { getDevices } = require('./controllers/audio')

module.exports = (app) => {
  app.get('/audiodevice', getDevices)
}