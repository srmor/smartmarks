var baseUrl = 'http://www.smartmarks.co';

var SmartMarks = {
    signIn: function() {
        $.ajax({
            type: 'POST',
            url: baseUrl+'/api/sign-in',
            data: {
                'email': $('#sign-in .email').val(),
                'password': $('#sign-in .password').val()
            },
            dataType: 'json',
            statusCode: {
                200: function(data) {
                    // store API key in local storage
                    chrome.storage.local.set({'smartmarks': data.responseText});
                    SmartMarks.showCreateBookmark();
                },
                401: function(data) {
                    $('#sign-in h4').after('<div class="alert alert-error">Sorry, those are not valid credentials</div>');
                    $('#sign-in .btn').removeAttr('disabled');
                }
            }
        });
    },

    createBookmark: function(tab) {
        favicon = tab[0].favIconUrl;
        title = $('#bookmark .title').val();
        url = $('#bookmark .url').val();

        // if the page does not have a favicon then set favicon to an empty string
        if (!favicon) {
            favicon = " ";
        }

        $.ajax({
            type: 'POST',
            url: baseUrl+'/api/create',
            data: {
                'title': title,
                'url': url,
                'favicon': favicon,
                'type': 'bookmark',
                'api_key': apiKey
            },
            dataType: 'json',
            statusCode: {
                200: function(data) {
                    $('#bookmark .btn').hide();
                    $('#bookmark .btn').after('<span class="bookmark-added pull-right btn btn-success" disabled="disabled">Bookmark Added</span>');
                }
            }
        });
    },

    showSignIn: function() {
        $('#sign-in').show();

        $('#sign-in .btn').click(function() {
            $(this).attr("disabled", "disabled");

            SmartMarks.signIn();
        });
    },

    showCreateBookmark: function() {
        chrome.tabs.query({active : true, currentWindow: true}, function (tab) {
            $('#sign-in').hide();
            $('#bookmark').show();
            $('#bookmark .title').val(tab[0].title);
            $('#bookmark .url').val(tab[0].url);
            $('#bookmark .favicon').val(tab[0].favIconUrl);

            $('#bookmark .btn').click(function() {
                $(this).attr("disabled", "disabled");
                SmartMarks.createBookmark(tab);
            });
        });
    }
};

$(function () {
    chrome.storage.local.get('smartmarks', function(items) {
        apiKey = items.smartmarks;
        if (apiKey) {
            SmartMarks.showCreateBookmark();
        } else {
            SmartMarks.showSignIn();
        }
    });

});