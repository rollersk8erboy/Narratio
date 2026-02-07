function getAlert(message) {
    Swal.fire({
        toast: true,
        timerProgressBar: true,
        showConfirmButton: false,
        timer: 2000,
        title: message,
        position: 'bottom-end',
        icon: 'info',
        background: 'rgb(34, 37, 41)',
        color: 'rgb(241, 241, 241)',
        width: '600px',
    })
}

function confirmDestroy(button) {
    const url = button.dataset.url;
    Swal.fire({
        showCancelButton: true,
        icon: 'info',
        title: '¿Quieres eliminar este elemento de manera permanente?',
        text: "Esta acción no se puede deshacer.",
        confirmButtonColor: 'rgb(203, 68, 74)',
        color: 'rgb(241, 241, 241)',
        background: 'rgb(34, 37, 41)',
        confirmButtonText: 'Eliminar',
        cancelButtonText: 'Cancelar',
        width: '600px',
    }).then((result) => {
        if (result.isConfirmed) {
            var form = document.createElement('form');
            form.method = 'POST';
            form.action = url;
            document.body.appendChild(form);
            form.submit();
        }
    });
}
