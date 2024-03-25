

function show_alert(message, _type){
    const element = document.getElementById("show_alert")

    if (_type === "error"){
        element.innerHTML = `
        <div class="alert alert-danger" role="alert"><span class="fe fe-minus-circle fe-16 mr-2"></span> ${message}</div>
        `
    } else if (_type === "success"){
        element.innerHTML = `
        <div class="alert alert-success" role="alert"><span class="fe fe-check fe-16 mr-2"></span> ${message}</div>
        `
    } else if (_type === "info"){
        element.innerHTML = `
        <div class="alert alert-info" role="alert"><span class="fe fe-info fe-16 mr-2"></span> ${message}</div>
        `
    }
}

function close_button(element_id){
    const button = document.getElementById(element_id)

    button.disabled = true
    button.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp; الرجاء الأنتظار`
}

function unclose_button(element_id, message){
    const button = document.getElementById(element_id)
    button.disabled = false
    button.innerHTML = message
}