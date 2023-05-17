function err(message) {
    ElMessage.error(message)
}

function myFetch(input, init) {
    return new Promise((resolve, reject) => {
        fetch(input, init).then(res => {
            json = resolve(res.json())
            if (json.code != 0) {
                err(json.message)
                reject(new Error(json.message))
            } else {
                resolve(json)
            }
        }).catch(err => {
            reject(err)
        })
    })
}

// export async function fetchDocList() {
//     return new Promise((resolve, reject) => {
//         myFetch("/api/my_docs").then(res => resolve(res)).catch(e => reject(e))
//     })
// }
export async function fetchDocList(user) {
    return new Promise((resolve, reject) => {
        myFetch("/api/my_docs", {
            method: "POST",
            body: JSON.stringify({user: user}),
            headers: {
                "Content-Type": "application/json",
            }
        }).then(res => resolve(res)).catch(e => reject(e))
    })
}

export async function fetchQuery(doc_id, query, user) {
    return new Promise((resolve, reject) => {
        myFetch("/api/ask/" + doc_id + "?question=" + query + "&user=" + JSON.stringify(user)).then(res => resolve(res)).catch(e => reject(e))
    })
}

export async function fetchMsg(doc_id) {
    return new Promise((resolve, reject) => {
        myFetch("/api/msg/" + doc_id).then(res => resolve(res)).catch(e => reject(e))
    })
}

export async function fetchDelDoc(doc_id) {
    return new Promise((resolve, reject) => {
        myFetch("/api/del/" + doc_id, {method: "DELETE"}).then(res => resolve(res)).catch(e => reject(e))
    })
}

export async function addAddLink(link, user) {
    return new Promise((resolve, reject) => {
        myFetch("/api/add_link", {
            method: "POST",
            body: JSON.stringify({link: link, user: user}),
            headers: {
                "Content-Type": "application/json",
            }
        }).then(res => resolve(res)).catch(e => reject(e))
    })
}

export async function addApikey(api_key, user) {
    return new Promise((resolve, reject) => {
        myFetch("/api/add_apikey", {
            method: "POST",
            body: JSON.stringify({apikey: api_key, user: user}),
            headers: {
                "Content-Type": "application/json",
            }
        }).then(res => resolve(res)).catch(e => reject(e))
    })
}


// export async function fetchApikey() {
//     return new Promise((resolve, reject) => {
//         myFetch("/api/my_apikey").then(res => resolve(res)).catch(e => reject(e))
//     })
// }
export async function fetchApikey(user) {
    return new Promise((resolve, reject) => {
        myFetch("/api/my_apikey", {
            method: "POST",
            body: JSON.stringify({user: user}),
            headers: {
                "Content-Type": "application/json",
            }
        }).then(res => resolve(res)).catch(e => reject(e))
    })
}


function apiUrl() {
    return 'http://localhost:8001/';
}

export function postApi(pathToResource, data) {
    // return fetch(apiUrl() + pathToResource, {
    //   method: 'POST',
    //   mode: 'cors',
    //   body: new URLSearchParams(data),
    // });
    return fetch("/api/" + pathToResource, {
        method: "POST",
        body: new URLSearchParams(data),
        // headers: {
        //     "Content-Type": "application/json",
        // }
    })
}

