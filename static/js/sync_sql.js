$(document).ready(function() {
//批量命令
    $("#FormOnline").validate({
        rules: {
            test_servers_post: {
                required: true
            },
            // servers_post: {
            //     required: true
            // },
            env: {
                required: true
            }
            // command_post: {
            //     required: true
            // }
        }
    });
    $("#FormTest").validate({
        rules: {
            test_target_servers_post: {
                required: true
            },
            test_source_servers_post: {
                required: true
            },
            user: {
                required: true
            }
            // path: {
            //     required: true
            // }
        }
    });


    var edit = document.querySelector("#write_online");
	edit.addEventListener('click', function(event) {
		event.preventDefault();
		var whichdata = $("input[name='database']:checked").val();
		layer.prompt({title: '输入口令，并确认', formType: 1}, function(pass,index){
		layer.close(index);
		var index1 = layer.load(1, {shade: [0.1,'#fff'] });
		$.ajax({
			url: "/devops/rsync_online_sql",
			type: "POST",
			data: $("#FormOnline").serialize()+'&password='+pass+'&whichdata='+whichdata,
			success: function (data) {
				if (data == 'authorized fail'){layer.close(index1);layer.msg('密码错误', {icon: 5});}
				else if(data == 'validate'){layer.close(index1);layer.msg('缺少输入项', {icon: 5});}
				else{
					layer.close(index1);
					document.getElementById("sqlresult").value = data['data'];
					var editor_one = CodeMirror.fromTextArea(document.getElementById("sqlresult"), {
						lineNumbers: true,
						matchBrackets: true,
						mode:'javascript',
						styleActiveLine: true,
						readOnly: true,
						lineWrapping: true,
						theme:"ambiance"
					});
					editor_one.setSize('auto','800px');
					layer.alert('成功：'+data['success_count']+'表'+'<br>失败：'+data['fail_count']+'表', {icon: 6});
				}
			},
			error: function (jqXHR, textStatus, errorThrown) {
				layer.close(index1);
				layer.msg('内部错误', {icon: 5});
			}
		});
		});


	});


	var edit = document.querySelector("#write_test");
	edit.addEventListener('click', function(event) {
		event.preventDefault();
		var whichdata = $("input[name='database']:checked").val();
		layer.prompt({title: '输入口令，并确认', formType: 1}, function(pass,index){
		layer.close(index);
		var index1 = layer.load(1, {shade: [0.1,'#fff'] });
		$.ajax({
			url: "/devops/rsync_test_sql",
			type: "POST",
			data: $("#FormTest").serialize()+'&password='+pass+'&whichdata='+whichdata,
			success: function (data) {
				if (data == 'authorized fail'){layer.close(index1);layer.msg('密码错误', {icon: 5});}
				else if(data == 'validate'){layer.close(index1);layer.msg('缺少输入项', {icon: 5});}
				else{
					layer.close(index1);
					document.getElementById("sqlresult").value = data['data'];
					var editor_one = CodeMirror.fromTextArea(document.getElementById("sqlresult"), {
						lineNumbers: true,
						matchBrackets: true,
						mode:'javascript',
						styleActiveLine: true,
						readOnly: true,
						lineWrapping: true,
						theme:"ambiance"
					});
					editor_one.setSize('auto','800px');
					layer.alert('成功：'+data['success_count']+'表'+'<br>失败：'+data['fail_count']+'表', {icon: 6});
				}
			},
			error: function (jqXHR, textStatus, errorThrown) {
				layer.close(index1);
				layer.msg('内部错误', {icon: 5});
			}
		});
		});


	});
	
});

