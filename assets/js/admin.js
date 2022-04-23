async function deleteTweeb() {
    const form = event.target.form
    const tweebId = form.tweeb_id.value

    const conn = await fetch(`/tweebs/${tweebId}/as-admin`, {
        method: "DELETE"
    })

    if (!conn.ok) {
        console.log(conn)
        return
    }

    // SUCCES
    form.remove()
}


async function loadMoreTweebs() {
    const btn = event.target

    const conn = await fetch(`/tweebs/in-chunks/${btn.dataset.chunk * 10}`,{
        method : "GET"
    })

    if (!conn.ok) {
        console.log(conn)
        return
    }

    if (conn.status == 204) {
        btn.remove()
        return
    }

    res = await conn.json()
    btn.dataset.chunk ++
    console.log(res.html)
    // if not loading max amount - remove btn 
    if (res.count < 10) btn.remove()

    document.querySelector(".tweebs").insertAdjacentHTML("beforeend", res.html)
}