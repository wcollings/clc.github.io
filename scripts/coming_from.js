const response = await fetch("../album_map.json");
const data=await response.json();
const params = new URLSearchParams(window.location.search);
if (params.has("album")) {
    var link_map = data;
    var album=params.get("album")
    var inpage=document.querySelector("#album")
    var alb_art = document.querySelector("#art")
    console.log("album art tag:")
    console.log(alb_art)
    console.log("inpage:")
    console.log(inpage)
    console.log("album from URL:")
    console.log(album)
    console.log("link_map:")
    console.log(link_map)
    console.log("Coming from '" + `${album}`  + "'")
    var link=link_map[album]
    inpage.textContent=album
    inpage.href="../" + `${link}` + "/index.html";
    alb_art.src="../" + `${link}` + "/" + `${link}` + '.jpg';
}