$(function () {
    // Every time the page changes notify background.js to store the new page
    chrome.extension.sendMessage('new page');
});