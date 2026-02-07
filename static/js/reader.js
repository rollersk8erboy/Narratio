const audio = new Audio();

function launchReader() {
    const qrBoxSize = Math.min(window.innerWidth * 0.8, 300);
    const html5QrcodeScanner = new Html5Qrcode("reader");
    const config = {
        fps: 30,
        qrbox: { width: qrBoxSize, height: qrBoxSize },
        videoConstraints: {
            facingMode: "environment",
            width: { min: 1280, ideal: 1920, max: 3840 },
            height: { min: 720, ideal: 1080, max: 2160 },
            focusMode: "continuous"
        }
    };
    html5QrcodeScanner.start(
        { facingMode: "environment" },
        config,
        onScanSuccess
    ).catch(e => console.error(e));
}

function onScanSuccess(decodedText) {
    if (audio.paused) {
        audio.src = '/static/mp3.nosync/' + decodedText + '.mp3';
        audio.load();
        audio.play().catch(e => console.error(e));
    }
}