    const inputSearch = document.querySelector('input[ name = "buscar"]');
    const tableInsurance = document.querySelector('table');
    const countElement = document.getElementById('count');
    inputSearch.addEventListener('input', searchInsurance);
    const clear = document.getElementById('button-color-other')
    clear.addEventListener('click', clearFilter)
    
    function searchInsurance(){
        const textSearch = inputSearch.value.trim();
        const tableRows = tableInsurance.querySelectorAll('tbody tr');
        let count = 0;
        tableRows.forEach( row => {
            const nameClient = row.cells[0].textContent.toLowerCase();
            if (nameClient.startsWith(textSearch.toLowerCase())){
                row.style.display = "";
                count++;
            }else{
                row.style.display = 'none'
            }
        });
        countElement.textContent = count;
    }
    function clearFilter(){
        tableRows.forEach(row => {
            row.style.display = ""
        });
    }




