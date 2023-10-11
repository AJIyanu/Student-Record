const img = document.getElementById("cropmehere");
const upload = document.querySelector("#pp-image");
const crop = document.querySelector("#cropmehere");
const contain = document.querySelector("#dp-crop");
const cancel = document.querySelector("#cancel");
const cropped = document.querySelector("#done");
const dp = document.querySelector("#dp");
const level = document.querySelector('#change-level').value;

let imgurl, cropper, uploadUrl

upload.addEventListener("change", () => {
    imgurl = URL.createObjectURL(upload.files[0])
    crop.src = imgurl;
    contain.style.display = "block";

    cropper = new Cropper(img, {
        aspectRatio: 1,
        preview: ".cropped-upload",
        viewMode: 3
    })

    cancel.onclick = function () {
        cropper.destroy();
        cropper = null
        contain.style.display = "none";
    }

    cropped.onclick = function () {
        canvas = cropper.getCroppedCanvas({
            width: 160,
            height: 160
        });

        uploadUrl = canvas.toDataURL()

        cropper.destroy();
        cropper = null;

        canvas.toBlob((blob) => {
            const formData = new FormData();

            formData.append("dp_image", blob);

            fetch(`/register/${level}`, {
                method: 'POST',
                body: formData
            })
            .then(() => {
                contain.style.display = "none";
                dp.src = uploadUrl;
            })
            .catch(err => console.error)
        })
    }

    upload.value = "";
})
