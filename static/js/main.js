
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


// Remove Project Tags

{/* <script>
    let tags = document.getElementsByClassName('project-tag')

    for ( let i = 0; i < tags.length; i++) {

        tags[i].addEventListener('click', (e) => {
            e.preventDefault()

            let tagId = e.target.dataset.tag
            let projectId = e.target.dataset.project
            

            fetch('http://127.0.0.1:8000/api/remove-tag/', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({'project': projectId, 'tag': tagId})

            })
            .then(res => res.json())
            .then(data => {
                e.target.remove()
            })
        })
    }

</script> */}