// ! BUG: Mobile quit tab not working
// ! BUG: Look on error of socket.io

const CamID = sessionStorage.getItem('cam');
const MicID = sessionStorage.getItem('mic');

console.log(CamID, MicID);

const socket = io('/');
const videoGrid = document.getElementById('video-grid');
const myPeer = new Peer(undefined, {
    host: 'se-online-1.kasitphoom.com',
    //port: ''
    path: '/peerjs'
});

let isVideoLoaded = false;
let oldUserId = null;
let myUserID = null;
let PresentedUsers = [];

const myVideo = document.createElement('video');
const myCanvas = document.createElement('canvas');
const div = document.createElement('div');
myCanvas.id = 'myCanvas';
div.id = 'myCanvasDiv';
div.append(myCanvas);
videoGrid.append(div);
div.classList.add("hide");
div.classList.add("canvas");
myVideo.muted = true;

const Peers = {};

myCanvas.captureStream = myCanvas.captureStream || myCanvas.mozCaptureStream;

const endCallBtn = document.getElementById('end-call');

endCallBtn.addEventListener('click', () => {
    console.log("clicked")
    socket.emit('I-disconnect', ROOM_ID, myUserID);

    // Close all Peer connections and remove video elements
    for (const userId in Peers) {
        if (Peers.hasOwnProperty(userId)) {
            const peerConnections = Peers[userId];
            if (peerConnections) {
                // Close each Peer connection
                for (const peerConnection of peerConnections) {
                    peerConnection.close();
                }
            }
        }
    }
    history.go(-2)
});

navigator.mediaDevices.getUserMedia({
    video: CamID ? {deviceId: CamID} : false,
    audio: MicID ? {deviceId: MicID} : true
}).then(stream => {

    

    // add my video
    addVideoStream(myVideo, stream, 'myVideo', 'video');

    // flip my video
    const myVideoElement = document.getElementById('myVideo');
    myVideoElement.style.transform = 'rotateY(180deg)';

    // listen for controls button to be pressed
    const micControl = document.getElementById('mic-control');
    micControl.addEventListener('click', () => {
        socket.emit('mic-triggered', ROOM_ID, myUserID); // send signal to server
        micNotMute = "fa-microphone"
        micMute = "fa-microphone-slash" 
        stream.getAudioTracks()[0].enabled = !(stream.getAudioTracks()[0].enabled);
        micControl.classList.toggle('mic-off');
        if (micControl.classList.contains('mic-off')) {
            micControl.innerHTML = `<i class="fas ${micMute}"></i>`;
        } else {
            micControl.innerHTML = `<i class="fas ${micNotMute}"></i>`;
        }

        const avatarPlaceholder = document.getElementById(`myVideo-mic-placeholder`);
        avatarPlaceholder.classList.toggle('hide');
    });

    const cameraControl = document.getElementById('camera-control');
    cameraControl.addEventListener('click', () => {
        socket.emit('camera-triggered', ROOM_ID, myUserID); // send signal to server
        cameraNotMute = "fa-video"
        cameraMute = "fa-video-slash"
        if (CamID) stream.getVideoTracks()[0].enabled = !(stream.getVideoTracks()[0].enabled);
        cameraControl.classList.toggle('camera-off');
        if (cameraControl.classList.contains('camera-off')) {
            cameraControl.innerHTML = `<i class="fas ${cameraMute}"></i>`;
        } else {
            cameraControl.innerHTML = `<i class="fas ${cameraNotMute}"></i>`;
        }

        const myVideo = document.getElementById('myVideo');
        myVideo.classList.toggle('hide');

        const avatarPlaceholder = document.getElementById(`myVideo-avatar-placeholder`);
        avatarPlaceholder.classList.toggle('hide');
    });

    const handControl = document.getElementById('hand-control');
    handControl.addEventListener('click', () => {
        socket.emit('hand-triggered', ROOM_ID, myUserID); // send signal to server
        handControl.classList.toggle('hand-raise');
        const myVideo = document.getElementById('myVideo-div');
        myVideo.classList.toggle('hand-raise');
    });

    const canvasControl = document.getElementById('canvas-control');
    canvasControl.addEventListener('click', ToggleCanvasControl);

    // get lists of user informations
    socket.emit('get-users', ROOM_ID);
    socket.on('users', users => {
        console.log(users);
        PresentedUsers = users;
    });

    socket.on('user-connected', userId => {
        console.log('User connected: ' + userId)
        // connect to new user and send my stream
        setTimeout(connectToNewUser,1500,userId,stream, myCanvas.captureStream(60));
        // Play sound that user join
        const audio = new Audio('/sound/Join.wav');
        audio.play();
        audio.volume = 0.7;
    });

    socket.on('user-disconnected', userId => { // when user disconnect
        if (Peers[userId]) {
            const peerConnections = Peers[userId];
            if (peerConnections) {
                // Close each Peer connection
                for (const peerConnection of peerConnections) {
                    peerConnection.close();
                }
            }
            
        }

        console.log("user disconnected: " + userId);

        // remove every video element and canvas element
        const videoDiv = document.getElementById(`${userId}-div`);
        const canvasDiv = document.getElementById(`${userId}-canvas-div`);
        if (videoDiv) {
            videoDiv.remove();
        }
        if (canvasDiv) {
            canvasDiv.remove();
        }

        videoGridChanged();
        updateUserNumber(); // Update number of users
    });

    socket.on('user-mic-triggered', userId => { // when user mute mic
        console.log('User muted: ' + userId)
        const micPlaceholder = document.getElementById(`${userId}-mic-placeholder`);
        console.log(micPlaceholder.classList);
        micPlaceholder.classList.toggle('hide');
        
    });

    socket.on('user-camera-triggered', userId => { // when user turn off camera
        console.log('User camera triggered: ' + userId)
        const videoDiv = document.getElementById(`${userId}-div`);
        const avatarPlaceholder = document.getElementById(`${userId}-avatar-placeholder`);
        // remove video and show avatar instead, vise versa
        if (videoDiv) {
            videoDiv.childNodes[0].classList.toggle('hide');
        }
        if (avatarPlaceholder) {
            avatarPlaceholder.classList.toggle('hide');
        }
    });

    socket.on('user-hand-triggered', userId => { // when user raise hand
        console.log('User hand triggered: ' + userId)
        const videoDiv = document.getElementById(`${userId}-div`);
        videoDiv.classList.toggle('hand-raise');
    });

    socket.on('user-test', text => { // when user test
        console.log(text)
    });

    // on video call
    myPeer.on('call', call => {
        console.log('This peer is being called...');
        let videoCount = 0;
        if (call.metadata === 'video') { // check that if call is for video or canvas
            call.answer(stream);
        } else if (call.metadata === 'canvas') {
            call.answer(myCanvas.captureStream(60));
        }
        call.on('stream', userVideoStream => {
            // console.log metadata
            console.log(call.metadata);
            console.log('This peer is being called...on-stream...1');
            if (call.metadata === 'video') {
                videoCount++;
                Peers[call.peer] = [call];
                if (videoCount > 1) return; // make sure that only one video is added
                const video = document.createElement('video');
                // find user information of this id
                const user = PresentedUsers.find(user => user.id === call.peer);
                console.log(user);
                addVideoStream(video, userVideoStream, call.peer, 'video', user.mic, user.camera, user.hand);
            } else if (call.metadata === 'canvas') {
                const videocanvas = document.createElement('video');
                addVideoStream(videocanvas, userVideoStream, call.peer, 'canvas');
            }
        });
    });
}).catch(err => {
    // !=================================================! //
    // TODO: handle error when user have no camera or mic  //
    // !=================================================! //

    console.log(err);
    document.writeln(err);
});

myPeer.on('open', id => {
    socket.emit('join-room', ROOM_ID, id); // send signal to server that you are joining
    myUserID = id;
});

// check for tab close
window.addEventListener('beforeunload', function (e) {
    e.preventDefault();
    socket.emit('I-disconnect', ROOM_ID, myUserID);
    socket.emit('test', ROOM_ID, `I am leaving: ${myUserID}`);
    
});

// check for tab close
window.addEventListener('unload', function (e) {
    e.preventDefault();
    socket.emit('I-disconnect', ROOM_ID, myUserID);
    socket.emit('test', ROOM_ID, `I am leaving: ${myUserID}`);
    
});

function addVideoStream(video, stream, id, className, mic = true, camera = true, hand = false) { // add video to grid
    const div = document.createElement('div');

    div.id = id + '-div'; // add id for video div
    div.className = className + '-div';
    if (className === 'canvas') div.id = id + '-canvas-div'; // add id for canvas

    div.append(video);
    video.srcObject = stream;
    video.addEventListener('loadedmetadata', () => {
        video.play();
    });
    video.id = id;
    video.className = className;

    videoGrid.append(div);

    if (className != 'canvas') { // add avatar for video
        // Add avatar placeholder
        const avatarDiv = document.createElement('div');
        avatarDiv.id = id + '-avatar-placeholder';
        avatarDiv.className = 'avatar-placeholder';
        avatarDiv.innerHTML = `
            <img src="/images/user-default-avatar.svg" alt="Avatar">
        `;
        div.append(avatarDiv);
    
        const avatarPlaceholder = document.getElementById(`${id}-avatar-placeholder`);
        avatarPlaceholder.classList.add('hide');

        // Add mic muted icon
        const micDiv = document.createElement('div');
        micDiv.id = id + '-mic-placeholder';
        micDiv.className = 'mic-placeholder';
        micDiv.innerHTML = `
            <div class="mic-container">
                <i class="fas fa-microphone-slash"></i>
            </div>
        `;
        div.append(micDiv);

        const micPlaceholder = document.getElementById(`${id}-mic-placeholder`);
        micPlaceholder.classList.add('hide');

        // add username placeholder
        const usernameDiv = document.createElement('div');
        usernameDiv.id = id + '-username-placeholder';
        usernameDiv.className = 'username-placeholder';
        let username = id == 'myVideo' ? 'You' : id;
        usernameDiv.innerHTML = `
            <p>${username}</p>
        `;
        div.append(usernameDiv);

        if(!mic){
            micPlaceholder.classList.remove('hide');
        }
        if(!camera){
            avatarPlaceholder.classList.remove('hide');
            video.classList.add('hide');
        }
        if(!hand){
            div.classList.remove('hand-raise');
        }else if(hand){
            div.classList.add('hand-raise');
        }
    }

    if (videoGrid.classList.contains('on-focus')) div.classList.add('hide');

    videoGridChanged(); // Update grid size
    updateUserNumber(); // Update number of users
}

function connectToNewUser(userId, stream, canvasStream) {
    console.log('Connecting to new user...');
    if (oldUserId != userId) isVideoLoaded = false;
    oldUserId = userId;

    // Make separate calls for video and canvas streams
    const videoCall = myPeer.call(userId, stream, { metadata: 'video' });
    const canvasCall = myPeer.call(userId, canvasStream, { metadata: 'canvas' });
    Peers[userId] = [videoCall, canvasCall];
    // Handle 'stream' event for video call
    videoCall.on('stream', userVideoStream => {
        console.log('This peer is being called...on-stream (video)...');
        if (isVideoLoaded) return;
        const video = document.createElement('video');
        addVideoStream(video, userVideoStream, userId, 'video');
        isVideoLoaded = true;
        // Handle call closure for video call
        videoCall.on('close', () => {
            video.remove();
        });
    });

    // Handle 'stream' event for canvas call
    canvasCall.on('stream', userCanvasStream => {
        console.log('This peer is being called...on-stream (canvas)...');
        const videocanvas = document.createElement('video');
        addVideoStream(videocanvas, userCanvasStream, userId, 'canvas');

        // Handle call closure for canvas call
        canvasCall.on('close', () => {
            videocanvas.remove();
        });
    });
}