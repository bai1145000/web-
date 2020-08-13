$(function(){

	var error_name = false;
	var error_password = false;
	var error_check_password = false;
	var error_email = false;
	var error_check = false;

	$('#user_name').blur(function() {
		check_user_name();
	});

	$('#pwd').blur(function() {
		check_pwd();
	});

	$('#cpwd').blur(function() {
		check_cpwd();
	});

	$('#email').blur(function() {
		check_email();
	});

	$('#allow').click(function() {
		if($(this).is(':checked'))
		{
			error_check = false;
			$(this).siblings('span').hide();
		}
		else
		{
			error_check = true;
			$(this).siblings('span').html('请勾选同意');
			$(this).siblings('span').show();
		}
	});

    //校园用户名
	function check_user_name(){
		var len = $('#user_name').val().length;
		var span = $('#unameSpan');
        if(len<5||len>20)
        {
           span.html('请输入5-20个字符的用户名')
            $('#user_name').next().show();
            error_name = true;
        }
        else
        {
            $('#user_name').next().hide();
            error_name = false;
        }

	}
	//第一次确认密码
	function check_pwd(){
	    var upwd = $('#pwd').val();
        //创建校验规则,密码要求6-8位，首位为字母，后面5-7位是数字
        var reg=/^[a-z]\w{5,7}$/;
         //获取span对象
        var span=$('#pwdSpan');
        if(upwd == null || upwd ==''){
            //输入校验结果
            span.html("*密码不能为空");
            span.css('color:red');
            error_password = false;
        }else if(reg.test(upwd)){
            //输入校验结果
            span.html("*密码通过");
            span.css('color:red');
        }else{
            //输入校验结果
            span.html("*密码格式不符");
            span.css('color:red');
            error_password = false;
        }
		//第一次密码为a123456，第二次密码为a1234567，则修改的第一次密码，确认密码也会重新校验
		check_cpwd();
	};

    //二次确认密码
	function check_cpwd(){
		var pass = $('#pwd').val();
		var cpass = $('#cpwd').val();
		//获取审判对象，提示信息
		var span = $('#pwd2Span');
		if(cpass=="" || cpass==null){
			span.html('密码不能为空');
			span.show();
			error_check_password = true;
		}else if(pass!== cpass)
		{
			span.html('两次输入的密码不一致');
			span.show();
			error_check_password = true;
		}
		else
		{
			$('#cpwd').next().hide();
			error_check_password = false;
		}

	};
	function createCode(){
	    //创建随机4位数字，math.floor向下取整
	    var code=Math.floor(Math.random()*9000+1000);
	    //获取元素对象
	    var  span=document.getElementById("codeSpan");
	    //将数字存放到span中
	    span.innerHTML=code;
	    //给span添加背景图片
	    //一次确认密码
		function check_pwd(){
		    //获取用户获得用户名信息
	        var upwd=$("pwd").value;
	         //创建校验规则,密码要求6-8位，首位为字母，后面5-7位是数字
	        var reg=/^[a-z]\w{5,7}$/;
	         //获取span对象
	        var span=$('#pwdSpan');
	        if(span==""||span==null){
	            //输入校验结果
	            span.innerHTML="*密码不能为空";
	            span.style.color="red";
	            return error_password = false;
	        }else if(reg.test(upwd)){
	            //输入校验结果
	            span.innerHTML="*密码通过";
	            span.style.color="green";
	        }else{
	            //输入校验结果
	            span.innerHTML="*密码格式不符"
	            span.style.color="red";
	              return error_password = false;
	        }
			//第一次密码为a123456，第二次密码为a1234567，则修改的第一次密码，确认密码也会重新校验
			check_cpwd();
		}
	};
	//校验确认验证码------------------
    function checkCode(){
        //获取用户输入验证码
            var code=document.getElementById("code").value;
        //获取随机验证码
            var code2=document.getElementById("codeSpan").innerHTML;
        //获取span对象
            var span=document.getElementById("codeSpan2");
        //比较前两次密码是否相同
            if( code==""|| code==null){
                //输入校验结果
                span.innerHTML="*验证码不能为空";
                span.style.color="red";
                createCode();
                return false;
            }else if(code==code2){
                //输入校验结果
                span.innerHTML="*验证码通过";
                span.style.color="green";
                return true;
            }else{
                //输入校验结果
                span.innerHTML="*验证码错误"
                span.style.color="red";
                createCode();
                return false;
            }
    }
    //email效验
	function check_email(){
		var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

		if(re.test($('#email').val()))
		{
			$('#email').next().hide();
			error_email = false;
		}else if($('#email') == null){
		    $('#email').next().html('请输入邮箱')
		    error_check_password = true;
		}else
		{
			$('#email').next().html('你输入的邮箱格式不正确')
			$('#email').next().show();
			error_check_password = true;
		}

	};

	$('#reg_form').submit(function() {
		check_user_name();
		check_pwd();
		check_cpwd();
		check_email();
		checkCode();

		if(error_name == false && error_password == false && error_check_password == false && error_email == false && error_check == false)
		{
			return true;
		}
		else
		{
			return false;
		}

	});

});