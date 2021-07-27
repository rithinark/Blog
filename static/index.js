var popoverTriggerList = [].slice.call(
  document.querySelectorAll('[data-bs-toggle="popover"]')
);
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl);
});

http = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
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
  image_uploadBtn.addEventListener("click", function () {
    imgInput.click();
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
      put(form_data, ID);
    }, 500);
  });

  get(ID).then((elem) => {
    postContent.innerHTML = elem.content;
  });


}

window.addEventListener("load", function () {
  if (this.document.title === "write") {
    writePage();
  }
});
