
// const image_uploadBtn = document.getElementById('image-upload')
// const imgInput = document.getElementById('img-uploadInput');
// const uploadImg = document.getElementById('uploadedImg');
// imgInput.addEventListener('change',function(){
//     if(this.files && this.files[0]) {
//         var reader = new FileReader();
//         reader.onload = function(e){
//             uploadImg.setAttribute('src',e.target.result);
//             image_uploadBtn.parentElement.setAttribute('style','height:auto;')
//             image_uploadBtn.setAttribute('style','opacity:.9;')
//             uploadImg.setAttribute('style','display:inline;max-height:500px;')
//         }
//         reader.readAsDataURL(this.files[0]);

//     }
// })
// image_uploadBtn.addEventListener('click', function(){
//   imgInput.click();
// })


// function editableMaxLengthValidator(element, max_length) {
//     const validator = (event)=>{
//         if(element.innerText.length > max_length) {
//             if(event.which==8){
//                 element.innerText= element.innerText.substring(0,max_length)
//                 const selection = window.getSelection();
//                 const range = document.createRange();
//                 selection.removeAllRanges();
//                 range.selectNodeContents(element);
//                 range.collapse(false);
//                 selection.addRange(range);
//                 element.focus();
                
//             }
//             event.preventDefault();
//         }
//     }
//     element.addEventListener('keydown', function(event){
//         validator(event);
        
//     })
// }

// postTitle = document.getElementById('create-post-title');
// editableMaxLengthValidator(postTitle, 40)

// postTitle.addEventListener('keydown', function(event){
//     if(event.which==13){
//         event.preventDefault();
  
//     }
// })
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
})