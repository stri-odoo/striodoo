$( document ).ready(function() {
   // alert("TEST2");
      // remover_item();
   
      console.log("cambio")
      console.log("Boton = " + $(".oe_action_button"))
      console.log("Boton = " + $(".oe_action_button").length)
      
      
      validar_boton();
   // $(".oe_action_button").click(function(){
   //    alert("TEST_1234");         
   //    setTimeout(function(){ 
   //       console.log($("button[name*='search_visitor']"));
   //       $("button[name*='search_visitor']").attr("onclick","remover_item()");
   //        }, 4000);
           
   //         });
   //       }, 4000);
   });
    
//  });
// //document.getElementById("btn_search").onclick = remover_item;
// function remover_item(){
//     var list = document.getElementsByClassName("ui-sortable")[0];
//     console.log(list);
//     list.removeChild(list.childNodes[0]);
//     console.log('Esta funcionando');
// }

     
    function remover_item(){
    $("body").append("<div  id='loading_div' style='width: 100%;background-color:black;opacity:0.5;min-height: 100%;height: auto !important;position: fixed;top:0;left:0;'>test</div>")
    setTimeout(function(){ 
      var list = document.getElementsByClassName("ui-sortable")[0];
      console.log(list)
    if(list<=0)
    {
       console.log("no encontrado")
      remover_item()
   }
   else
   {
      remover_item_final()
   }
     }, 500);
    }

    function remove_item_final(){
      alert("termino");
      $("#loading_div").remove();
       var list = document.getElementsByClassName("ui-sortable")[0];
          console.log(list);
          list.removeChild(list.childNodes[0]);
          console.log('Esta funcionando');
   }

   function validar_boton() {
      setTimeout(function(){
      var boton = $(".oe_action_button").length;
      if (boton <= 0) {
         console.log("No se Encuentra!")
         validar_boton()
      }
      else {
         $(".oe_action_button").attr("onclick","remover_item()");
         // remover_item()
      }
      },500)
      
   }