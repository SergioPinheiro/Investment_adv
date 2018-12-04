function new_news(name) {
        var xhttp = new XMLHttpRequest();
        var message = name;
        xhttp.onreadystatechange = function() {
    			if (this.readyState == 4 && this.status == 200) {
    				let json = JSON.parse(this.responseText);
            clear_tables();
            var tb_noticias = document.getElementById("tb_noticias");
            for (const key in json["news"]) {
              // console.log(json["news"][key]);

              var row = tb_noticias.insertRow(0);
              var cell1 = row.insertCell(0);
              var cell2 = row.insertCell(1);

              cell1.innerHTML = key;
              cell2.innerHTML = json["news"][key];
              }

              var tb_ent = document.getElementById("tb_ent");
              for (const key in json["enterprises"]) {
                // console.log(json["news"][key]);

                var row = tb_ent.insertRow(0);
                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);

                cell1.innerHTML = key;
                cell2.innerHTML = json["enterprises"][key];
                }

                var tb_cli = document.getElementById("tb_cli");
                for (const key in json["clients"]) {
                  // console.log(json["news"][key]);

                  var row = tb_cli.insertRow(0);
                  var cell1 = row.insertCell(0);
                  var cell2 = row.insertCell(1);

                  cell1.innerHTML = key;
                  cell2.innerHTML = json["clients"][key];
                  }

                  var tb_pre = document.getElementById("tb_pre");
                  for (const key in json["adv"]) {
                    // console.log(json["news"][key]);

                    var row = tb_pre.insertRow(0);
                    var cell1 = row.insertCell(0);
                    var cell2 = row.insertCell(1);

                    cell1.innerHTML = key;
                    cell2.innerHTML = json["adv"][key];
                    }


    				}
        };
        xhttp.open("POST", "http://localhost:8080", true);
        xhttp.send(message);
}

function clear_tables(){
  var tb_noticias = document.getElementById("tb_noticias");
  var tb_ent = document.getElementById("tb_ent");
  var tb_cli = document.getElementById("tb_cli");
  var tb_pre = document.getElementById("tb_pre");

  tb_noticias.innerHTML = "";
  tb_ent.innerHTML = "";
  tb_cli.innerHTML = "";
  tb_pre.innerHTML = "";

}
