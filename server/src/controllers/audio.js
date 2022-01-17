
const { audioDevices } = require('../services/audio')

module.exports.getDevices = async (req, res) => {
  const devices = await audioDevices();
  res.send(devices);
}