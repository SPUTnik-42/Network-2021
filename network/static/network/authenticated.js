document.addEventListener('DOMContentLoaded', function() {
    // Init posts
    document.querySelectorAll("div.post").forEach((postNode) => {
        
        editPostControl(postNode);
 
    });

    

    window.addEventListener("resize", () => {
        document.querySelectorAll("div.post").forEach((postNode) => {
            showMoreButtonControl(postNode);
        })

    })
});