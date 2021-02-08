$(document).ready(function() {
    let display = false
    $(`.cmt_btn`).click(function () {
        if (display===false) {
            $(this).next(`.comment-box`).show("slow");
            display=true
        } else {
            $(this).next(`.comment-box`).hide("slow");
            display=false
        }  
    });
    $(`.like-form`).submit(function (e){
        e.preventDefault()
        const post_id = $(this).attr('id')
        const url = $(this).attr('action')
        const likes = parseInt($.trim($(`.like-count${post_id}`).text()))
        let result
        
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken').val(),
                'post_id': post_id,
            },
            success: function(response) {
                if ( response.value === 'Unlike'){
                    $.trim($(`.icon${post_id}`).replaceWith($(`<i class="heart icon teal icon${post_id}"></i>`)))
                    result = likes - 1
                } else if(response.value === 'Like') {
                    $.trim($(`.icon${post_id}`).replaceWith($(`<i class="heart icon red icon${post_id}"></i>`)))
                    result = likes + 1
                }
                $.trim($(`.like-count${post_id}`).text(result))
            },
            error: function(response) {
                console.log('errorrrrr', response)
            }
        })
    })
})