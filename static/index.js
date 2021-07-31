var popoverTriggerList = [].slice.call(
  document.querySelectorAll('[data-bs-toggle="popover"]')
);
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl);
});
const editor = document.querySelectorAll(".editor");
editor.forEach((element) => {
  element.addEventListener("paste", function (e) {
    e.preventDefault();
    var text = (e.originalEvent || e).clipboardData.getData("text/plain");
    document.execCommand("insertHTML", false, text);
  });
});

http = axios.create({
  baseURL: document.location.origin + "/api",
  headers: {
    "content-type": "multipart/form-data",
    "X-CSRFToken": getCookie("csrftoken"),
  },
});
async function getAll() {
  try {
    const response = await http.get("/posts/");
    return response.data;
  } catch (error) {
    console.log(error);
  }
}

async function get(id) {
  const response = await http.get("/posts/" + id);
  return response.data;
}

async function put(data, id) {
  try {
    const response = await http.put("/posts/" + id, data, {
      headers: {
        "content-type": "multipart/form-data",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    });
    console.log(response);
  } catch (error) {
    console.log(error);
  }
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function writePage() {
  const ID = document.URL.split("write/")[1];
  const image_uploadBtn = document.getElementById("image-upload");
  const imgInput = document.getElementById("img-uploadInput");
  const uploadImg = document.getElementById("uploadedImg");
  const publishBtn = document.getElementById("publish-btn");

  imgInput.addEventListener("change", function () {
    if (this.files && this.files[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
        uploadImg.setAttribute("src", e.target.result);
        image_uploadBtn.parentElement.setAttribute("style", "min-height:0;");
        image_uploadBtn.setAttribute("style", "opacity:.9;");
        uploadImg.setAttribute("style", "display:inline;max-height:500px;");
      };
      reader.readAsDataURL(this.files[0]);
      let form_data = new FormData();
      form_data.append("tumbnail", this.files[0]);
      put(form_data, ID);
    }
  });

  publishBtn.addEventListener("click", function () {
    let form_data = new FormData();
    form_data.append("content", postContent.innerHTML);
    form_data.append("title", postTitle.innerText);
    put(form_data, ID);
  });
  postTitle = document.getElementById("create-post-title");
  var timeout = null;
  function editableMaxLengthValidator(element, max_length) {
    const validator = () => {
      return element.innerText.length > max_length;
    };
    element.addEventListener("keyup", function (event) {
      clearTimeout(timeout);
      timeout = setTimeout(function () {
        if (!validator(event)) {
          let form_data = new FormData();
          form_data.append("title", postTitle.innerText);
          put(form_data, ID);
        }
      }, 500);
    });
    element.addEventListener("keydown", (event) => {
      if (validator(event)) {
        element.innerHTML = element.innerText.substring(0, max_length);
        if (event.which == 8) return;
        event.preventDefault();
      }
    });
  }

  editableMaxLengthValidator(postTitle, 40);

  postTitle.addEventListener("keydown", function (event) {
    if (event.which == 13) {
      event.preventDefault();
    }
  });

  var postContent = document.getElementById("create-post-content");
  var Ctimeout = null;
  postContent.addEventListener("keyup", function () {
    clearTimeout(Ctimeout);
    Ctimeout = setTimeout(function () {
      let form_data = new FormData();
      data = postContent.innerHTML;
      form_data.append("content", data);
      console.log(form_data.data);
      put(form_data, ID);
    }, 500);
  });

  get(ID).then((elem) => {
    postContent.innerHTML = elem.content;
  });
}

//====================================================profile-Edit-Page==============================================
function profileEditPage() {
  const ID = document.URL.split("profile-edit/")[1];

  const profilePicture = document.querySelectorAll(".profile-picture");
  const pictureInput = document.querySelector("#propicinput");
  const pictureUpload = document.querySelector("#propicupload");
  const aboutSubmit = document.getElementById("about-submit");
  const aboutField = document.getElementById("about-user");
  async function postProfileImage(data) {
    const response = await http.put("/userdetails/", data, {
      headers: {
        "content-type": "multipart/form-data",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    });
    return response.data;
  }
  pictureInput.addEventListener("change", function () {
    if (this.files && this.files[0]) {
      const reader = new FileReader();
      reader.addEventListener("load", function (event) {
        profilePicture.forEach((elem) => {
          elem.setAttribute(
            "style",
            `background-image:url('${event.target.result}');`
          );
        });
      });
      reader.readAsDataURL(this.files[0]);
      let form_data = new FormData();
      form_data.append("profile_img", this.files[0]);
      postProfileImage(form_data);
    }
  });
  aboutSubmit.addEventListener("click", async function () {
    if (aboutField && aboutField.innerText.trim() != "") {
      let form_data = new FormData();
      form_data.append("about", aboutField.innerText);
      await postProfileImage(form_data);
    }
  });
}

function postPage() {
  const ID = document.URL.split("post/")[1];
  const upvoteBtn = document.getElementById("upvote-btn");
  const downvoteBtn = document.getElementById("downvote-btn");
  const votes = document.getElementById("votes");
  const postDeleteBtn = document.getElementById("delete-post");

  async function getVote(id) {
    const response = await http.get("/vote/" + id);
    return response.data;
  }

  async function getVoteCount() {
    const response = await http.get("/vote/" + ID + "/");
    console.log(response.data);
    return response.data;
  }
  async function postVote(data) {
    try {
      const response = await http.post("/votes/", data, {
        headers: {
          "content-type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
      });
    } catch (error) {
      window.location.href = "/login";
    }
  }

  async function putVote(data, id) {
    try {
      const response = await http.put("/vote/" + id + "/", data, {
        headers: {
          "content-type": "multipart/form-data",
          "X-CSRFToken": getCookie("csrftoken"),
        },
      });
      console.log(response);
    } catch (error) {
      console.log(error);
    }
  }
  async function validateVote() {
    const data = await getVote(ID);

    getVoteCount().then((e) => (votes.innerText = e.votes_count));
    if (data.vote === "UPVOTE") {
      upvoteBtn.setAttribute("style", "color:blue");
      downvoteBtn.setAttribute("style", "color:black");
    } else if (data.vote === "DOWNVOTE") {
      upvoteBtn.setAttribute("style", "color:black");
      downvoteBtn.setAttribute("style", "color:blue");
    } else {
      upvoteBtn.setAttribute("style", "color:black");
      downvoteBtn.setAttribute("style", "color:black");
    }
  }
  validateVote();

  upvoteBtn.addEventListener("click", async function () {
    const data = await getVote(ID);
    if (data && data.vote === "UPVOTE") {
      await http.delete("vote/" + ID + "/");
    } else if (data && data.vote === "DOWNVOTE") {
      let form_data = new FormData();
      form_data.append("vote", "UPVOTE");
      await putVote(form_data, ID);
    } else {
      form_data = {
        vote: "UPVOTE",
        post: ID,
      };
      await postVote(form_data);
    }

    await validateVote();
  });
  downvoteBtn.addEventListener("click", async function () {
    const data = await getVote(ID);
    if (data && data.vote === "DOWNVOTE") {
      await http.delete("vote/" + ID + "/");
    } else if (data && data.vote === "UPVOTE") {
      let form_data = new FormData();
      form_data.append("vote", "DOWNVOTE");
      await putVote(form_data, ID);
    } else {
      form_data = {
        vote: "DOWNVOTE",
        post: ID,
      };
      await postVote(form_data);
    }

    await validateVote();
  });
  async function postReview(data) {
    try {
      const response = await http.post("/reviews/" + ID + "/", data, {
        headers: {
          "content-type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
      });

      return response.data;
    } catch (error) {
      return false;
    }
  }

  postDeleteBtn.addEventListener("click", async function () {
    await http.delete("/posts/" + ID + "/");
    window.location.href = document.location.origin;
  });
  const commentSubmit = document.getElementById("comment-submit");
  const commentCancel = document.getElementById("comment-cancel");
  const commentBody = document.getElementById("add-comment");
  const commentBox = document.getElementById("comment");
  commentSubmit.addEventListener("click", async function () {
    if (commentBody && commentBody.innerText.trim() != "") {
      data = {
        body: commentBody.innerText,
        post: ID,
      };
      const check = await postReview(data);
      if (check) {
        window.location.reload();
      } else {
        commentBox.setAttribute("style", "border: 3px solid red;");
        setTimeout(function () {
          commentBox.setAttribute("style", "border: 0");
        }, 1000);
      }
    }
  });

  commentCancel.addEventListener("click", function () {
    if (commentBody) {
      commentBody.innerText = "";
    }
  });
}
window.addEventListener("load", function () {
  if (this.document.title === "write") {
    writePage();
  } else if (this.document.title === "profile-edit") {
    profileEditPage();
  } else if (this.document.title === "post") {
    postPage();
  }
});
