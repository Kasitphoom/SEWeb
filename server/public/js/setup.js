const CamSelect = document.getElementById('cam-select')
const MicSelect = document.getElementById('mic-select')
const Preview = document.getElementById('preview')
const Submit = document.getElementById('submit')
const pathArray = window.location.pathname.split('/');
const ROOM_ID = pathArray[2];

if (!navigator.mediaDevices?.enumerateDevices) {
    console.log("enumerateDevices() not supported.");
} else {
    // List cameras and microphones.
    navigator.mediaDevices
        .enumerateDevices()
        .then((devices) => {
            devices.forEach((device) => {
                if (device.kind === 'videoinput') {
                    const option = document.createElement('option')
                    option.value = device.deviceId
                    option.innerText = device.label
                    CamSelect.appendChild(option)
                }else if (device.kind === 'audioinput') {
                    const option = document.createElement('option')
                    option.value = device.deviceId
                    option.innerText = device.label
                    MicSelect.appendChild(option)
                }
                console.log(`${device.kind}: ${device.label} id = ${device.deviceId}`);
            });
            showStream("default", "default")
        })
        .catch((err) => {
            console.error(`${err.name}: ${err.message}`);
        });
}

CamSelect.addEventListener('change', async (e) => {
    await showStream(e.target.value, MicSelect.value)
})

async function showStream(camid, micid) {
    const stream = await navigator.mediaDevices.getUserMedia({
        video: {deviceId: camid},
        audio: {deviceId: micid}
    })
    Preview.srcObject = stream
    Preview.play()
}

Submit.addEventListener('click', async (e) => {
    e.preventDefault()
    sessionStorage.setItem('cam', CamSelect.value)
    sessionStorage.setItem('mic', MicSelect.value)
    window.location.href = `/room/${ROOM_ID}`
});