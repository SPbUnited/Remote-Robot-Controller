
// import "./input.js";
import { validateSpeed, mapTrigger, mapStick, sleep } from "./input.js";
import {
    voltageUp,
    voltageDown,
    toggleDribbler,
    toggleCharge,
    switchSpeed,
    switchAutokick,
    kickUp,
    kickDown,
    drSpeedUp,
    drSpeedDown,
    switchBot,
    beep,
    stopAll
} from './controls.js';


let origin = location.hostname;
let api = "http://" + origin + ":8001/api/";
let wsApi = "ws://" + origin + ":8001/api/webclient";

window.addEventListener("gamepadconnected", function (e) {
    let gp = navigator.getGamepads()[e.gamepad.index];
    console.log(gp);
});

let socket = new WebSocket(wsApi);
socket.onmessage = wsMsg;

document.getElementById('stop_all').onclick = stopAll;

async function wsMsg(event) {
    // console.log(`[message] Data: ${event.data}`);
    // event.
  //  console.log(gp);
//
    let content = document.getElementById("content");
    let menus = content.getElementsByClassName("submenu");
    let msg = JSON.parse(event.data);
    for (let i = 0; i < 8; i++) {
        menus[i].getElementsByClassName("header")[0].textContent = "Robot: " + msg["robot_" + i]["address"];
        menus[i].getElementsByClassName("speedX")[0].textContent =
            "X: " + msg["robot_" + i]["speed_x"] + " " +
            "Y: " + msg["robot_" + i]["speed_y"] + " " +
            "W: " + msg["robot_" + i]["speed_w"] + " ";

        // menus[i].getElementsByClassName("speedY")[0].textContent = "Y: " + msg["robot_" + i]["speed_y"] + " Pr";
        // menus[i].getElementsByClassName("speedW")[0].textContent = "W: " + msg["robot_" + i]["speed_w"] + " Pr";
        menus[i].getElementsByClassName("voltage")[0].textContent = "Voltage: " + msg["robot_" + i]["robot_voltage"] + "pr";
        menus[i].getElementsByClassName("kickerVoltage")[0].textContent = "KickerVoltage: " + msg["robot_" + i]["kicker_voltage"] + "pr";
        menus[i].getElementsByClassName("drSpeed")[0].textContent = "Dribbler Speed: " + msg["robot_" + i]["dribbler_speed"] + "pr";

        if (msg["robot_" + i]["charge_en"])
            menus[i].getElementsByClassName("chargeEn")[0].textContent = "Charge: Enabled";
        else
            menus[i].getElementsByClassName("chargeEn")[0].textContent = "Charge: Disabled";

        if (msg["robot_" + i]["dribbler_en"])
            menus[i].getElementsByClassName("drEn")[0].textContent = "Dribbler: Enabled";
        else
            menus[i].getElementsByClassName("drEn")[0].textContent = "Dribbler: Disabled";
        if (msg["robot_" + i]["auto_kick_en"] || msg["robot_" + i]["auto_kick_upper"])
            if (msg["robot_" + i]["auto_kick_upper"] && !msg["robot_" + i]["auto_kick_en"])
                menus[i].getElementsByClassName("autokick")[0].textContent = "Autokick: Straight";
            else if (!msg["robot_" + i]["auto_kick_upper"] && msg["robot_" + i]["auto_kick_en"])
                menus[i].getElementsByClassName("autokick")[0].textContent = "Autokick: Chip";
            else
                menus[i].getElementsByClassName("autokick")[0].textContent = "Autokick: Momentum";
        else
            menus[i].getElementsByClassName("autokick")[0].textContent = "Autokick: Disabled";

        if (msg["robot_" + i]["ball_checker"])
            menus[i].getElementsByClassName("ballChecker")[0].textContent = "BallChecker: +";
        else
            menus[i].getElementsByClassName("ballChecker")[0].textContent = "BallChecker: -";

        menus[i].style.borderColor = "rgba(255, 0, 0, 0.6)";
    }

    currentBot = msg["selected_bot"];
    speedRange = msg["speed_range"];
    boxIp = msg["box_ip"];

    document.getElementById("selected_bot").textContent = "Selected Robot: " + currentBot;
    document.getElementById("speed_range").textContent = "Max Speed: " + Math.trunc((speedRange + 1) / 5 * 100) + "%";
    document.getElementById("box_ip").textContent = "Box IP: " + boxIp;


    menus[currentBot].style.borderColor = "#ff0000";

    // menus[currentBot].


}


async function inputLoop() {
    while (true) {
       console.log('asd');
        try {
            let gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads : []);
            if (!gamepads) {
                console.log('asd');
                continue;
            }

            let gp = gamepads[0];

            // if (buttonPressed(gp.buttons[12]))
            //     await drSpeedUp();
            //
            // if (buttonPressed(gp.buttons[13]))
            //     move_backward();

            // if (!buttonPressed(gp.buttons[12]) && !buttonPressed(gp.buttons[13]))
            // stop_fb();

            set_fb(mapStick(-gp.axes[1]));
            set_lr(mapStick(gp.axes[0]));
            console.log('hello');

           kickUpFlag = (buttonPressed(gp.buttons[0]));

            kickDownFlag = (buttonPressed(gp.buttons[1]));



            if (btnLegal(gp, 2))
                await toggleDribbler();

            if (btnLegal(gp, 3))
                await switchAutokick();

            if (btnLegal(gp, 4))
                await switchSpeed();

            beepFlag = (buttonPressed(gp.buttons[5]));

            set_rot(mapTrigger(gp.buttons[6].value - gp.buttons[7].value));

            if (btnLegal(gp, 8))
                await switchBot();

            if (btnLegal(gp, 9))
                await toggleCharge();

            if (btnLegal(gp, 12))
                await drSpeedUp();

            if (btnLegal(gp, 13))
                await drSpeedDown();

            if (btnLegal(gp, 14))
                await voltageDown();

            if (btnLegal(gp, 15))
                await voltageUp();

            // if (btnLegal(gp, 16)) {}


            if (socket)
                await sendSpeedNTriggers();
            await sleep(100);
        } catch (e) {
            await stopAll();
        }

    }


}


function btnLegal(gp, index) {
    if (btnChanged(buttonPressed(gp.buttons[index]), index))
        if (buttonPressed(gp.buttons[index]))
            return true;
    return false;
}

async function sendSpeedNTriggers() {
    let msg = {
        command: "speed_n_triggers",
        speed_x: speedX,
        speed_y: speedY,
        speed_w: speedW,
        kick_up: kickUpFlag,
        kick_down: kickDownFlag,
        beep: beepFlag
    };
    await socket.send(JSON.stringify(msg));
}


let interval;

let speedX = 0;
let speedY = 0;
let speedW = 0;
let kickUpFlag = false;
let kickDownFlag = false;
let beepFlag = false;

let currentBot = 0
let speedRange = 0
let boxIp = "0.0.0.0"

let botNumb = 0;
let dribblerEn = false;
let chargeEn = false;

let xEn = true;
let yEn = true;
let wEn = true;

let btnEn = new Array(20);
btnEn.forEach(elem => elem = true);

function btnChanged(value, index) {
    if (btnEn[index] === value)
        return false;
    else {
        btnEn[index] = value;
        return true;
    }
}


function stop() {
    speedX = 0;
    speedY = 0;
    speedW = 0;
}


function move_forward(speed = null) {
    if (!yEn)
        return;
    speedY += validateSpeed(speed);
    yEn = false;
}

function move_backward(speed = null) {
    if (!yEn)
        return;
    speedY -= validateSpeed(speed);
    yEn = false;
}

function set_fb(speed = 0) {
    speedY = speed;  // _validate_speed(speed);
}

function stop_fb() {

    speedY = 0;
    yEn = true;
}

function move_right(speed = null) {
    if (!xEn)
        return;
    speedX += validateSpeed(speed);
    xEn = false;
}

function move_left(speed = null) {
    if (!xEn)
        return;
    speedX -= validateSpeed(speed);
    xEn = false;
}

function set_lr(speed = 0) {
    speedX = speed;  //_validate_speed(speed);
}

function stop_lr() {
    speedX = 0;
    xEn = true;
}

function rot_ccv(speed = null) {
    if (!wEn)
        return;
    speedW += validateSpeed(speed);
    wEn = false;
}

function rot_cv(speed = null) {
    if (!wEn)
        return;
    speedW -= validateSpeed(speed);
    wEn = false;
}

function set_rot(speed = 0) {
    speedW = speed;  // _validate_speed(speed);
}

function stop_rot() {
    speedW = 0;
    wEn = true;
}


// Input stuff

function buttonPressed(b) {
    console.log(b)
    if (typeof (b) == "object") {
        return b.pressed;
    }
    return b === 1.0;
}

if (!('ongamepadconnected' in window)) {
    // No gamepad events available, poll instead.
    interval = setInterval(pollGamepads, 500);
}

function pollGamepads() {
    var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads : []);
    for (var i = 0; i < gamepads.length; i++) {
        var gp = gamepads[i];
        console.log(gp);
        if (gp) {
            inputLoop();
            clearInterval(interval);
        }
    }
}



