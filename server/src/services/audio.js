const util = require('util');
const exec = util.promisify(require('child_process').exec);

module.exports.audioDevices = async () => {
  const { stdout } = await exec('aplay -l');
  const stdoutList = stdout.split('\n');
  const devices = stdoutList.filter(line => line.startsWith('card'));
  return devices;
}
