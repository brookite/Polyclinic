function fetch(method, data, success, error, async=true) {
    $.ajax({
        url: `/api/${method}`, 
        method: 'get',
        dataType: 'json',
        data: data,
        success: success,
        error: error,
        async: async
    });
}

function apiPost(method, data, success, error, async=true) {
    $.ajax({
        url: `/api/${method}`, 
        method: 'post',
        dataType: 'json',
        data: data,
        success: success,
        error: error,
        async: async
    });
}