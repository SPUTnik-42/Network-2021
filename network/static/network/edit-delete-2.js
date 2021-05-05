// Controls asynchronous editing of a post
function editPostControl(postNode) {
    let modalDialog = postNode.querySelector(".edit-modal");

    if (modalDialog !== null) {
        $(modalDialog).on('show.bs.modal', () => {
            // Get save button and modal body
            let saveButton = modalDialog.querySelector(".modal-footer > .btn-primary");
            let modalBody = modalDialog.querySelector(".modal-body");

            // Get post id
            const postID = postNode.id.substr(5);
            

            // Get content of post to be edited
            let contentNode = postNode.querySelector("div.post-content");
            const contentInnerText = contentNode.textContent.trim();
            
            
            // Populate content with form to fill
            modalBody.innerHTML = `<textarea class="new-content form-control">${contentInnerText}</textarea>`;

            // After save - update
            saveButton.addEventListener("click", () => {
                // Get content to submit
                const submittedContent = modalBody.querySelector("textarea.new-content").value.trim();
                
                let csrftoken = getCookie('csrftoken');

                // Hide modal
                $(modalDialog).modal('hide');

                // Send PUT request
                fetch("/post/post", {
                    method: "PUT",
                    body: JSON.stringify({
                        id: postID,
                        content: submittedContent,
                    }),
                    headers: {"X-CSRFToken": csrftoken}
                })
                .then(async(response) => {
                    // if success - update post's content
                    if (response.status === 201) {
                        showMoreButtonControl(postNode);
                        contentNode.innerHTML = submittedContent;
                        console.log(`post id: ${postID} edited successfully`);
                    }
                    // if error - show alert and reload the page
                    else {
                        let response_body = await response.json();

                        throw new Error(response_body.error);                        
                    }
                })
                .catch(error => {
                    alert(error);
                    location.reload();
                })
            });
        });
    }
}