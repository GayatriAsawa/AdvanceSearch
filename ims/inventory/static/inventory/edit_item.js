      $('.select_field_class').select2( { placeholder: "Select here", maximumSelectionSize: 100  } );
      console.log($('.select_field_class').val)
function add(){
      var new_chq_no = parseInt($('#total_chq').val())+1;
      var new_input1 = "<td style='display : flex'><select style='margin-bottom: 1rem;white-space: nowrap; float: left; display : block' name='newtype_"+new_chq_no+"' id='newtype_"+new_chq_no+"'  class='form-control' aria-label='Type'><option selected>Storage Type</option> <option value='H'>Hard Disk Drive</option> <option value='S'>Solid State Drive</option> </select></td>"

      var new_input2="<td style='display : flex'><select style='margin-bottom: 1rem;white-space: nowrap; float: left; display : block' name='newmem_"+new_chq_no+"' id='newmem_"+new_chq_no+"' class='form-control' aria-label='Memory'><option selected>Memory</option><option value='128'>128</option><option value='256'>256</option><option value='512'>512</option><option value='1024'>1024</option></select></td>"
    //   var new_input="<input type='text' id='new_"+new_chq_no+"'>";
      $('#new_chq1').append(new_input1);
      $('#new_chq2').append(new_input2);
      $('#total_chq').val(new_chq_no)
    }
    function remove(){
      var last_chq_no = $('#total_chq').val();
      if(last_chq_no>1){
        $('#newtype_'+last_chq_no).remove();
        $('#newmem_'+last_chq_no).remove();
        $('#total_chq').val(last_chq_no-1); 
        
      }
    }
    $(document).ready(function () {
        getProject();
    });
    function getProject(){
        var skillsSelect = document.getElementById("id_project");
        var selectedText = skillsSelect.options[skillsSelect.selectedIndex].text;
        // alert(selectedText)

    $.ajax(
    {
        type:"GET",
        url: "/getProjectData",
        data:{
                 project_id: selectedText
        },
        success: function(data) 
        {
            // $( '#like'+ catid ).remove();
            // $( '#message' ).text(data);
            $('#projectName').val(data)
        }
     })

    }