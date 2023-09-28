$('.delete-btn').click(function (e) {
    let room_id = $(this).data('id')
    let room_name = $(this).data('name')
    $('#room-name').text(room_name)

    $('#confirm-delete-btn').data('id', room_id)
});

$('#confirm-delete-btn').click(function (e) {
    let room_id = $(this).data('id')
    let user = $('#current_user').data('user')
    let room_name = $('#room-name').text();

    token = $("#change_password-form").find('input[name=csrfmiddlewaretoken]').val()

    $.ajax({
        data: {
            user: user,
            room_id: room_id,
            csrfmiddlewaretoken: window.CSRF_TOKEN
        },
        type: 'POST',
        url: '/delete-room'
    })
        .done(function (data) {
            if (data.success) {
                $(`div[data-id=${room_id}]`).remove()
                $('#success').show()
                $('#mysuccess').text(`${room_name} room Removed`)


            }
        })

});


//filter on change

$('#dropdownRadio input').change(function (e) {
    e.preventDefault();
    let filter_value = $('input[name="filter"]:checked').val()

    if (filter_value === 'private') {
        $('#dropdownRadioButton span').text("Private Rooms")
        $('.rooms').hide()
        $('.locked').closest('.rooms').fadeIn();

    } else if (filter_value === 'all') {
        $('#dropdownRadioButton span').text("All Rooms")
        $('.locked').closest('.rooms').fadeOut();
        $('.rooms').fadeIn()

    }


});


//pagess
nextPage = $('#nextPage')
previousPage = $('#previousPage')

var url_string = window.location.href;
var url = new URL(url_string);
var page = parseInt(url.searchParams.get("page"));

let page_param;

if (!page) {
    page_param = false
    previousPage.hide()
    page = 1
}


let a = 0;
let first_link;
let first_no;
let final_no;

$('#btn-numbers a').each(function (index, element) {
    let link = $(this)

    if (a < 1) {
        link.text(page)
        link.attr('href', window.location.href);

        first_link = link
        first_no = parseInt(first_link.text())
    }
    else {
        first_no += 1

        if (first_no <= last_page) {
            final_no = first_no
            link.text(first_no)
            var url = new URL(window.location.href);
            if (page_param) {
                url.searchParams.append('page', first_no);

            } else {
                url.searchParams.set('page', first_no);

            }

            link.attr('href', url);
        }
        else {
            link.hide()
        }
    }
    a += 1
});

if (page < last_page && final_no != last_page) {
    nextPage.show()
}
else {
    nextPage.hide()
}

var url = new URL(window.location.href);
if (page_param) {
    url.searchParams.append('page', page + 1);

} else {
    url.searchParams.set('page', page + 1);
}
nextPage.attr('href', url)



if (page > 1) {
    var url = new URL(window.location.href);
    if (page_param) {
        url.searchParams.append('page', page - 1);

    } else {
        url.searchParams.set('page', page - 1);
    }
    previousPage.attr('href', url)
} else {
    previousPage.hide()
}


//filter

let recent = $('#recent')
let popular = $('#popular')

let currentUrl = new URL(window.location.href);

if (!currentUrl.searchParams.get("filter")) {
    currentUrl.searchParams.append("filter", "popular")
    popular.attr('href', currentUrl)

    currentUrl.searchParams.delete("filter")

    currentUrl.searchParams.append("filter", "recent")
    recent.attr('href', currentUrl)

} else {
    currentUrl.searchParams.set("filter", "popular")
    popular.attr('href', currentUrl)

    currentUrl.searchParams.delete("filter")

    currentUrl.searchParams.set("filter", "recent")
    recent.attr('href', currentUrl)

}
