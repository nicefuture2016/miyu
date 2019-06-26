$(document).ready(function() {
//批量命令
    $("#FormHost").validate({
        rules: {
            groups_post: {
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
    $("#FormCron").validate({
        rules: {
            // groups_post: {
            //     required: true
            // },
            servers_post: {
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

        $("#FormSlb").validate({
        rules: {
            // groups_post: {
            //     required: true
            // },
            server_in_project_choice: {
                required: true
            },
            slb_project_post: {
                required: true
            }
            // path: {
            //     required: true
            // }
        }
    });

    var read = document.querySelector("#read");
	read.addEventListener('click', function(event) {
		event.preventDefault();
		var whichval = $("input[name='conf_manage']:checked").val();
		layer.prompt({title: '输入口令，并确认', formType: 1}, function(pass,index){
		layer.close(index);
		var index1 = layer.load(1, {shade: [0.1,'#fff'] });
		$.ajax({
			url: "/config/read_hosts",
			type: "POST",
			data: $("#FormHost").serialize()+$("#FormCron").serialize()+'&password='+pass+'&whichval='+whichval,
			success: function (data) {
				if (data == 'authorized fail'){layer.close(index1);layer.msg('密码错误', {icon: 5});}
				else if(data == 'validate'){layer.close(index1);layer.msg('缺少输入项', {icon: 5});}
				else{
					layer.close(index1);
					//document.getElementById("diffile").value = "";
					//alert(data['data']);
					document.getElementById("editresult").value = data['data'];
					var editor_one = CodeMirror.fromTextArea(document.getElementById("editresult"), {
						lineNumbers: true,
						matchBrackets: true,
						mode:'javascript',
						styleActiveLine: true,
						readOnly: false,
						lineWrapping: true,
						theme:"ambiance"
					});
					editor_one.setSize('auto','800px');
					layer.alert('总共：'+data['total']+'组'+'<br>失败：'+data['fail_count']+'组', {icon: 6});
				}
			},
			error: function (jqXHR, textStatus, errorThrown) {
				layer.close(index1);
				layer.msg('内部错误', {icon: 5});
			}
		});
		});


	});

    var edit = document.querySelector("#write");
	edit.addEventListener('click', function(event) {
		event.preventDefault();
		var whichval = $("input[name='conf_manage']:checked").val();
		var conten = document.getElementById("editresult").value;
		conten = encodeURIComponent(encodeURIComponent(conten));
		encodeURI(conten);
		layer.prompt({title: '输入口令，并确认', formType: 1}, function(pass,index){
		layer.close(index);
		var index1 = layer.load(1, {shade: [0.1,'#fff'] });
		$.ajax({
			url: "/config/edit_hosts",
			type: "POST",
			data: $("#FormHost").serialize()+$("#FormCron").serialize()+'&password='+pass+'&conten='+conten+'&whichval='+whichval,
			success: function (data) {
				if (data == 'authorized fail'){layer.close(index1);layer.msg('密码错误', {icon: 5});}
				else if(data == 'validate'){layer.close(index1);layer.msg('缺少输入项', {icon: 5});}
				else{
					layer.close(index1);
					layer.alert('总共：'+data['total']+'组'+'<br>失败：'+data['fail_count']+'组', {icon: 6});
				}
			},
			error: function (jqXHR, textStatus, errorThrown) {
				layer.close(index1);
				layer.msg('内部错误', {icon: 5});
			}
		});
		});


	});

    var slb = document.querySelector("#unmount");
	slb.addEventListener('click', function(event) {
		event.preventDefault();
		layer.prompt({title: '输入口令，并确认', formType: 1}, function(pass,index){
		layer.close(index);
		var index1 = layer.load(1, {shade: [0.1,'#fff'] });
		$.ajax({
			url: "/config/unmount_slb",
			type: "POST",
			data: $("#FormSlb").serialize()+'&password='+pass,
			success: function (data) {
				if (data == 'authorized fail'){layer.close(index1);layer.msg('密码错误', {icon: 5});}
				else if(data == 'validate'){layer.close(index1);layer.msg('缺少输入项', {icon: 5});}
				else{
					layer.close(index1);
					document.getElementById("editresult").value = data['data'];
					var editor_two = CodeMirror.fromTextArea(document.getElementById("editresult"), {
						lineNumbers: true,
						matchBrackets: true,
						mode:'javascript',
						styleActiveLine: true,
						readOnly: false,
						lineWrapping: true,
						theme:"ambiance"
					});
					editor_two.setSize('auto','800px');
					layer.alert('总共：'+data['total']+'组'+'<br>失败：'+data['fail_count']+'组', {icon: 6});
				}
			},
			error: function (jqXHR, textStatus, errorThrown) {
				layer.close(index1);
				layer.msg('内部错误', {icon: 5});
			}
		});
		});


	});

	var mountslb = document.querySelector("#mount");
	mountslb.addEventListener('click', function(event) {
		event.preventDefault();
		layer.prompt({title: '输入口令，并确认', formType: 1}, function(pass,index){
		layer.close(index);
		var index1 = layer.load(1, {shade: [0.1,'#fff'] });
		$.ajax({
			url: "/config/mount_slb",
			type: "POST",
			data: $("#FormSlb").serialize()+'&password='+pass,
			success: function (data) {
				if (data == 'authorized fail'){layer.close(index1);layer.msg('密码错误', {icon: 5});}
				else if(data == 'validate'){layer.close(index1);layer.msg('缺少输入项', {icon: 5});}
				else{
					layer.close(index1);
					document.getElementById("editresult").value = data['data'];
					var editor_three = CodeMirror.fromTextArea(document.getElementById("editresult"), {
						lineNumbers: true,
						matchBrackets: true,
						mode:'javascript',
						styleActiveLine: true,
						readOnly: false,
						lineWrapping: true,
						theme:"ambiance"
					});
					editor_three.setSize('auto','800px');
					layer.alert('总共：'+data['total']+'组'+'<br>失败：'+data['fail_count']+'组', {icon: 6});
				}
			},
			error: function (jqXHR, textStatus, errorThrown) {
				layer.close(index1);
				layer.msg('内部错误', {icon: 5});
			}
		});
		});


	});
	//var exec_command = document.querySelector("#exec_command");
	//exec_command.addEventListener('click', function(event) {
	//	event.preventDefault();
	//	layer.prompt({title: '输入口令，并确认', formType: 1}, function(pass,index){
	//	layer.close(index);
	//	var index1 = layer.load(1, {shade: [0.1,'#fff'] });
	//	$.ajax({
	//		url: "/config/execCommand",
	//		type: "POST",
	//		data: $("#FormCmd").serialize()+'&password='+pass,
	//		success: function (data) {
	//			if (data == 'authorized fail'){layer.close(index1);layer.msg('密码错误', {icon: 5});}
	//			else if(data == 'validate'){layer.close(index1);layer.msg('缺少输入项', {icon: 5});}
	//			else if(data == 'cmd fail'){layer.close(index1);layer.msg('禁止的命令', {icon: 5});}
	//			else{
	//				layer.close(index1);
	//				//document.getElementById("diffile").value = "";
	//				document.getElementById("result").value = data['data'];
	//				var editor_one = CodeMirror.fromTextArea(document.getElementById("result"), {
	//					lineNumbers: true,
	//					matchBrackets: true,
	//					mode:'javascript',
	//					styleActiveLine: true,
	//					readOnly: true,
	//					lineWrapping: true,
	//					theme:"ambiance"
	//				});
	//				editor_one.setSize('auto','800px');
	//				layer.alert('总共：'+data['total']+'组'+'<br>失败：'+data['fail_count']+'组', {icon: 6});
	//			}
	//		},
	//		error: function (jqXHR, textStatus, errorThrown) {
	//			layer.close(index1);
	//			layer.msg('内部错误', {icon: 5});
	//		}
	//	});
	//	});
//
//
	//});
	//
	//var file_upload = document.querySelector("#file_upload");
	//file_upload.addEventListener('click', function(event) {
	//	event.preventDefault();
//
	//	//console.log($("#FormUpd").serialize());
	//	//alert($("#myId .dz-preview").length);
	//	var filelist = "";
	//	for ( var i = 0; i < $("#myId .dz-preview").length; i++ ) {
	//		//filelist[i] = $($($("#myId .dz-preview")[i]).find('span')[1]).text()
	//		filelist += $($($("#myId .dz-preview")[i]).find('span')[1]).text()+':'
	//	}
	//
	//	console.log(filelist);
	//	//console.log($($($("#myId .dz-preview")[0]).find('span')[1]).text());
	//	layer.prompt({title: '输入口令，并确认', formType: 1}, function(pass,index){
	//	layer.close(index);
	//	var index1 = layer.load(1, {shade: [0.1,'#fff'] });
	//	$.ajax({
	//		url: "/config/fileUpload",
	//		type: "POST",
	//		data: $("#FormUpd").serialize()+'&password='+pass+'&filelist='+filelist,
	//		success: function (data) {
	//			if (data == 'authorized fail'){layer.close(index1);layer.msg('密码错误', {icon: 5});}
	//			else if(data == 'validate'){layer.close(index1);layer.msg('缺少输入项', {icon: 5});}
	//			else{
	//				layer.close(index1);
	//				document.getElementById("result").value = data['data'];
	//				var editor_one = CodeMirror.fromTextArea(document.getElementById("result"), {
	//					lineNumbers: true,
	//					matchBrackets: true,
	//					mode:'javascript',
	//					styleActiveLine: true,
	//					readOnly: true,
	//					lineWrapping: true,
	//					theme:"ambiance"
	//				});
	//				editor_one.setSize('auto','800px');
	//				layer.alert('总共：'+data['total']+'组'+'<br>失败：'+data['fail_count']+'组', {icon: 6});
	//			}
	//		},
	//		error: function (jqXHR, textStatus, errorThrown) {
	//			layer.close(index1);
	//			layer.msg('内部错误', {icon: 5});
	//		}
	//	});
	//	});
//

	//});
	
});

