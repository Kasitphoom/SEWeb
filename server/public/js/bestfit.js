
function videoGridChanged(){

    let classCanvas = document.querySelectorAll('.canvas-div');
    classCanvas.forEach(canvas => {
        canvas.classList.add('hide');
    });
    
    changeGridSize();
    resetCanvasSize();
    appendUserClickVideoListener();
    
}

function changeGridSize(){
    const MAX_HEIGHT = 600;

    let currentNumChild = videoGrid.childElementCount;

    // get child element count that is not display none
    for (let i = 0; i < videoGrid.childElementCount; i++) {
        if (videoGrid.children[i].classList.contains('hide')) {
            currentNumChild--;
        }
    }

    let sizecolumn = Math.ceil(Math.sqrt(currentNumChild));
    let sizerow = Math.ceil(Math.sqrt(currentNumChild));
    if (currentNumChild === 1) {sizecolumn = 1; sizerow = 1;}
    if (currentNumChild === 2) {sizecolumn = 2; sizerow = 1;}
    // if videogrid not have class called on-focus
    if(!videoGrid.classList.contains('on-focus')){
        videoGrid.style.gridTemplateColumns = `repeat(${sizecolumn}, minmax(30rem, 1fr))`;
        videoGrid.style.gridTemplateRows = `repeat(${sizerow}, minmax(30rem, ${MAX_HEIGHT / sizerow}px))`;

        // if window width is less than 1000px
        console.log(window.innerWidth)
        if (window.innerWidth < 1000) {
            sizecolumn = 1;
            sizerow = currentNumChild;
            videoGrid.style.gridTemplateColumns = `repeat(${sizecolumn}, minmax(30rem, 1fr))`;
            videoGrid.style.gridTemplateRows = `repeat(${sizerow}, minmax(30rem, ${MAX_HEIGHT / sizerow}px))`;
        }
    }
}

function appendUserClickVideoListener(){
    const classVideo = document.querySelectorAll('.video-div');
    classVideo.forEach(video => {
        // check if element already have listener or not?
        if (video.hasAttribute('listener')) return;
        video.setAttribute('listener', true);

        video.addEventListener('click', e => {
            const videoGrid = document.getElementById('video-grid');

            // toggle on-focus class
            videoGrid.classList.toggle('on-focus');
            videoGrid.style = '';

            // remove number user div
            if(videoGrid.contains(document.getElementById('number-user-div'))) videoGrid.removeChild(document.getElementById('number-user-div'));
            
            // usercanvas with e.target.id and class canvas
            if (video.id === 'myVideo-div') {
                document.getElementById('myCanvasDiv').classList.toggle('hide')
                if(window.innerWidth > 1000) document.getElementById('myCanvasDiv').style.gridRow = 'span 2';
                // hide every element except element that have id == myVideo-div
                let classVideo = document.querySelectorAll('.video-div');
                classVideo.forEach(video => {
                    if (video.id !== e.target.id) {
                        if (video.id == 'myVideo-div') return;
                        video.classList.toggle('hide');
                    }
                });
                if(videoGrid.classList.contains('on-focus') && window.innerWidth > 1000) addNumberUserDiv();
            }else{
                let usercanvas = document.querySelectorAll(`.canvas-div`);
                let focusCanvas = null;
                let focusVideo = null;
                usercanvas.forEach(canvas => {
                    if (canvas.id === `${video.childNodes[0].id}-canvas-div`) {
                        canvas.classList.toggle('hide');
                        focusCanvas = canvas;
                    }
                });
                let uservideo = document.querySelectorAll(`.video-div`);
                uservideo.forEach(U_video => {
                    if (video.id != `${U_video.childNodes[0].id}-div`) {
                        U_video.classList.toggle('hide');
                        console.log(U_video, U_video.classList)
                    }else{
                        focusVideo = video;
                    }
                });

                

                focusCanvas.parentNode.insertBefore(focusCanvas, focusCanvas.parentNode.firstChild);
                if(videoGrid.classList.contains('on-focus') && window.innerWidth > 1000) {
                    focusCanvas.style.gridRow = 'span 2';
                    addNumberUserDiv();
                }
            }

            let currentNumChild = videoGrid.childElementCount;

            // get child element count that is not display none
            for (let i = 0; i < videoGrid.childElementCount; i++) {
                if (videoGrid.children[i].classList.contains('hide')) {
                    currentNumChild--;
                }
            }

            changeGridSize();
            resetCanvasSize();
        });
    });

}

function addNumberUserDiv(){
    const div = document.createElement('div');
    div.classList.add('number-user-div');
    div.id = 'number-user-div';

    const p = document.createElement('p');
    console.log(Peers)
    let numberOfUsers = Object.keys(Peers).length;

    p.id = 'number-user';
    p.innerHTML = `${numberOfUsers} +`;
    div.appendChild(p);
    videoGrid.appendChild(div);
}

function updateUserNumber(){
    let numberOfUsers = Object.keys(Peers).length;
    if (!document.getElementById('number-user-div')) return;
    document.getElementById('number-user').innerHTML = `${numberOfUsers} +`;
}