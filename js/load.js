
function getUrlParam(parameter, defaultvalue){
    var urlparameter = defaultvalue;
    if(window.location.href.indexOf(parameter) > -1){
        urlparameter = getUrlVars()[parameter];
        }
    return urlparameter;
}
function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}
function load_artist(link)
{
	var link=getUrlParam("artist","None");
	var temp="https://www.celticlyricscorner.site/"+link +"/artist_info.json";
	fetch(temp)
	.then(function(response) {
		return response.json();
	})
	.then(function (data) {
		fill_page(data);
	})
	}
	function fill_page(data)
	{
	document.getElementsByTagName("title")[0].innerHTML=data["artist"] +" Lyrics";
	var artist_tags=document.getElementsByTagName("art_name");
	for (var i=0; i < artist_tags.length; ++i)
	{
		artist_tags[i].innerHTML=data["artist"];
	}
	var albums=document.getElementById("albums")
	var iH='<td id="lc"> Albums </td><td>';
	for (var i=0; i < data["albums"].length; ++i)
	{
		iH+=data["albums"][i][0]+' - ';
		iH+='<a href="' + data["albums"][i][2] + '/' + data["albums"][i][2] + '.html"> ';
		iH+=data["albums"][i][1] + '</a> <br>';
	}
	iH+="</td>";
	albums.innerHTML=iH;

	var img=document.getElementById("img");
	var art_pic=new Image("150");
	art_pic.src="breabach.jpg";
	art_pic.alt=data["artist"];
	var lc=document.createElement("td");
	var rc=document.createElement("td");
	rc.innerHTML="<H1>" + data["artist"] +"</H1>";
	lc.setAttribute("id","lc");
	lc.appendChild(art_pic);
	img.appendChild(lc);
	img.appendChild(rc);

	if ("members" in data)
	{
		var mem_col=document.getElementById("members");
		mem_col.innerHTML='<td id="lc"> Members </td><td> ' + data["members"] + '</td>';
	}
}