/**
 *
 * @param response
 * @returns {Promise<{data: *, error: boolean, status}|*>}
 */
async function handleResponse(response) {
    if (response.status >= 200 && response.status < 400) {
        try {
            const data = await response.json()
            if (data.data) return data.data
            return data
        } catch (err) {
            return err
        }
    } else if (response.status >= 400 && response.status < 500) {
        const data = await response.json()
        let message = []
        if (data.message) message.push(data.message)
        if (data.errors) message.push(Object.values(data.errors))
        const id = crypto.randomUUID()
        document.body.insertAdjacentHTML('beforeend', `<span id="${id}" class="notify">${message.join("<br/>")}</span>`)
        const el = document.getElementById(id)
        setTimeout(() => {
            el.classList.add('active')
            setTimeout(() => {
                el.classList.remove('active')
                setTimeout(() => {
                    el.remove()
                }, 100)
            }, 3000)
        }, 100)
        return {data, error: true, status: response.status}
    } else alert('server error')
}

/**
 *
 * @param path
 * @param method
 * @param body
 * @returns {Promise<*|{data: *, error: boolean, status: *}|undefined>}
 */
export default async function $fetch(path, method = 'get', body = null) {
    const url = new URL('https://cqlgklbvubvw.buymysite.ru/api-of' + path);

    const headers = {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
        Accept: 'application/json',
    }
    if (!body || method === 'get') {
        url.search = new URLSearchParams(body ?? {}).toString()
        return await handleResponse(await fetch(url, {method, headers}))
    }
    return await handleResponse(await fetch(url, {method, headers, body}))
}