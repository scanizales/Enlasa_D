    const inputSearch = document.querySelector('input[ name = "buscar"]');
    const tableInsurance = document.querySelector('table');
    inputSearch.addEventListener('input', searchInsurance);
    
    function searchInsurance(){
        const textSearch = inputSearch.value.trim();
        const tableRows = tableInsurance.querySelectorAll('tbody tr');
        tableRows.forEach( row => {
            const nameClient = row.cells[0].textContent.toLowerCase();
            if (nameClient.startsWith(textSearch.toLowerCase())){
                row.style.display = "";
            }else{
                row.style.display = 'none'
            }
        });
    }