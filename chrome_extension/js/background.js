var baseUrl = 'http://localhost:5000';

$(function () {
    chrome.extension.onMessage.addListener(
      function(request, sender, sendResponse) {

        chrome.storage.local.get('smartmarks', function(key) {
            apiKey = key.smartmarks;
            if (apiKey) {
                url = sender.tab.url;
                favicon = sender.tab.favIconUrl;
                title = sender.tab.title;

                // if the page does not have a favicon then set favicon to an empty string
                if (!favicon) {
                    favicon = " ";
                }

                // if the page is a smartmarks page do not save it.
                if (url.substring(0, 22) !== baseUrl+'/') {
                    $.ajax({
                        type: 'POST',
                        url: baseUrl+'/api/create',
                        data: {
                            'title': title,
                            'url': url,
                            'favicon': favicon,
                            'type': 'history',
                            'api_key': apiKey
                        },
                        dataType: 'json'
                    });
                }
            }
        });

      });
});