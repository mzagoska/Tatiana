
var socket = io.connect('http://127.0.0.1:5000/chat');

socket.on("connect", function(){
                console.log("connected");
                socket.emit('joined', 'joined');
            });
socket.on("status", function(data){
                console.log(data.msg);
            });

socket.on('msg', function(data) {
    console.log("input message");
    mess = data.msg;
    setTimeout(function() {
        $('.message.loading').remove();
        $('<div class="message new"><figure class="avatar"><img src="https://png.pngtree.com/png-vector/20200618/ourlarge/pngtree-female-doctor-design-png-image_2257811.jpg" /></figure>' + mess + '</div>').appendTo($('.mCSB_container')).addClass('new');
        setDate();
        updateScrollbar();
        i++;
    }, 1000 + (Math.random() * 20) * 100);
    });

var constraints = { audio: true };

var k = 0;



      navigator.mediaDevices.getUserMedia(constraints).then(function(mediaStream) {

        var mediaRecorder = new MediaRecorder(mediaStream);
        mediaRecorder.onstart = function(e) {
            this.chunks = [];
        };
        mediaRecorder.ondataavailable = function(e) {
            this.chunks.push(e.data);
        };
        mediaRecorder.onstop = function(e) {
            var blob = new Blob(this.chunks, { 'type' : 'audio/x-wav; codecs=PCM_16' });//codecs=vorbis/opus
            socket.emit('radio', blob);
            console.log(type(blob));
            console.log("sent voice");
        };

        $('.message-submit_v').click(function() {
            mediaRecorder.start();
            $('<div class="message loading new"><figure class="avatar"><img src="https://png.pngtree.com/png-vector/20200618/ourlarge/pngtree-female-doctor-design-png-image_2257811.jpg"/></figure>Слушаю...<span></span></div>').appendTo($('.mCSB_container'));
            updateScrollbar();
        });

        $('.message-submit_v1').click(function() {

                mediaRecorder.stop();
                $('.message.loading').remove();

        });
      });




// When the client receives a voice message it will play the sound
socket.on('voice', function(arrayBuffer) {
    console.log("take voice");
    var blob = new Blob([arrayBuffer], { 'type' : 'audio/x-wav; codecs=PCM_16' });
    var audio = document.createElement('audio');
    audio.src = window.URL.createObjectURL(blob);
    audio.play();
});

var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(window).load(function() {
  if (i == 0) {
    $messages.mCustomScrollbar();
  setTimeout(function() {
    fakeMessage();
  }, 100);
  }
});

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

function setDate(){
  d = new Date()
  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
  }
}

function insertMessage() {
  msg = $('.message-input').val();
  if ($.trim(msg) == '') {
    return false;
  }
  socket.emit('text', msg);
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  $('.message-input').val(null);
  updateScrollbar();
  setTimeout(function() {
    trueMessage();
  }, 1000 + (Math.random() * 20) * 100);
}

$('.message-submit').click(function() {
  insertMessage();
});

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    insertMessage();
    return false;
  }
})

var Fake = [
  'Привет, я Таня. Чем могу быть полезна?'
]

function fakeMessage() {
  if ($('.message-input').val() != '') {
    return false;
  }
  $('<div class="message loading new"><figure class="avatar"><img src="https://png.pngtree.com/png-vector/20200618/ourlarge/pngtree-female-doctor-design-png-image_2257811.jpg" /></figure><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();

  setTimeout(function() {
    $('.message.loading').remove();
    $('<div class="message new"><figure class="avatar"><img src="https://png.pngtree.com/png-vector/20200618/ourlarge/pngtree-female-doctor-design-png-image_2257811.jpg" /></figure>' + Fake[i] + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    updateScrollbar();
    i++;
  }, 1000 + (Math.random() * 20) * 100);

}

function trueMessage() {
  $('<div class="message loading new"><figure class="avatar"><img src="https://png.pngtree.com/png-vector/20200618/ourlarge/pngtree-female-doctor-design-png-image_2257811.jpg" /></figure><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();
}