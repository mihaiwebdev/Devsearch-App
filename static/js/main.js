
// Pagination with search query
const searchForm = document.querySelector('#searchForm')
let pageLinks = [...document.getElementsByClassName('page-link')]

if (searchForm) {
pageLinks.map(link => link.addEventListener('click', (e) => {
    e.preventDefault()

    let page = link.dataset.page

    searchForm.innerHTML += `<input value=${page} name="page" hidden />`

    searchForm.submit()
}))
}

