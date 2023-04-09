function fetch(method, data, success, error) {
    $.ajax({
        url: `/api/${method}`, 
        method: 'get',
        dataType: 'json',
        data: data,
        success: success,
        error: error
    });
}

function apiPost(method, data, success, error) {
    $.ajax({
        url: `/api/${method}`, 
        method: 'post',
        dataType: 'json',
        data: data,
        success: success,
        error: error
    });
}