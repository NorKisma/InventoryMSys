


const sidebarToggle = document.querySelector("#sidebar-toggle");
sidebarToggle.addEventListener("click",function(){
    document.querySelector("#sidebar").classList.toggle("collapsed");
});

document.querySelector(".theme-toggle").addEventListener("click",() => {
    toggleLocalStorage();
    toggleRootClass();
});

function toggleRootClass(){
    const current = document.documentElement.getAttribute('data-bs-theme');
    const inverted = current == 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-bs-theme',inverted);
}

function toggleLocalStorage(){
    if(isLight()){
        localStorage.removeItem("light");
    }else{
        localStorage.setItem("light","set");
    }
}

function isLight(){
    return localStorage.getItem("light");
}

if(isLight()){
    toggleRootClass();}




    document.getElementById('searchInput').addEventListener('keyup', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = document.querySelectorAll('#searchTable tbody tr');
  
        rows.forEach(row => {
          const cells = row.querySelectorAll('td');
          let rowContainsTerm = false;
  
          cells.forEach(cell => {
            if (cell.textContent.toLowerCase().includes(searchTerm)) {
              rowContainsTerm = true;
            }
          });
  
          if (rowContainsTerm) {
            row.style.display = '';
          } else {
            row.style.display = 'none';
          }
        });
      });