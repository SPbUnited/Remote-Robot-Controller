let origin = location.hostname;
let api = "http://" + origin + ":8001/api/";
let wsApi = "ws://" + origin + ":8001/api/webclient";

async function switchBot() {
    let response = await fetch(api + "bot/switch_bot", {method: "PUT"});
    if (response.ok) {}
}

async function switchSpeed() {
    let response = await fetch(api + "bot/switch_speed_range", {method: "PUT"});
    if (response.ok) {}
}

async function switchAutokick() {
    let response = await fetch(api + "bot/switch_autokick", {method: "PUT"});
    if (response.ok) {}
}

async function toggleCharge() {
    let response = await fetch(api + "bot/toggle_charge", {method: "PUT"});
    if (response.ok) {}
}

async function toggleDribbler() {
    let response = await fetch(api + "bot/toggle_dribbler", {method: "PUT"});
    if (response.ok) {}
}

async function voltageUp() {
    let response = await fetch(api + "bot/voltage_up", {method: "PUT"});
    if (response.ok) {}
}

async function voltageDown() {
    let response = await fetch(api + "bot/voltage_down", {method: "PUT"});
    if (response.ok) {}
}

async function drSpeedUp() {
    let response = await fetch(api + "bot/dribbler_speed_up", {method: "PUT"});
    if (response.ok) {}
}

async function drSpeedDown() {
    let response = await fetch(api + "bot/dribbler_speed_down", {method: "PUT"});
    if (response.ok) {}
}

async function kickUp() {
    let response = await fetch(api + "bot/kick_up", {method: "PUT"});
    if (response.ok) {}
}

async function kickDown() {
    let response = await fetch(api + "bot/kick_down", {method: "PUT"});
    if (response.ok) {}
}

async function beep() {
    let response = await fetch(api + "bot/beep", {method: "PUT"});
    if (response.ok) {}
}

async function stopAll() {
    let response = await fetch(api + "bot/stop_all", {method: "PUT"});
    if (response.ok) {}
}

export {beep,switchBot,drSpeedDown,drSpeedUp,kickDown,kickUp,switchAutokick,switchSpeed,toggleCharge,toggleDribbler,voltageDown,voltageUp,stopAll};