// $( document ).ready(function() {
//     alert("TEST1");
//     $(".oe_highlight").click(function(){
//         remover_item();
//     });
    
//  });
// //document.getElementById("btn_search").onclick = remover_item;
// function remover_item(){
//     var list = document.getElementsByClassName("ui-sortable")[0];
//     console.log(list);
//     list.removeChild(list.childNodes[0]);
//     console.log('Esta funcionando');
// }
$(".oe_action_button").click(function(){

    setTimeout(function(){ 
    console.log($("button[name*='search_visitor']"));
    $("button[name*='search_visitor']").attr("onclick","remover_item()");
     }, 2000);
      
      });
     
    function remover_item(){
    $("body").append("<div  id='loading_div' style='width: 100%;background-color:black;opacity:0.5;min-height: 100%;height: auto !important;position: fixed;top:0;left:0;'>test</div>")
    setTimeout(function(){ 
    alert("termino");
    $("#loading_div").remove();
     var list = document.getElementsByClassName("ui-sortable")[0];
        console.log(list);
        list.removeChild(list.childNodes[0]);
        console.log('Esta funcionando');
     }, 4000);
    }

