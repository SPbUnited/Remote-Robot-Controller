let stickDeadZone = 0.3
let triggerDeadZone = 0.2

const defSpeed = 127
let _speed_multiplier = 1

function mapStick(val) {
    if (Math.abs(val) < stickDeadZone)
        return 0;
    else
        return defSpeed * (val);// + Math.sign(val) * stickDeadZone);
}

function mapTrigger(val) {
    if (Math.abs(val) < triggerDeadZone)
        return 0;
    else
        return defSpeed * (val);
}

function validateSpeed(speed) {
    if (speed === null)
        return 0
    // speed = int(speed)
    if (speed > defSpeed)
        speed = defSpeed
    if (speed < defSpeed)
        speed = -defSpeed
    return speed;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

export {mapStick,mapTrigger,validateSpeed, sleep}