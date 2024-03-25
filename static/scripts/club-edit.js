var clubId = "{{ club_id }}";
$(document).ready(function(){
$('#uploadImage').submit(function(event){
    if ($('#uploadFile').val()){
        event.preventDefault();

        var formData = new FormData(this);
        formData.append('club_id', clubId);

        $('#loader-icon').show();
        $('#targetLayer').hide();

        $.ajax({
            url: '/upload/'+clubId,  // Replace with the actual URL for your upload endpoint
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            beforeSend: function(){
                $('.progress-bar').width('50%');
            },
            xhr: function(){
                var xhr = $.ajaxSettings.xhr();
                xhr.upload.onprogress = function(event) {
                    if (event.lengthComputable) {
                        var percentageComplete = (event.loaded / event.total) * 100;
                        $('.progress-bar').animate({
                            width: percentageComplete + '%'
                        }, {
                            duration: 1000
                        });
                    }
                };
                return xhr;
            },
            success: function(data){
                $('#loader-icon').hide();
                $('#targetLayer').show();
                $('#targetLayer').append(data.htmlresponse);
            }
        });
    }
    return false;
});
});
function add_leadership() {
    var leaderRole = $('#leader-role').val();
    var leaderName = $('#leader-name').val();
    var iconName = document.getElementById("icons").value;
    console.log({leader_role: leaderRole, leader_name: leaderName, club_id: clubId})
    $.ajax({
        url: '/add_leadership',
        type: 'GET',
        data: {leader_role: leaderRole, leader_name: leaderName, club_id: clubId},
        success: function(response) {
            window.location.reload(true);
        },
        error: function(error) {
            console.log(error);
        }
    });
}
function add_social() {
    var contactInfo = $('#contact-info').val();
    var iconName = document.getElementById("icons").value;
    $.ajax({
        url: '/add_social',
        type: 'GET',
        data: {contact_info: contactInfo, icon_name: iconName, club_id: clubId},
        success: function(response) {
            location.reload();
        },
        error: function(error) {
            console.log(error);
        }
    });
}
function delete_social(socialIndex) {
    $.ajax({
        url: '/delete_social',
        type: 'GET',
        data: {social_index: socialIndex, club_id: clubId},
        success: function(response) {
            location.reload();
        },
        error: function(error) {
            location.reload();
        }
    });
}
function delete_leadership(leaderIndex) {
    $.ajax({
        url: '/delete_leadership',
        type: 'GET',
        data: {leader_index: leaderIndex, club_id: clubId},
        success: function(response) {
            location.reload();
        },
        error: function(error) {
            console.log(error);
        }
    });
}
function update_all() {
var description = $('#description').val();
var name = $('#club-name').val();
var new_meeting = $('#meeting-dates').val();
var club_slogan  = $('#club-slogan').val();
console.log(name)
var regex = /[!@#$%^&*()_+\-=\[\]{};':"\|,.<>\/?]+/g
var new_club_id = name.replace(regex, '').replace(/[_\s]/g, '-');
    $.ajax({
        url: '/update_all',
        type: 'GET',
        data: {description:description,club_name:name,meeting: new_meeting,club_id: clubId,club_slogan:club_slogan},
        success: function(response) {
        if(name === ""){
            window.location.replace("/view/"+clubId);
        }
        else{
            window.location.replace("/view/"+new_club_id);
        }
        },
        error: function(error) {
            console.log(error);
        }
    });
}