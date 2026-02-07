function resizeArea(textarea) {
    textarea.style.height = 58 + 'px';
    textarea.style.height = textarea.scrollHeight + 'px';
}

function toggleInputType() {
    const mycodeid = document.getElementById('mycodeid');
    const myfiletype = document.getElementById('myfiletype');
    const description = document.getElementById('description');
    const audio = document.getElementById('audio');
    const mydescription = document.getElementById('mydescription');
    const myaudio = document.getElementById('myaudio');

    if (myfiletype.value === 'txt') {
        description.classList.remove('d-none');
        resizeArea(mydescription);
        audio.classList.add('d-none');
        myaudio.required = false;
        mydescription.required = true;
    } else {
        audio.classList.remove('d-none');
        description.classList.add('d-none');
        mydescription.value = null;
        mydescription.required = false;
        if (mycodeid == null) {
            myaudio.required = true;
        }
    }
}

document.addEventListener('DOMContentLoaded', function () {
    toggleInputType();
});

document.addEventListener("DOMContentLoaded", function () {
    const textareas = document.querySelectorAll("textarea[oninput]");
    textareas.forEach(textarea => resizeArea(textarea));
});