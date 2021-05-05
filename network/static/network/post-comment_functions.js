function showMoreButtonControl(node) {
    let content = node.querySelector(".content")
    let showMore;
    if (content.classList.contains("post-content")){
        showMore = content.nextElementSibling;
    }
    else {
        showMore = content.parentElement.nextElementSibling;
    }

    let isOverflowing = (content.clientWidth < content.scrollWidth)
                        || (content.clientHeight < content.scrollHeight); 

    // Text overflowing -> show show-more button and handle click event
    if (isOverflowing) {
        showMore.classList.remove("hidden")

        showMore.onclick = () => {
            // Make post content short or full height
            content.classList.remove("short");
            showMore.classList.add("hidden")
        }
    }
    // Text not overflowing -> hide show-more button
    else {
        showMore.classList.add("hidden")
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}