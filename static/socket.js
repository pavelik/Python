const socket = io.connect('https://flask-chat-app.herokuapp.com/');

const form = $('form').on('submit', (e) => {
    e.preventDefault();

    const today = new Date();
    const dateString =
    ("0" + today.getDate()).slice(-2) + "." +
    ("0" + (today.getMonth() + 1)).slice(-2) + "." +
    today.getFullYear() + " " +
    ("0" + today.getHours()).slice(-2) + ":" +
    ("0" + today.getMinutes()).slice(-2) + ":" +
    ("0" + today.getSeconds()).slice(-2);
    
    const nickname = $('#nickname').val();
    const message = $('#message').val();
    
    socket.emit('message', {
        nickname: nickname,
        message: message,
        date: dateString
    });

    $('#message').val('').focus();
});

socket.on('response', (msg) => {
    $('#messages').append(
        `<label class="author">${msg.nickname}</label>
            <div class="alert alert-dark" role="alert">
                ${msg.message}
                <div class="text-muted text-right">
                    <small>${msg.date}</small>
                </div>
            </div>`
    );

    $("html, body").animate({
        scrollTop: ($(document).height())
    }, 1000);

    $('#message').focus();
});
