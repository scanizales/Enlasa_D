
const modal = document.getElementById('modal');
const abrirModal = document.getElementById('abrir-modal');
const cerrrarModal = document.getElementById('cerrar-modal');
const cerrrarModal2 = document.getElementById('cerrar-modal2');

abrirModal.addEventListener('click',() =>{
    modal.classList.add('show');
});
cerrrarModal.addEventListener('click', () =>{
    modal.classList.remove('show');
})
cerrrarModal2.addEventListener('click', () =>{
    modal.classList.remove('show');
})