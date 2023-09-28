// On page load or when changing themes, best to add inline in `head` to avoid FOUC
if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark')
    $('#theme-dark').show()
    $('#theme-light').hide()

} else {
    document.documentElement.classList.remove('dark')
    $('#theme-light').show()
    $('#theme-dark').hide()


}

$('#theme-btn').click(function (e) {
    if (localStorage.theme == 'light') {
        document.documentElement.classList.add('dark')
        localStorage.theme = 'dark'
        $('#theme-dark').show()
        $('#theme-light').hide()

    } else {
        document.documentElement.classList.remove('dark')

        localStorage.theme = 'light'
        $('#theme-light').show()
        $('#theme-dark').hide()

    }

});




$(window).on("load", function (e) {


    $('.modal-btn').click(function () {
        $('#content').addClass('blurPage');
    });

    $('.modal-close').click(function () {
        $('#content').removeClass('blurPage');
    })

});



const modals = $('.blur-modal')

window.addEventListener("click", (event) => {
    $.each(modals, function (indexInArray, modal) {
        if (event.target === modal) {
            $('#content').removeClass('blurPage');
        }
    });
});
$(document).keyup(function (e) {
    if (e.key === "Escape") { // escape key maps to keycode `27`
        $('#content').removeClass('blurPage');

    }
});



//topic btn
$(document).ready(function () {
    $("#topics a").each(function () {
        var url_string = window.location.href;
        var url = new URL(url_string);
        var q = url.searchParams.get("q");

        if ($(this).attr('data-q') == q) {
            $(this).find('div.the-btn').removeClass('trans-btn');
            $(this).find('div.the-btn').addClass('trans-btn-full');
        } else if ($(this).attr('data-q') == 'home' && q == null) {
            $(this).find('div.the-btn').removeClass('trans-btn');
            $(this).find('div.the-btn').addClass('trans-btn-full');
        }

    });
});



// // topic choose btn in roomupdate

var demoInput = document.getElementById('topic-choose');
if (demoInput != null) {
    let current_topic = $('#current_topic').data('topic')
    demoInput.value = current_topic
    demoInput.onfocus = function () { demoInput.value = ''; };

}




// hiding alerts and stuff


$('.hide-alert').click(function () {
    $(this).hide()
})





// fadeout these elemtns

function removeFadeOut() {
    $('div[name=fadeOut]').delay(12000).fadeOut('fast');
}

setInterval(removeFadeOut, 1000);

//pasword

$('.js-password-toggle').click(function (e) {


    let pwd = $(this).parent('div').find('input')

    let passwordLabel = $(this).find('label')

    if ($(pwd).attr('type') === 'password') {
        $(pwd).attr('type', 'text')
        passwordLabel.html('hide')
    } else {
        $(pwd).attr('type', 'password')
        passwordLabel.html('show')

    }

    pwd.focus()
})

//on page load 
if (!$('#current_user').data('user')) {
    if (localStorage.getItem('modal') === 'shown') {

    } else {
        window.addEventListener("load", showModal);
        localStorage.setItem('modal', 'shown')
    }



    // Function to show the modal

    function showModal() {
        $('#show-signup-modal').click()
    }


    // Show the modal when the page loads

    // Set an interval to show the modal every 5 minutes (300,000 milliseconds)
    setInterval(showModal, 300000);
}


